"""Offline speech-to-text engines: Vosk (Kaldi) for EN/FR command recognition."""
import io
import os
import threading
import wave

import numpy as np

from services.errors import ServiceError

try:
    import vosk
    vosk.SetLogLevel(-1)
except ImportError:  # optional dependency (dev host without vosk)
    vosk = None

MODEL_DIR = os.environ.get(
    "VOSK_MODEL_DIR",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vosk_models"),
)

MODEL_BY_LANG = {
    "en": "vosk-model-small-en-us-0.15",
    "fr": "vosk-model-small-fr-0.22",
}

SAMPLE_RATE = 16000
MAX_AUDIO_SECONDS = 30

_model_lock = threading.Lock()
_model_cache: dict = {}


def vosk_available() -> bool:
    return vosk is not None


def model_path(lang: str) -> str:
    name = MODEL_BY_LANG.get(lang)
    if not name:
        return ""
    return os.path.join(MODEL_DIR, name)


def model_present(lang: str) -> bool:
    path = model_path(lang)
    return bool(path) and os.path.isdir(path) and os.path.exists(os.path.join(path, "am"))


def status() -> dict:
    return {
        "vosk": {
            "available": vosk_available(),
            "model_dir": MODEL_DIR,
            "models": {lang: model_present(lang) for lang in MODEL_BY_LANG},
        },
        "sample_rate": SAMPLE_RATE,
        "max_audio_seconds": MAX_AUDIO_SECONDS,
    }


def _get_model(lang: str):
    if not vosk_available():
        raise ServiceError("vosk is not installed")
    if lang not in MODEL_BY_LANG:
        raise ServiceError(f"unsupported language: {lang}")
    path = model_path(lang)
    if not model_present(lang):
        raise ServiceError(f"Vosk model not found for '{lang}': {path}")
    with _model_lock:
        if lang not in _model_cache:
            _model_cache[lang] = vosk.Model(path)
        return _model_cache[lang]


def wav_to_pcm16(wav_bytes: bytes, target_rate: int = SAMPLE_RATE) -> bytes:
    """Decode WAV to mono int16 PCM at target_rate (linear resample)."""
    try:
        with wave.open(io.BytesIO(wav_bytes), "rb") as wf:
            rate = wf.getframerate()
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            frames = wf.readframes(wf.getnframes())
    except wave.Error as e:
        raise ServiceError(f"invalid WAV: {e}") from e

    if not frames or not rate:
        raise ServiceError("empty audio")

    if sampwidth == 2:
        x = np.frombuffer(frames, dtype=np.int16).astype(np.float64)
    elif sampwidth == 1:
        x = (np.frombuffer(frames, dtype=np.uint8).astype(np.float64) - 128.0) * 256.0
    elif sampwidth == 4:
        x = np.frombuffer(frames, dtype=np.int32).astype(np.float64) / 65536.0
    else:
        raise ServiceError(f"unsupported sample width: {sampwidth}")

    if channels > 1:
        usable = (len(x) // channels) * channels
        x = x[:usable].reshape(-1, channels).mean(axis=1)

    if rate != target_rate and len(x) > 1:
        n_out = max(1, int(len(x) * target_rate / rate))
        idx = np.linspace(0.0, len(x) - 1, n_out)
        x = np.interp(idx, np.arange(len(x), dtype=np.float64), x)

    x = np.clip(x, -32768.0, 32767.0).astype(np.int16)
    return x.tobytes()


def pcm_duration_seconds(pcm: bytes) -> float:
    return round(len(pcm) / (2.0 * SAMPLE_RATE), 3)


def recognize_pcm(lang: str, pcm: bytes, sample_rate: int = SAMPLE_RATE,
                  words=None) -> str:
    """Run Vosk on mono int16 PCM; returns lowercased recognized text.

    words: optional vocabulary restriction (JSON list) — dramatically
    improves accuracy for short command words (help/aide/…).
    """
    import json
    model = _get_model(lang)
    with _model_lock:
        if words:
            rec = vosk.KaldiRecognizer(model, sample_rate, json.dumps(list(words)))
        else:
            rec = vosk.KaldiRecognizer(model, sample_rate)
        rec.AcceptWaveform(pcm)
        result = json.loads(rec.FinalResult())
    return (result.get("text") or "").strip()


def recognize_wav(lang: str, wav_bytes: bytes, words=None) -> str:
    pcm = wav_to_pcm16(wav_bytes)
    if pcm_duration_seconds(pcm) > MAX_AUDIO_SECONDS:
        raise ServiceError(f"audio is too long (max {MAX_AUDIO_SECONDS}s)")
    return recognize_pcm(lang, pcm, words=words)


def wav_to_pcm_safe(wav_bytes: bytes) -> bytes:
    """Decode + duration-check; shared by dual-pass recognition."""
    pcm = wav_to_pcm16(wav_bytes)
    if pcm_duration_seconds(pcm) > MAX_AUDIO_SECONDS:
        raise ServiceError(f"audio is too long (max {MAX_AUDIO_SECONDS}s)")
    return pcm
