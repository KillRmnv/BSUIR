"""Offline TTS engines: Piper (neural, primary) and eSpeak-NG (formant, fallback)."""
import io
import os
import shutil
import subprocess
import tempfile
import threading
import wave

from services.errors import ServiceError
from tts.voices import Voice

try:
    from piper import PiperVoice, SynthesisConfig
except ImportError:  # optional dependency (dev host without piper-tts)
    PiperVoice = None
    SynthesisConfig = None

MODEL_DIR = os.environ.get(
    "TTS_MODEL_DIR",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tts_models"),
)

_espeak_lock = threading.Lock()
_model_lock = threading.Lock()
_model_cache: dict = {}


def espeak_available() -> bool:
    return shutil.which("espeak-ng") is not None


def piper_available() -> bool:
    return PiperVoice is not None


def model_path(model: str) -> str:
    return os.path.join(MODEL_DIR, model + ".onnx")


def model_present(model: str) -> bool:
    return piper_available() and os.path.exists(model_path(model))


def _get_piper_voice(model: str):
    path = model_path(model)
    if not os.path.exists(path):
        raise ServiceError(f"Piper model not found: {model}")
    with _model_lock:
        if model not in _model_cache:
            _model_cache[model] = PiperVoice.load(path)
        return _model_cache[model]


def wav_duration_seconds(wav_bytes: bytes) -> float:
    try:
        with wave.open(io.BytesIO(wav_bytes), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return round(frames / rate, 3) if rate else 0.0
    except Exception:
        return 0.0


def synthesize_piper(voice: Voice, text: str, rate: float, volume: int) -> bytes:
    """Neural synthesis. rate: 1.0 = normal (>1 faster); volume: 0-100%."""
    model = _get_piper_voice(voice.model)
    length_scale = 1.0 / rate if rate > 0 else 1.0
    cfg = SynthesisConfig(length_scale=length_scale, volume=volume / 100.0)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        model.synthesize_wav(text, wf, syn_config=cfg)
    return buf.getvalue()


def synthesize_espeak(voice: Voice, text: str, rate: float, volume: int, pitch: int) -> bytes:
    """Formant synthesis via espeak-ng CLI: -s wpm, -a amplitude(0-200), -p pitch(0-99)."""
    if not espeak_available():
        raise ServiceError("espeak-ng is not installed")
    wpm = int(max(80, min(450, round(175 * rate))))
    amp = int(max(0, min(200, volume)))
    pitch = int(max(0, min(99, pitch)))
    with tempfile.TemporaryDirectory(prefix="tts_") as td:
        out_path = os.path.join(td, "out.wav")
        cmd = [
            "espeak-ng", "-v", voice.model,
            "-s", str(wpm), "-a", str(amp), "-p", str(pitch),
            "-w", out_path, text,
        ]
        with _espeak_lock:
            proc = subprocess.run(cmd, capture_output=True, timeout=60)
        if proc.returncode != 0 or not os.path.exists(out_path):
            err = proc.stderr.decode(errors="replace")[:300]
            raise ServiceError(f"espeak-ng failed: {err or 'unknown error'}")
        with open(out_path, "rb") as fh:
            return fh.read()
