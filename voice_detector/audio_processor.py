import math
import numpy as np
import scipy.signal as signal

try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False


class AudioProcessor:
    """
    Extracts DSP features and spectral metrics from audio frame buffers.
    """

    def __init__(self, sample_rate: int = 16000, n_fft: int = 512, hop_length: int = 256, n_mels: int = 80):
        self.sample_rate = sample_rate
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.n_mels = n_mels

    def process_chunk(self, raw_audio: np.ndarray) -> dict:
        """
        Processes a single raw PCM audio frame buffer and returns extracted feature metrics.
        """
        if raw_audio is None or len(raw_audio) < 64:
            return self._empty_response()

        # Ensure float32 normalized signal [-1.0, 1.0]
        if raw_audio.dtype != np.float32:
            raw_audio = raw_audio.astype(np.float32) / 32768.0

        # Replace any non-finite values (NaN / Inf) with 0.0
        raw_audio = np.nan_to_num(raw_audio, nan=0.0, posinf=0.0, neginf=0.0)

        # Calculate Root Mean Square (RMS) energy
        rms = float(np.sqrt(np.mean(raw_audio ** 2)))
        
        # Avoid processing silence
        if rms < 0.005:
            return self._empty_response()

        # 1. Short-Time Fourier Transform (STFT)
        if HAS_LIBROSA:
            stft = librosa.stft(y=raw_audio, n_fft=self.n_fft, hop_length=self.hop_length)
            spectrogram = np.abs(stft)
            phase = np.angle(stft)

            # Mel-Spectrogram & Spectral Features via Librosa
            mel_spec = librosa.feature.melspectrogram(
                S=spectrogram**2, sr=self.sample_rate, n_mels=self.n_mels
            )
            mel_db = librosa.power_to_db(mel_spec, ref=np.max)

            spectral_centroid = librosa.feature.spectral_centroid(
                y=raw_audio, sr=self.sample_rate, n_fft=self.n_fft, hop_length=self.hop_length
            )
            avg_centroid = float(np.mean(spectral_centroid))

            spectral_rolloff = librosa.feature.spectral_rolloff(
                y=raw_audio, sr=self.sample_rate, n_fft=self.n_fft, hop_length=self.hop_length, roll_percent=0.85
            )
            avg_rolloff = float(np.mean(spectral_rolloff))
        else:
            # Native SciPy / NumPy Fallback Implementation
            f, t, stft = signal.stft(raw_audio, fs=self.sample_rate, nperseg=self.n_fft, noverlap=self.n_fft - self.hop_length)
            spectrogram = np.abs(stft)
            phase = np.angle(stft)

            # Spectral Centroid (Weighted mean of frequencies)
            freqs = f[:, np.newaxis]
            tot_mag = np.sum(spectrogram, axis=0) + 1e-9
            avg_centroid = float(np.mean(np.sum(spectrogram * freqs, axis=0) / tot_mag))

            # Spectral Rolloff (85% energy frequency)
            cum_energy = np.cumsum(spectrogram**2, axis=0)
            total_e = cum_energy[-1, :] + 1e-9
            rolloff_idx = np.argmax(cum_energy >= 0.85 * total_e, axis=0)
            avg_rolloff = float(np.mean(f[rolloff_idx]))

            # Log Spectrogram summary for UI
            mel_db = 10 * np.log10(spectrogram + 1e-9)

        # 5. Phase Discontinuity & High-Frequency Artifact Analysis
        # Phase incoherence unwraps phase across frames to accurately measure phase variance
        if phase.ndim == 2 and phase.shape[1] > 1:
            unwrapped_phase = np.unwrap(phase, axis=1)
            phase_diff = np.diff(unwrapped_phase, axis=1)
            phase_incoherence = float(np.var(phase_diff))
        else:
            phase_incoherence = 0.0
        
        # High-frequency band power ratio (> 6.5 kHz)
        nyquist = self.sample_rate / 2.0
        n_bins = spectrogram.shape[0]
        high_freq_bin_start = int((6500.0 / nyquist) * n_bins)
        high_freq_bin_start = max(0, min(high_freq_bin_start, n_bins - 1))
        
        high_freq_energy = float(np.sum(spectrogram[high_freq_bin_start:, :]))
        total_energy = float(np.sum(spectrogram)) + 1e-9
        high_freq_ratio = high_freq_energy / total_energy

        # Sanitize outputs against NaN / Inf
        avg_centroid = 0.0 if not math.isfinite(avg_centroid) else avg_centroid
        avg_rolloff = 0.0 if not math.isfinite(avg_rolloff) else avg_rolloff
        phase_incoherence = 0.0 if not math.isfinite(phase_incoherence) else phase_incoherence
        high_freq_ratio = 0.0 if not math.isfinite(high_freq_ratio) else high_freq_ratio

        mel_summary = np.mean(mel_db, axis=1)[:16] if mel_db.size > 0 else np.zeros(16)
        mel_summary = np.nan_to_num(mel_summary, nan=0.0, posinf=0.0, neginf=-80.0)

        return {
            "rms_energy": round(float(rms), 4),
            "spectral_centroid": round(float(avg_centroid), 2),
            "spectral_rolloff": round(float(avg_rolloff), 2),
            "phase_incoherence": round(float(phase_incoherence), 4),
            "high_freq_ratio": round(float(high_freq_ratio), 4),
            "mel_db_summary": [round(float(x), 2) for x in mel_summary]
        }

    def _empty_response(self) -> dict:
        return {
            "rms_energy": 0.0,
            "spectral_centroid": 0.0,
            "spectral_rolloff": 0.0,
            "phase_incoherence": 0.0,
            "high_freq_ratio": 0.0,
            "mel_db_summary": [0.0] * 16
        }

