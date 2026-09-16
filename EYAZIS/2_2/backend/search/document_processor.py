import re
import math
import html as html_module
from collections import Counter
from typing import List, Dict, Tuple, Set
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

STEMMER = PorterStemmer()
STOP_WORDS_EN = set(stopwords.words('english'))
STOP_WORDS_FR = set(stopwords.words('french'))
FR_EXTRA = "àâäéèêëîïôöùûüçœæÿ"
VOCAB: Dict[str, int] = {}
IDF: Dict[str, float] = {}


def clean_text(text: str, lang: str = 'en') -> List[str]:
    text = text.lower()
    if lang == 'fr':
        text = re.sub(f'[^a-z{FR_EXTRA}\s]', '', text)
        tokens = text.split()
        tokens = [t for t in tokens if t not in STOP_WORDS_FR and len(t) > 1]
    else:
        text = re.sub(r'[^a-z\s]', '', text)
        tokens = text.split()
        tokens = [t for t in tokens if t not in STOP_WORDS_EN and len(t) > 1]
        tokens = [STEMMER.stem(t) for t in tokens]
    return tokens


def build_vocabulary(documents: List[str], lang: str = 'en', langs: List[str] = None) -> Dict[str, int]:
    global VOCAB
    doc_freq = Counter()
    for i, doc in enumerate(documents):
        doc_lang = langs[i] if langs else lang
        tokens = set(clean_text(doc, doc_lang))
        for token in tokens:
            doc_freq[token] += 1
    sorted_words = sorted(doc_freq.keys())
    VOCAB = {word: idx for idx, word in enumerate(sorted_words)}
    return VOCAB


def compute_idf(documents: List[str], lang: str = 'en', langs: List[str] = None) -> Dict[str, float]:
    global IDF
    n = len(documents)
    doc_freq = Counter()
    for i, doc in enumerate(documents):
        doc_lang = langs[i] if langs else lang
        tokens = set(clean_text(doc, doc_lang))
        for token in tokens:
            doc_freq[token] += 1
    IDF = {word: math.log(n / (freq + 1)) + 1 for word, freq in doc_freq.items()}
    return IDF


def expand_vocabulary(new_texts: List[str], all_corpus_texts: List[str],
                      load_vocab_fn, load_idf_fn, save_vocab_fn, save_idf_fn,
                      lang: str = 'en') -> Dict[str, int]:
    """Incrementally extend the global VOCAB/IDF without re-indexing existing words.

    1. Load existing vocab+IDF from DB (preserving old word->index mappings).
    2. Add only genuinely new words, appending indices after existing ones.
    3. Recompute IDF over the full corpus (old + new texts).
    4. Persist to DB.
    """
    global VOCAB, IDF

    existing_vocab = load_vocab_fn() or {}
    next_idx = max(existing_vocab.values(), default=-1) + 1

    new_tokens = set()
    for text in new_texts:
        new_tokens.update(clean_text(text, lang))

    extended = dict(existing_vocab)
    for token in sorted(new_tokens):
        if token not in extended:
            extended[token] = next_idx
            next_idx += 1

    VOCAB = extended
    save_vocab_fn(VOCAB)

    compute_idf(all_corpus_texts, lang)
    save_idf_fn(IDF)

    return VOCAB


def vectorize_text(text: str) -> List[float]:
    tokens = clean_text(text)
    tf = Counter(tokens)
    dim = len(VOCAB)
    vector = [0.0] * dim
    for token, count in tf.items():
        if token in VOCAB:
            idx = VOCAB[token]
            tf_val = 1 + math.log(count) if count > 0 else 0
            idf_val = IDF.get(token, math.log(10) + 1)
            vector[idx] = tf_val * idf_val
    norm = math.sqrt(sum(v * v for v in vector))
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector


