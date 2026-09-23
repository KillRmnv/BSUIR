"""
Seed the translation dictionary to >= 30 000 entries.

Sources (all local, already present in the Docker image):
  1. Project seed lists: COMMON_WORDS (1197), COMMON_TRANSLATIONS (747),
     PHRASE_PAIRS (163) — curated CS/literature domain terms, freq 10.
  2. English WordNet x French OMW/WOLF (NLTK omw-1.4): aligned by synset,
     POS comes from the synset (n/v/a/s/r -> Penn tag + pos_group), freq 1.
     Single-token EN lemmas -> words; multiword lemmas are skipped
     (curated PHRASE_PAIRS already cover phrases).
  3. FreeDict eng-fra TEI (optional, only if count still < TARGET):
     file translator/data/eng-fra.tei, no POS -> pos_group 'other'.

Idempotent: skips entirely when count(*) >= TARGET_ROWS.
Run: python translator/seed_dictionary.py  (start.sh does this after migrate)
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nltk.corpus import wordnet as wn

from translator import dictionary
from translator.common_words import COMMON_WORDS
from translator.dict_builder import COMMON_TRANSLATIONS, PHRASE_PAIRS

TARGET_ROWS = 30000
_BATCH_NOTE = "seed uses on_conflict='skip': existing user/bootstrap rows are kept"

# WordNet POS -> (Penn source_pos, coarse French target_pos)
_WN_POS = {
    "n": ("NN", "NC"),
    "v": ("VB", "V"),
    "a": ("JJ", "ADJ"),
    "s": ("JJ", "ADJ"),
    "r": ("RB", "ADV"),
}

_WORD_RE = re.compile(r"^[a-z][a-z'\-]*$")

# ── Source 1: project seed lists ─────────────────────────────────────

def _pairs_from_seed_lists() -> tuple:
    """Union of COMMON_WORDS + COMMON_TRANSLATIONS -> word entries,
    PHRASE_PAIRS -> phrase entries. Dedup keeps first occurrence."""
    words, seen = [], set()
    for en, (fr, en_pos, fr_pos) in COMMON_WORDS.items():
        if not en or not fr:
            continue
        key = (en, fr, (en_pos or "").upper())
        if key in seen:
            continue
        seen.add(key)
        words.append({
            "source": en, "target": fr,
            "source_pos": en_pos or "", "target_pos": fr_pos or "",
            "freq": 10,
        })
    for source, target, s_pos, t_pos in COMMON_TRANSLATIONS:
        if not source or not target:
            continue
        src = source.lower()
        key = (src, target.lower(), (s_pos or "").upper())
        if key in seen:
            continue
        seen.add(key)
        words.append({
            "source": src, "target": target,
            "source_pos": s_pos or "", "target_pos": t_pos or "",
            "freq": 10,
        })
    phrases = [
        {"source": en.lower(), "target": fr, "freq": 10}
        for en, fr in PHRASE_PAIRS if en and fr
    ]
    return words, phrases


# ── Source 2: English WordNet x French OMW/WOLF ──────────────────────

def _pairs_from_wordnet() -> list:
    """(en_lemma, fr_lemma, Penn pos) per synset that has French lemmas.
    Requires NLTK corpora wordnet + omw-1.4 (downloaded in the Dockerfile)."""
    words = []
    seen = set()
    for syn in wn.all_synsets():
        meta = _WN_POS.get(syn.pos())
        if meta is None:
            continue
        en_pos, fr_pos = meta
        try:
            fr_lemmas = syn.lemma_names("fra")
        except Exception:
            continue
        if not fr_lemmas:
            continue
        en_lemmas = syn.lemma_names()
        for en in en_lemmas:
            src = en.lower().replace("_", " ").strip()
            if not _WORD_RE.match(src):
                continue  # multiword / non-alpha -> skip (phrases curated separately)
            for fr in fr_lemmas:
                tgt = fr.lower().strip()
                if not tgt or not _WORD_RE.match(tgt.replace(" ", "")):
                    continue
                key = (src, tgt, en_pos)
                if key in seen:
                    continue
                seen.add(key)
                words.append({
                    "source": src, "target": tgt,
                    "source_pos": en_pos, "target_pos": fr_pos,
                    "freq": 1,
                })
    return words


# ── Source 3: FreeDict TEI (fallback, file must be vendored) ─────────

_FREE_DICT_PATH = os.path.join(os.path.dirname(__file__), "data", "eng-fra.tei")
_ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.S)
_ORTH_RE = re.compile(r"<orth>(.*?)</orth>", re.S)
_TRANS_RE = re.compile(r'<cit type="trans">\s*<quote>(.*?)</quote>', re.S)


def _pairs_from_freedict() -> tuple:
    """Parse FreeDict eng-fra TEI. No POS in entries -> source_pos ''."""
    if not os.path.exists(_FREE_DICT_PATH):
        return [], []
    with open(_FREE_DICT_PATH, encoding="utf-8") as fh:
        raw = fh.read()
    words, phrases = [], []
    for block in _ENTRY_RE.findall(raw):
        m = _ORTH_RE.search(block)
        if not m:
            continue
        src = m.group(1).strip().lower()
        trans = [t.strip().lower() for t in _TRANS_RE.findall(block) if t.strip()]
        if not src or not trans:
            continue
        if _WORD_RE.match(src):
            for tgt in trans[:3]:  # cap senses per headword
                words.append({
                    "source": src, "target": tgt,
                    "source_pos": "", "target_pos": "",
                    "freq": 1,
                })
        else:
            phrases.append({"source": src, "target": trans[0], "freq": 1})
    return words, phrases


# ── Entry point ──────────────────────────────────────────────────────

def seed(force: bool = False) -> dict:
    """Seed the dictionary. Skips when already at/above TARGET_ROWS."""
    try:
        current = dictionary.count()
    except Exception as e:
        return {"skipped": True, "reason": f"database unavailable: {e}"}

    if not force and current >= TARGET_ROWS:
        return {"skipped": True, "count": current, "target": TARGET_ROWS}

    # 1. Curated lists first (freq 10 wins over WordNet freq 1 on conflict)
    list_words, list_phrases = _pairs_from_seed_lists()
    added_lists = dictionary.bulk_add(list_words, on_conflict="skip")
    added_phrases = dictionary.bulk_add_phrases(list_phrases, on_conflict="skip")

    # 2. WordNet x French OMW/WOLF — the volume source
    added_wn = 0
    try:
        wn_words = _pairs_from_wordnet()
        added_wn = dictionary.bulk_add(wn_words, on_conflict="skip")
    except Exception as e:
        print(f"WARNING: WordNet seeding failed: {e}")

    total = dictionary.count()

    # 3. FreeDict fallback if we are still short of the target
    added_fd_words = added_fd_phrases = 0
    if total < TARGET_ROWS:
        fd_words, fd_phrases = _pairs_from_freedict()
        if fd_words or fd_phrases:
            added_fd_words = dictionary.bulk_add(fd_words, on_conflict="skip")
            added_fd_phrases = dictionary.bulk_add_phrases(fd_phrases, on_conflict="skip")
            total = dictionary.count()

    result = {
        "count": total,
        "target": TARGET_ROWS,
        "added_seed_lists": added_lists,
        "added_seed_phrases": added_phrases,
        "added_wordnet": added_wn,
        "added_freedict": added_fd_words,
        "added_freedict_phrases": added_fd_phrases,
        "note": _BATCH_NOTE,
    }
    if total < TARGET_ROWS:
        result["warning"] = (
            f"only {total} entries (< {TARGET_ROWS}): "
            "check wordnet/omw-1.4 corpora or vendor data/eng-fra.tei"
        )
        print(f"WARNING: {result['warning']}")
    else:
        print(f"Dictionary seeded: {total} entries (target {TARGET_ROWS})")
    return result


if __name__ == "__main__":
    print(seed())
