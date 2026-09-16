#!/usr/bin/env python3
"""
Fetch Wikipedia article summaries for EN and FR language detection training.
Uses the Wikipedia REST API (no extra packages needed).
"""
import urllib.request
import urllib.parse
import json
import os
import time

EN_TITLES = [
    "Artificial_intelligence",
    "Quantum_computing",
    "Climate_change",
    "Democracy",
    "Evolution",
    "Solar_system",
    "French_Revolution",
    "World_War_II",
    "Theory_of_relativity",
    "Genetics",
    "Ancient_Rome",
    "Photosynthesis",
    "Nanotechnology",
    "Economic_growth",
    "Volcanic_eruption",
    "Antibiotics",
    "Renaissance",
    "Artificial_satellite",
    "Electromagnetism",
    "Ocean",
    "Mathematics",
    "Philosophy",
    "Archaeology",
    "Astronomy",
    "Biology",
    "Chemistry",
    "Physics",
    "Geography",
    "Literature",
    "Music",
]

FR_TITLES = [
    "Intelligence_artificielle",
    "Informatique_quantique",
    "Changement_climatique",
    "Démocratie",
    "Évolution_(biologie)",
    "Système_solaire",
    "Révolution_française",
    "Seconde_Guerre_mondiale",
    "Théorie_de_la_relativité",
    "Génétique",
    "Rome_antique",
    "Photosynthèse",
    "Nanotechnologie",
    "Croissance_économique",
    "Éruption_volcanique",
    "Antibiotiques",
    "Renaissance",
    "Satellite_artificiel",
    "Électromagnétisme",
    "Océan",
    "Mathématiques",
    "Philosophie",
    "Archéologie",
    "Astronomie",
    "Biologie",
    "Chimie",
    "Physique",
    "Géographie",
    "Littérature",
    "Musique",
]


def fetch_summary(title: str, lang: str) -> str:
    """Fetch a Wikipedia article summary as plain text."""
    encoded_title = urllib.parse.quote(title, safe="")
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "EYAZIS-LangDetect/1.0 (educational project; contact: student@bsuir.by)"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("extract", "")
    except Exception as e:
        print(f"  WARNING: Failed to fetch {lang}/{title}: {e}")
        return ""


def fetch_all(lang: str, titles: list) -> str:
    """Fetch all summaries for a language, return combined text."""
    paragraphs = []
    for i, title in enumerate(titles):
        print(f"  [{lang}] Fetching {i+1}/{len(titles)}: {title}...")
        text = fetch_summary(title, lang)
        if text and len(text) > 50:
            paragraphs.append(text)
        time.sleep(0.5)  # rate limit
    return "\n\n".join(paragraphs)


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "training")
    os.makedirs(out_dir, exist_ok=True)

    print("Fetching English Wikipedia summaries...")
    en_text = fetch_all("en", EN_TITLES)
    en_path = os.path.join(out_dir, "wiki_en.txt")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_text)
    print(f"  Saved {len(en_text)} chars to {en_path}")

    print("Fetching French Wikipedia summaries...")
    fr_text = fetch_all("fr", FR_TITLES)
    fr_path = os.path.join(out_dir, "wiki_fr.txt")
    with open(fr_path, "w", encoding="utf-8") as f:
        f.write(fr_text)
    print(f"  Saved {len(fr_text)} chars to {fr_path}")

    print("Done.")


if __name__ == "__main__":
    main()
