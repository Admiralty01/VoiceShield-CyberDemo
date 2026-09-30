"""
Zero-Shot Voice Conversion & Synthesis Engine
Provides a modular architecture for audio feature matching, pitch shifting, 
formant adaptation, and frame-by-frame streaming voice conversion.
"""

import numpy as np
import scipy.signal as signal
from .config import config


class VoiceClonerEngine:
    """
    Simulates real-time zero-shot voice conversion pipeline.
    Transforms streaming input microphone buffers into target voice characteristics.
    """

    def __init__(self, reference_audio_path: str = None):
        self.sample_rate = config.SAMPLE_RATE
        self.chunk_size = config.CHUNK_SIZE
        self.reference_audio_path = reference_audio_path
        self.target_pitch_shift = config.PITCH_SHIFT_SEMITONES
        self.formant_shift = config.FORMANT_SHIFT_RATIO
        
        # Internal state buffers for streaming cross-fading & DSP filtering
        self.previous_frame = np.zeros(self.chunk_size, dtype=np.float32)
        self.filter_zi = None
        self.is_initialized = False
        
        if reference_audio_path:
            self.load_reference_profile(reference_audio_path)

    def load_reference_profile(self, audio_path: str) -> bool:
        """
        Loads and extracts speaker embedding / acoustic target profile from reference audio file.
        """
        print(f"[ClonerEngine] Loading reference speaker profile from: {audio_path}")
        # Mock loading acoustic target characteristics
        self.is_initialized = True
        return True

    def process_frame(self, in_data: np.ndarray) -> np.ndarray:
        """
        Processes a single audio buffer frame in real-time.
        Applies DSP pitch shifting, formant modification, and acoustic matching.
        """
        if in_data is None or len(in_data) == 0:
            return np.zeros(self.chunk_size, dtype=np.float32)

        # Convert to float32 normalized signal [-1.0, 1.0]
        if in_data.dtype != np.float32:
            in_data = in_data.astype(np.float32) / 32768.0

        processed = in_data.copy()
        n_samples = len(processed)

        # 1. Pitch Shift Simulation via High-Quality Linear Interpolation
        if abs(self.target_pitch_shift) > 0.01:
            factor = 2 ** (self.target_pitch_shift / 12.0)
            orig_indices = np.arange(n_samples)
            resampled_indices = np.arange(0, n_samples, factor)
            
            # Interpolate resampled waveform smoothly
            resampled = np.interp(resampled_indices, orig_indices, processed)
            
            if len(resampled) < n_samples:
                processed = np.pad(resampled, (0, n_samples - len(resampled)))
            else:
                processed = resampled[:n_samples]

        # 2. Formant Modulation / Spectral Envelope Smoothing with State Preservation
        if abs(self.formant_shift - 1.0) > 0.01:
            cutoff = min(0.45, 0.2 * self.formant_shift)
            b, a = signal.butter(4, cutoff, btype='low')
            
            if self.filter_zi is None or len(self.filter_zi) != max(len(a), len(b)) - 1:
                self.filter_zi = signal.lfilter_zi(b, a) * processed[0]
                
            processed, self.filter_zi = signal.lfilter(b, a, processed, zi=self.filter_zi)

        # 3. Frame Overlap-Add Crossfade to prevent streaming pops/clicks
        crossfade_len = min(64, n_samples)
        fade_in = np.linspace(0.0, 1.0, crossfade_len, dtype=np.float32)
        fade_out = np.linspace(1.0, 0.0, crossfade_len, dtype=np.float32)
        
        processed[:crossfade_len] = (processed[:crossfade_len] * fade_in) + (self.previous_frame[-crossfade_len:] * fade_out)
        self.previous_frame = processed.copy()

        return processed.astype(np.float32)

    def set_pitch_shift(self, semitones: float):
        """Dynamically update pitch shift target."""
        self.target_pitch_shift = semitones

    def set_formant_shift(self, ratio: float):
        """Dynamically update formant ratio target."""
        self.formant_shift = ratio

