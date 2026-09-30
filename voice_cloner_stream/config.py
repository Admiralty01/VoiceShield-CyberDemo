"""
Configuration Settings for Real-Time Voice Cloning & Virtual Routing
"""

import os
from dataclasses import dataclass

@dataclass
class AudioConfig:
    # Audio Sampling & Frame Setup
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    CHUNK_SIZE: int = 1024       # 64ms frame at 16kHz
    HOP_LENGTH: int = 256
    N_FFT: int = 512
    N_MELS: int = 80
    
    # Latency & Buffer Settings
    BUFFER_FRAMES: int = 4
    INPUT_DEVICE_INDEX: int = None   # Default input mic
    OUTPUT_DEVICE_INDEX: int = None  # Default output speaker / Virtual Cable
    
    # Pitch & Voice Modification Limits
    PITCH_SHIFT_SEMITONES: float = 0.0
    FORMANT_SHIFT_RATIO: float = 1.0
    ENABLE_DSP_EMULATION: bool = True

    # Checkpoint / Reference Audio Path
    DEFAULT_REFERENCE_PATH: str = os.path.join(
        os.path.dirname(__file__), "samples", "reference_voice.wav"
    )

config = AudioConfig()
