from translator.translation_engine import translate_text as _translate_text
from translator.translation_engine import get_frequency_list as _get_frequency_list
from translator.pos_tagger import tag_text, get_pos_description
from translator.syntax_parser import parse_text
from translator import dictionary
from translator.dict_builder import build_all
from services.errors import ValidationError


def translate(text: str) -> dict:
    if not text:
        raise ValidationError("text is required")
    return _translate_text(text)


def pos_tag(text: str, lang: str = "en") -> dict:
    if not text:
        raise ValidationError("text is required")
    tagged = tag_text(text, lang=lang)
    return {
        "words": [{"word": w, "pos": p, "pos_desc": get_pos_description(p)} for w, p in tagged],
        "lang": lang,
    }


def syntax_parse(text: str, lang: str = "en") -> dict:
    if not text:
        raise ValidationError("text is required")
    results = parse_text(text, lang=lang)
    return {"results": results, "lang": lang}


def dict_list(limit: int = 100, offset: int = 0) -> dict:
    entries = dictionary.get_all(limit=limit, offset=offset)
    total = dictionary.count()
    return {"entries": entries, "total": total}


def dict_add(source: str, target: str, source_pos: str = "",
             target_pos: str = "") -> dict:
    if not source or not target:
        raise ValidationError("source and target are required")
    ok = dictionary.add_entry(source, target, source_pos, target_pos)
    return {"ok": ok}


def dict_search(q: str) -> dict:
    if not q:
        return {"entries": []}
    entries = dictionary.search(q)
    return {"entries": entries}


def dict_bulk_add(entries: list) -> dict:
    if not entries:
        raise ValidationError("entries list is required")
    count = dictionary.bulk_add(entries)
    return {"added": count}


def dict_bootstrap() -> dict:
    result = build_all()
    return {"added": result}


def dict_delete(entry_id) -> dict:
    if not entry_id:
        raise ValidationError("id is required")
    ok = dictionary.delete_entry_by_id(entry_id)
    return {"ok": ok}


def frequency_list(text: str) -> dict:
    if not text:
        raise ValidationError("text is required")
    freq = _get_frequency_list(text)
    return {"words": freq}


def export_txt(text: str, filename: str = "translation.txt") -> dict:
    if not text:
        raise ValidationError("text is required")
    result = _translate_text(text)
    freq = _get_frequency_list(text)

    lines = []
    lines.append("=" * 60)
    lines.append("EN → FR Translation")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Source text:")
    lines.append(text)
    lines.append("")
    lines.append("-" * 60)
    lines.append("Translation:")
    lines.append(result["translated_text"])
    lines.append("")
    lines.append("-" * 60)
    lines.append(f"Words: {result['word_count']} | Translated: {result['translated_count']} | Coverage: {result['stats']['coverage']}%")
    lines.append("")
    lines.append("-" * 60)
    lines.append("Word-by-word breakdown:")
    lines.append("")
    for w in result["words"]:
        if w["translated"]:
            lines.append(f"  {w['en']:20s} → {w['fr']:20s}  [{w['pos_en_desc']}]")
    lines.append("")
    lines.append("-" * 60)
    lines.append("Frequency list:")
    lines.append("")
    lines.append(f"  {'Word':20s} {'POS':6s} {'Freq':4s}  Translation")
    lines.append(f"  {'-'*20} {'-'*6} {'-'*4}  {'-'*20}")
    for w in freq[:50]:
        lines.append(f"  {w['en']:20s} {w['pos']:6s} {w['freq']:4d}  {w['fr']}")
    lines.append("")
    lines.append("=" * 60)

    if not filename.endswith(".txt"):
        filename += ".txt"

    return {"content": "\n".join(lines), "filename": filename}
