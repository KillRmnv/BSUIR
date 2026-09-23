"""Voice registry for the TTS subsystem (Variant 8: EN + FR, offline)."""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Voice:
    id: str
    name: str
    lang: str        # "fr" | "en"
    gender: str      # "F" | "M"
    engine: str      # "piper" | "espeak"
    model: str       # piper model stem (fr_FR-siwis-medium) or espeak voice (fr-fr)


# Neural offline voices (Piper, ~63 MB each, downloaded in the Dockerfile)
PIPER_VOICES: List[Voice] = [
    Voice("fr-siwis", "Siwis (French, female)", "fr", "F", "piper", "fr_FR-siwis-medium"),
    Voice("fr-tom", "Tom (French, male)", "fr", "M", "piper", "fr_FR-tom-medium"),
    Voice("en-amy", "Amy (English, female)", "en", "F", "piper", "en_US-amy-medium"),
    Voice("en-lessac", "Lessac (English, male)", "en", "M", "piper", "en_US-lessac-medium"),
]

# Fallback formant voices (espeak-ng, packaged with the image)
ESPEAK_VOICES: List[Voice] = [
    Voice("espeak-fr", "eSpeak French", "fr", "M", "espeak", "fr-fr"),
    Voice("espeak-en-us", "eSpeak English (US)", "en", "M", "espeak", "en-us"),
    Voice("espeak-en-gb", "eSpeak English (GB)", "en", "M", "espeak", "en-gb"),
]

ALL_VOICES: List[Voice] = PIPER_VOICES + ESPEAK_VOICES

DEFAULT_VOICE_BY_LANG: Dict[str, str] = {"fr": "fr-siwis", "en": "en-amy"}

MIN_RATE = 0.5
MAX_RATE = 2.0
DEFAULT_RATE = 1.0
MIN_VOLUME = 0
MAX_VOLUME = 100
DEFAULT_VOLUME = 100
MIN_PITCH = 0
MAX_PITCH = 99
DEFAULT_PITCH = 50

MAX_TEXT_CHARS = 4000


def get_voice(voice_id: Optional[str]) -> Optional[Voice]:
    if not voice_id:
        return None
    for v in ALL_VOICES:
        if v.id == voice_id:
            return v
    return None


def default_voice(lang: str) -> Voice:
    return get_voice(DEFAULT_VOICE_BY_LANG.get(lang, "en-amy"))


def espeak_fallback(lang: str) -> Voice:
    for v in ESPEAK_VOICES:
        if v.lang == lang:
            return v
    return ESPEAK_VOICES[0]
