"""TTS service: validation, language detection, engine dispatch, metrics."""
import time
from typing import Optional

from lang_detection.lang_methods import classify_text_all
from services.errors import ValidationError, ServiceError
from tts import engines, normalize, voices
from tts.voices import (
    DEFAULT_PITCH,
    DEFAULT_RATE,
    DEFAULT_VOLUME,
    MAX_PITCH,
    MAX_RATE,
    MAX_TEXT_CHARS,
    MAX_VOLUME,
    MIN_PITCH,
    MIN_RATE,
    MIN_VOLUME,
    Voice,
)


def status() -> dict:
    return {
        "piper": {
            "available": engines.piper_available(),
            "model_dir": engines.MODEL_DIR,
            "models": {v.model: engines.model_present(v.model) for v in voices.PIPER_VOICES},
        },
        "espeak": {"available": engines.espeak_available()},
        "max_text_chars": MAX_TEXT_CHARS,
    }


def list_voices() -> dict:
    items = []
    for v in voices.ALL_VOICES:
        if v.engine == "piper":
            available = engines.model_present(v.model)
        else:
            available = engines.espeak_available()
        items.append({
            "id": v.id,
            "name": v.name,
            "lang": v.lang,
            "gender": v.gender,
            "engine": v.engine,
            "model": v.model,
            "available": available,
        })
    return {"voices": items, "default_by_lang": voices.DEFAULT_VOICE_BY_LANG}


def detect_lang(text: str) -> dict:
    text = text.strip()
    if not text:
        raise ValidationError("text is required")
    try:
        result = classify_text_all(text)
    except RuntimeError as e:
        raise ServiceError(str(e))
    lang = result.get("lang", "en")
    return {
        "lang": lang,
        "agreed": result.get("agreed"),
        "elapsed_ms": result.get("elapsed_ms"),
        "default_voice": voices.DEFAULT_VOICE_BY_LANG.get(lang),
    }


def _clamp(value, lo, hi, default):
    try:
        v = type(default)(value)
    except (TypeError, ValueError):
        return default
    return max(lo, min(hi, v))


def _resolve_voice(voice_id: Optional[str], lang: Optional[str],
                   engine: Optional[str]) -> Voice:
    if voice_id:
        voice = voices.get_voice(voice_id)
        if voice is None:
            raise ValidationError(f"unknown voice: {voice_id}")
        if engine and voice.engine != engine:
            # keep requested engine + language of the chosen voice
            for alt in voices.ALL_VOICES:
                if alt.engine == engine and alt.lang == voice.lang and alt.id != voice.id:
                    return alt
            raise ValidationError(f"voice '{voice_id}' is not available for engine '{engine}'")
        return voice
    if lang is None:
        lang = "fr"  # variant 8 default language
    if lang not in ("fr", "en"):
        raise ValidationError("lang must be 'fr' or 'en'")
    if engine == "espeak":
        return voices.espeak_fallback(lang)
    if engine == "piper":
        default = voices.default_voice(lang)
        if engines.model_present(default.model):
            return default
        return voices.espeak_fallback(lang)
    default = voices.default_voice(lang)
    if engines.model_present(default.model):
        return default
    return voices.espeak_fallback(lang)


def synthesize(text: str, voice_id: Optional[str] = None, lang: Optional[str] = None,
               rate=DEFAULT_RATE, volume=DEFAULT_VOLUME, pitch=DEFAULT_PITCH,
               engine: Optional[str] = None) -> dict:
    normalized = normalize.normalize_text(text or "")
    if not normalized:
        raise ValidationError("text is required")
    if len(normalized) > MAX_TEXT_CHARS:
        raise ValidationError(f"text is too long (max {MAX_TEXT_CHARS} characters)")

    rate = _clamp(rate, MIN_RATE, MAX_RATE, DEFAULT_RATE)
    volume = _clamp(volume, MIN_VOLUME, MAX_VOLUME, DEFAULT_VOLUME)
    pitch = _clamp(pitch, MIN_PITCH, MAX_PITCH, DEFAULT_PITCH)

    voice = _resolve_voice(voice_id, lang, engine)

    # Fallback: requested piper voice but its model is missing -> espeak
    if voice.engine == "piper" and not engines.model_present(voice.model):
        voice = voices.espeak_fallback(voice.lang)

    started = time.perf_counter()
    if voice.engine == "piper":
        audio = engines.synthesize_piper(voice, normalized, rate, volume)
    else:
        audio = engines.synthesize_espeak(voice, normalized, rate, volume, pitch)
    elapsed_ms = round((time.perf_counter() - started) * 1000.0, 1)

    return {
        "audio": audio,
        "voice": voice.id,
        "engine": voice.engine,
        "lang": voice.lang,
        "rate": rate,
        "volume": volume,
        "pitch": pitch if voice.engine == "espeak" else None,
        "normalized": normalized,
        "chars": len(normalized),
        "bytes": len(audio),
        "duration_s": engines.wav_duration_seconds(audio),
        "elapsed_ms": elapsed_ms,
    }
