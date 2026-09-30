"""
FastAPI Backend with WebSockets for Real-Time Audio Telemetry & Deepfake Tracking
"""

import os
import json
from datetime import datetime
import numpy as np
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from .audio_processor import AudioProcessor
from .model_inference import DeepfakeDetectorModel

app = FastAPI(
    title="VoiceShield-CyberDemo: Real-Time Deepfake Detection Telemetry",
    description="WebSocket server for streaming audio feature analysis & synthetic voice detection.",
    version="1.0.0"
)

# Enable CORS for cross-origin local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core DSP & Inference Modules
processor = AudioProcessor(sample_rate=16000, n_fft=512, hop_length=256)
detector = DeepfakeDetectorModel(high_risk_threshold=0.65)

# Static Files Directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serves the main real-time telemetry dashboard UI."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>VoiceShield Backend Online. index.html not found.</h1>"


@app.websocket("/ws/stream")
async def websocket_audio_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint receiving binary Float32 PCM audio frames from client/mic or virtual routing,
    processing STFT features, and returning real-time risk scores & spectral telemetry.
    """
    await websocket.accept()
    print("[WebSocket] Client connected to VoiceShield Telemetry Feed.")
    
    # Create per-session detector instance to isolate telemetry state
    session_detector = DeepfakeDetectorModel(high_risk_threshold=0.65)

    try:
        while True:
            message = await websocket.receive()
            
            if "bytes" in message and message["bytes"]:
                raw_bytes = message["bytes"]
                if len(raw_bytes) == 0:
                    continue
                    
                # Convert raw PCM bytes to float32 numpy array
                audio_frame = np.frombuffer(raw_bytes, dtype=np.float32)
                
                # Extract Librosa DSP features
                features = processor.process_chunk(audio_frame)
                
                # Perform Deepfake & Artifact Classification
                inference_result = session_detector.predict(features)
                
                # Construct Telemetry Payload
                payload = {
                    "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
                    "features": features,
                    "detection": inference_result
                }
                
                # Send JSON analysis back to UI
                await websocket.send_text(json.dumps(payload))

            elif "text" in message and message["text"]:
                # Handle control/ping messages
                try:
                    data = json.loads(message["text"])
                    if data.get("type") == "ping":
                        await websocket.send_json({"type": "pong", "status": "active"})
                    elif data.get("type") == "reset":
                        session_detector.reset()
                        await websocket.send_json({"type": "reset_ack", "status": "cleared"})
                except json.JSONDecodeError:
                    pass

    except WebSocketDisconnect:
        print("[WebSocket] Client disconnected cleanly from Telemetry Feed.")
    except Exception as e:
        print(f"[WebSocket Error] Exception in streaming pipeline: {e}")


if __name__ == "__main__":
    uvicorn.run("voice_detector.main:app", host="0.0.0.0", port=8000, reload=True)

