"""
Microphone Capture & Virtual Audio Cable Routing Hook
Intercepts live input microphone streams, passes audio through Cloner Engine,
and routes synthesized frames into virtual audio devices or output speakers.
"""

import argparse
import time
import numpy as np
import sounddevice as sd
from .config import config
from .cloner_engine import VoiceClonerEngine


class VirtualAudioStream:
    """
    Manages real-time audio input/output stream hooks.
    """

    def __init__(self, reference_path: str = None, input_device: int = None, output_device: int = None):
        self.sample_rate = config.SAMPLE_RATE
        self.channels = config.CHANNELS
        self.chunk_size = config.CHUNK_SIZE
        
        self.input_device = input_device if input_device is not None else config.INPUT_DEVICE_INDEX
        self.output_device = output_device if output_device is not None else config.OUTPUT_DEVICE_INDEX
        
        self.engine = VoiceClonerEngine(reference_audio_path=reference_path)
        self.stream = None
        self.is_running = False

    def audio_callback(self, indata, outdata, frames, time_info, status):
        """
        Sounddevice stream callback running in a real-time high-priority audio thread.
        """
        if status:
            print(f"[VirtualStream Warning] Audio Status: {status}")

        # Extract primary input channel
        input_buffer = indata[:, 0] if indata.ndim > 1 else indata
        
        # Pass buffer through Zero-Shot Voice Conversion Engine
        converted_buffer = self.engine.process_frame(input_buffer)
        
        # Populate all output channels safely
        if outdata.ndim > 1:
            for ch in range(outdata.shape[1]):
                outdata[:, ch] = converted_buffer
        else:
            outdata[:] = converted_buffer

    def start(self):
        """
        Starts the low-latency duplex audio stream.
        """
        print("\n========================================================")
        print(" 🎙️ VoiceShield Threat Simulator: Virtual Stream Active ")
        print("========================================================")
        print(f" Sample Rate    : {self.sample_rate} Hz")
        print(f" Chunk Size     : {self.chunk_size} frames")
        print(f" Input Device   : {self.input_device if self.input_device is not None else 'System Default Mic'}")
        print(f" Output Device  : {self.output_device if self.output_device is not None else 'System Default Speaker / Virtual Cable'}")
        print(" Press Ctrl+C to stop streaming.\n")

        self.is_running = True
        
        device_tuple = None
        if self.input_device is not None or self.output_device is not None:
            device_tuple = (self.input_device, self.output_device)

        try:
            with sd.Stream(
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                device=device_tuple,
                channels=self.channels,
                dtype='float32',
                callback=self.audio_callback
            ):
                while self.is_running:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[VirtualStream] Stopping audio stream...")
        except Exception as e:
            print(f"[VirtualStream Error] Failed to initialize stream: {e}")
        finally:
            self.is_running = False
            print("[VirtualStream] Audio stream closed successfully.")


def list_audio_devices():
    """Prints all available hardware input/output and virtual cable audio devices."""
    print("\n--- Available System Audio Devices ---")
    try:
        devices = sd.query_devices()
        for idx, dev in enumerate(devices):
            max_in = dev['max_input_channels']
            max_out = dev['max_output_channels']
            print(f"[{idx}] {dev['name']} (Inputs: {max_in}, Outputs: {max_out})")
    except Exception as e:
        print(f"Failed to query audio devices: {e}")
    print("--------------------------------------\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VoiceShield Threat Simulation: Virtual Audio Stream Routing")
    parser.add_argument("--ref", type=str, default=None, help="Path to reference speaker target wav file")
    parser.add_argument("--in-device", type=int, default=None, help="Input microphone device index")
    parser.add_argument("--out-device", type=int, default=None, help="Output speaker/Virtual Audio Cable index")
    parser.add_argument("--list-devices", action="store_true", help="List all available audio devices and exit")
    parser.add_argument("--pitch", type=float, default=2.0, help="Pitch shift semitones (-12 to +12)")

    args = parser.parse_args()

    if args.list_devices:
        list_audio_devices()
    else:
        stream = VirtualAudioStream(
            reference_path=args.ref,
            input_device=args.in_device,
            output_device=args.out_device
        )
        stream.engine.set_pitch_shift(args.pitch)
        stream.start()

