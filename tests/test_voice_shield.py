"""
Comprehensive Automated Test Suite for VoiceShield-CyberDemo
Tests DSP feature extraction, classifier inference, FastAPI WebSockets, and zero-shot voice cloner engine.
"""

import pytest
import numpy as np
from fastapi.testclient import TestClient

from voice_detector.audio_processor import AudioProcessor
from voice_detector.model_inference import DeepfakeDetectorModel
from voice_detector.main import app
from voice_cloner_stream.cloner_engine import VoiceClonerEngine


def test_audio_processor_silence():
    processor = AudioProcessor(sample_rate=16000)
    silent_audio = np.zeros(1024, dtype=np.float32)
    features = processor.process_chunk(silent_audio)
    
    assert features["rms_energy"] == 0.0
    assert features["spectral_centroid"] == 0.0
    assert len(features["mel_db_summary"]) == 16


def test_audio_processor_sine_wave():
    processor = AudioProcessor(sample_rate=16000)
    t = np.linspace(0, 1.0, 16000, endpoint=False)
    sine_audio = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
    
    features = processor.process_chunk(sine_audio[:1024])
    assert features["rms_energy"] > 0.1
    assert features["spectral_centroid"] > 0.0
    assert isinstance(features["mel_db_summary"], list)


def test_deepfake_detector_model():
    model = DeepfakeDetectorModel(high_risk_threshold=0.65)
    
    # Silence test
    silence_res = model.predict({"rms_energy": 0.0})
    assert silence_res["label"] == "SILENCE"
    assert silence_res["risk_percentage"] == 0.0
    
    # Synthetic artifact test
    synth_features = {
        "rms_energy": 0.2,
        "spectral_centroid": 1500.0,
        "spectral_rolloff": 3000.0,
        "phase_incoherence": 2.0,
        "high_freq_ratio": 0.01
    }
    synth_res = model.predict(synth_features)
    assert "risk_score" in synth_res
    assert "risk_percentage" in synth_res
    assert synth_res["risk_percentage"] > 40.0


def test_cloner_engine_process_frame():
    engine = VoiceClonerEngine()
    engine.set_pitch_shift(3.0)
    engine.set_formant_shift(1.2)
    
    frame = (0.3 * np.random.randn(1024)).astype(np.float32)
    out_frame = engine.process_frame(frame)
    
    assert isinstance(out_frame, np.ndarray)
    assert len(out_frame) == 1024
    assert out_frame.dtype == np.float32


def test_fastapi_websocket_endpoint():
    client = TestClient(app)
    with client.websocket_connect("/ws/stream") as websocket:
        # Test ping/pong
        websocket.send_text('{"type": "ping"}')
        data = websocket.receive_json()
        assert data["type"] == "pong"
        assert data["status"] == "active"
        
        # Test binary Float32 PCM frame transmission
        test_frame = (0.2 * np.random.randn(1024)).astype(np.float32)
        websocket.send_bytes(test_frame.tobytes())
        telemetry = websocket.receive_json()
        
        assert "timestamp" in telemetry
        assert "features" in telemetry
        assert "detection" in telemetry
