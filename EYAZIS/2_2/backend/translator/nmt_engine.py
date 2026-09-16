"""
Neural Machine Translation using Helsinki-NLP/opus-mt-en-fr.
Lazy-loaded model (~305 MB, ~1.2 GB RAM).
"""
import time
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "Helsinki-NLP/opus-mt-en-fr"

_tokenizer = None
_model = None
_device = None
_loaded = False


def _load():
    """Load model and tokenizer once."""
    global _tokenizer, _model, _device, _loaded
    if _loaded:
        return
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _model = _model.to(_device)
    _model.eval()
    _loaded = True


def translate_text(text: str) -> dict:
    """Translate English text to French using NMT.
    Returns dict with translated_text, method, model, word_count, processing_time."""
    if not text or not text.strip():
        return {"translated_text": "", "method": "nmt", "model": MODEL_NAME, "word_count": 0, "processing_time": 0}

    t0 = time.time()
    _load()

    # Split into sentences for better quality
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(text.strip())

    translations = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        inputs = _tokenizer(sent, return_tensors="pt", padding=True,
                            truncation=True, max_length=512)
        inputs = {k: v.to(_device) for k, v in inputs.items()}
        with torch.no_grad():
            ids = _model.generate(**inputs, max_length=512, num_beams=4)
        translated = _tokenizer.batch_decode(ids, skip_special_tokens=True)[0]
        translations.append(translated)

    translated_text = " ".join(translations)
    word_count = len(text.split())
    elapsed = round(time.time() - t0, 4)

    return {
        "translated_text": translated_text,
        "method": "nmt",
        "model": MODEL_NAME,
        "word_count": word_count,
        "processing_time": elapsed,
    }


def is_available() -> bool:
    """Check if the model can be loaded."""
    try:
        import transformers
        import torch
        import sentencepiece
        return True
    except ImportError:
        return False
