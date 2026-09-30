# VoiceShield-CyberDemo 🛡️🎙️
> **Dual-Module Real-Time Voice Cloning & Deepfake Detection System**

VoiceShield-CyberDemo is a practical cybersecurity dual-module implementation designed for research, threat simulation, and practical defense analysis. The project demonstrates both a voice threat vector (**Real-Time Zero-Shot Voice Cloning & Virtual Audio Routing**) and a defense mechanism (**Real-Time Audio Deepfake Tracking, Spectral Analysis & Classification Dashboard**).

---

## 🏗️ Architecture Overview

```
VoiceShield-CyberDemo/
│
├── requirements.txt              # Project Python dependencies
├── README.md                     # System documentation & setup guide
│
├── voice_cloner_stream/          # Module 1: Threat Vector Simulation
│   ├── __init__.py
│   ├── config.py                 # Audio sample rate, chunk sizes & DSP settings
│   ├── cloner_engine.py          # Zero-shot voice conversion & DSP synthesis pipeline
│   └── virtual_stream.py         # Microphone capture & virtual audio cable routing
│
└── voice_detector/               # Module 2: Defense & Real-Time Tracking
    ├── __init__.py
    ├── main.py                   # FastAPI server with WebSockets for real-time telemetry
    ├── audio_processor.py        # Librosa DSP feature extraction (Mel-Spectrograms, STFT, Phase)
    ├── model_inference.py        # Lightweight deepfake classifier & artifact detection engine
    └── static/
        └── index.html            # Ultra-responsive real-time cybersecurity dashboard UI
```

---

## 🚀 Quick Start

### 1. Installation & Environment Setup
```bash
# Navigate to project root
cd VoiceShield-CyberDemo

# Create virtual environment
python -m venv venv

# Activate environment (Windows)
.\venv\Scripts\activate
# Activate environment (Linux/macOS)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running Module 2 (Defensive Detection Dashboard)
Launch the FastAPI WebSocket backend and live telemetry dashboard:
```bash
python -m voice_detector.main
```
Navigate to `http://localhost:8000` in your web browser. Grant microphone permissions to see real-time waveform analysis, spectral feature tracking, and synthetic risk scores!

### 3. Running Module 1 (Threat Simulation Stream)
Simulate real-time voice conversion and stream routing:
```bash
python -m voice_cloner_stream.virtual_stream --ref voice_sample.wav
```

---

## 🔍 Module Details

### Module 1: `voice_cloner_stream`
* **Zero-Shot Voice Conversion (`cloner_engine.py`)**: Accepts reference audio target profiles, extracts speaker pitch/formant embeddings, and converts audio frames in real time using Torch/DSP frame-by-frame processing.
* **Virtual Cable Hook (`virtual_stream.py`)**: Uses `sounddevice` / PyAudio streams to intercept microphone input, perform real-time conversion, and route synthetic frames into virtual audio devices (VB-Audio Cable, Loopback).

### Module 2: `voice_detector`
* **Librosa Audio Processor (`audio_processor.py`)**: Performs Short-Time Fourier Transform (STFT), Mel-Spectrogram analysis, Spectral Rolloff/Centroid calculation, and STFT Phase Discontinuity checks.
* **Artifact Detection Engine (`model_inference.py`)**: Evaluates synthetic voice artifacts (high-frequency cutoffs, pitch jitter anomalies, phase variance) to yield a real-time risk score between `0.0` (Authentic) and `1.0` (Deepfake/Synthetic).
* **WebSocket Dashboard (`static/index.html`)**: Interactive dark-mode dashboard displaying live audio oscilloscopes, risk gauges, spectral meters, and frame latency telemetry.

---

## 🔐 Ethical & Defensive Notice
This project is developed solely for academic research, defensive cybersecurity validation, and thesis defense demonstrations. All voice cloning capabilities are contained within local loopback interfaces for threat emulation purposes.