def vectorize_text_with_dim(text: str, dim: int, lang: str = 'en') -> List[float]:
    tokens = clean_text(text, lang)
    tf = Counter(tokens)
    vector = [0.0] * dim
    for token, count in tf.items():
        if token in VOCAB:
            idx = VOCAB[token]
            if idx < dim:
                tf_val = 1 + math.log(count) if count > 0 else 0
                idf_val = IDF.get(token, math.log(10) + 1)
                vector[idx] = tf_val * idf_val
    norm = math.sqrt(sum(v * v for v in vector))
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector


def get_vocab_size() -> int:
    return len(VOCAB)


def get_query_terms(query: str, lang: str = 'en') -> List[str]:
    """Stemmed query tokens that actually contribute to the vector
    (present in VOCAB/IDF, i.e. not stop-words and not OOV)."""
    return [t for t in clean_text(query, lang) if t in VOCAB or t in IDF]


def highlight_terms(text: str, terms: Set[str], lang: str = 'en') -> Tuple[str, List[str]]:
    """Escape text and wrap occurrences of `terms` (matched by stemmed form) in <mark>.
    Returns (html, matched_terms)."""
    escaped = html_module.escape(text)
    pattern = re.compile(r"[A-Za-z0-9']+")
    out = []
    last = 0
    matched = []
    seen = set()
    for m in pattern.finditer(escaped):
        word = m.group(0)
        if lang == 'fr':
            stem = word.lower().strip("'")
        else:
            stem = STEMMER.stem(word.lower().strip("'"))
        if stem in terms:
            if stem not in seen:
                seen.add(stem)
                matched.append(stem)
            out.append(escaped[last:m.start()])
            out.append(f"<mark>{word}</mark>")
        else:
            out.append(escaped[last:m.end()])
        last = m.end()
    out.append(escaped[last:])
    return "".join(out), matched


def highlight_snippet(
    content: str,
    terms: Set[str],
    max_len: int = 500,
    context: int = 160,
    lang: str = 'en',
) -> Tuple[str, List[str]]:
    """Build a highlighted snippet of `content` around the first token that matches `terms`.
    If nothing matches, take the plain prefix. Returns (html, matched_terms)."""
    first_span = None
    for m in re.finditer(r"[A-Za-z0-9']+", content):
        if lang == 'fr':
            stem = m.group(0).lower().strip("'")
        else:
            stem = STEMMER.stem(m.group(0).lower().strip("'"))
        if stem in terms:
            first_span = m.span()
            break

    if first_span is None:
        snippet = content[:max_len]
    else:
        start, end = first_span
        s = max(0, start - context)
        e = min(len(content), end + context)
        snippet = ("…" if s > 0 else "") + content[s:e] + ("…" if e < len(content) else "")
        if len(snippet) > max_len:
            snippet = snippet[:max_len] + "…"

    return highlight_terms(snippet, terms, lang)


def extract_keywords(text: str, top_k: int = 5, lang: str = 'en') -> List[str]:
    tokens = clean_text(text, lang)
    tf = Counter(tokens)
    scored = []
    for token, count in tf.items():
        tf_val = 1 + math.log(count) if count > 0 else 0
        idf_val = IDF.get(token, 1.0)
        scored.append((token, tf_val * idf_val))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [word for word, _ in scored[:top_k]]


def generate_summary(text: str, top_k: int = 3, min_sentence_len: int = 4, lang: str = 'en') -> str:
    """Extractive summary: pick the top-K sentences by summed TF-IDF weight
    and return them in their original order. Empty if nothing qualifying."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    scored = []
    for i, sent in enumerate(sentences):
        tokens = clean_text(sent, lang)
        if len(tokens) < min_sentence_len:
            continue
        tf = Counter(tokens)
        weight = sum(
            (1 + math.log(tf[token])) * IDF.get(token, 1.0)
            for token in tf
        )
        scored.append((weight, i, sent.strip()))
    if not scored:
        return ""
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]
    top.sort(key=lambda x: x[1])
    return " ".join(s for _, _, s in top)
