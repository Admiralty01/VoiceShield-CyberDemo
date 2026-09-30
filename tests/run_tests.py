import unittest
import numpy as np
from voice_detector.audio_processor import AudioProcessor
from voice_detector.model_inference import DeepfakeDetectorModel
from voice_cloner_stream.cloner_engine import VoiceClonerEngine


class TestVoiceShield(unittest.TestCase):
    def test_audio_processor_silence(self):
        processor = AudioProcessor(sample_rate=16000)
        silent_audio = np.zeros(1024, dtype=np.float32)
        features = processor.process_chunk(silent_audio)
        self.assertEqual(features["rms_energy"], 0.0)
        self.assertEqual(features["spectral_centroid"], 0.0)
        self.assertEqual(len(features["mel_db_summary"]), 16)

    def test_audio_processor_sine(self):
        processor = AudioProcessor(sample_rate=16000)
        t = np.linspace(0, 1.0, 16000, endpoint=False)
        sine_audio = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
        features = processor.process_chunk(sine_audio[:1024])
        self.assertGreater(features["rms_energy"], 0.1)
        self.assertGreater(features["spectral_centroid"], 0.0)

    def test_model_inference(self):
        model = DeepfakeDetectorModel(high_risk_threshold=0.65)
        silence_res = model.predict({"rms_energy": 0.0})
        self.assertEqual(silence_res["label"], "SILENCE")
        self.assertEqual(silence_res["risk_percentage"], 0.0)

        synth_res = model.predict({
            "rms_energy": 0.2,
            "spectral_centroid": 1500.0,
            "spectral_rolloff": 3000.0,
            "phase_incoherence": 2.0,
            "high_freq_ratio": 0.01
        })
        self.assertIn("risk_score", synth_res)
        self.assertIn("risk_percentage", synth_res)
        self.assertGreater(synth_res["risk_percentage"], 40.0)

    def test_cloner_engine(self):
        engine = VoiceClonerEngine()
        engine.set_pitch_shift(3.0)
        engine.set_formant_shift(1.2)
        frame = (0.3 * np.random.randn(1024)).astype(np.float32)
        out_frame = engine.process_frame(frame)
        self.assertEqual(len(out_frame), 1024)
        self.assertEqual(out_frame.dtype, np.float32)


if __name__ == "__main__":
    unittest.main()
