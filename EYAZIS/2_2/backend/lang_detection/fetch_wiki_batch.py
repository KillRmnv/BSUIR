#!/usr/bin/env python3
"""Fetch Wikipedia REST API summaries for EN and FR, append to wiki_en.txt / wiki_fr.txt."""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

BASE_DIR = os.path.dirname(__file__)
TRAINING_DIR = os.path.join(BASE_DIR, "training")

EN_TOPICS = [
    "Artificial_intelligence", "Machine_learning", "Deep_learning", "Neural_network",
    "Natural_language_processing", "Computer_vision", "Robotics", "Quantum_computing",
    "Blockchain", "Cybersecurity", "Cloud_computing", "Internet_of_things",
    "Renewable_energy", "Climate_change", "Biodiversity", "Ecology",
    "Evolution", "DNA", "Cell_biology", "Neuroscience",
    "Cognitive_science", "Psychology", "Sociology", "Anthropology",
    "Economics", "Political_science", "International_relations", "Globalization",
    "Democracy", "Human_rights", "Education", "Public_health",
    "Epidemiology", "Immunology", "Virology", "Genetic_engineering",
    "Biotechnology", "Nanotechnology", "Materials_science", "Semiconductor",
    "Photonics", "Laser", "Superconductor", "Fusion_power",
    "Solar_power", "Wind_power", "Hydroelectricity", "Nuclear_fission",
    "Electric_vehicle", "Autonomous_car", "Space_exploration", "Mars",
    "International_Space_Station", "Telescope", "Black_hole", "Dark_matter",
    "Cosmology", "Galaxy", "Supernova", "Exoplanet",
    "Plate_tectonics", "Volcano", "Earthquake", "Tsunami",
    "Ocean", "Mountain", "Forest", "Desert",
    "River", "Lake", "Glacier", "Coral_reef",
    "Agriculture", "Forestry", "Fishery", "Mining",
    "Architecture", "Urban_planning", "Transportation", "Logistics",
    "Telecommunications", "5G", "Satellite", "GPS",
    "Internet", "World_Wide_Web", "Search_engine", "Social_media",
    "E-commerce", "Digital_marketing", "Data_science", "Big_data",
    "Statistical_learning", "Reinforcement_learning", "Computer_graphics",
    "Image_processing", "Speech_recognition", "Optical_character_recognition",
    "Game_theory", "Cryptography", "Algorithm", "Data_structure",
    "Operating_system", "Database", "Compiler", "Software_engineering",
    "Agile_development", "DevOps", "Microservices", "API",
    "Programming_language", "Python", "Java", "C++",
    "JavaScript", "Rust", "Go", "Kotlin",
    "World_War_I", "World_War_II", "Cold_War", "Industrial_Revolution",
    "French_Revolution", "Renaissance", "Enlightenment", "Scientific_revolution",
    "Ancient_Egypt", "Ancient_Greece", "Roman_Empire", "Byzantine_Empire",
    "Ottoman_Empire", "Mongol_Empire", "British_Empire", "Colonialism",
    "Abolitionism", "Feminism", "Civil_rights_movement", "Decolonization",
    "United_Nations", "European_Union", "NATO", "World_Trade_Organization",
    "International Monetary Fund", "World_Bank", "G20", "BRICS",
    "Philosophy_of_mind", "Ethics", "Epistemology", "Metaphysics",
    "Logic", "Aesthetics", "Political_philosophy", "Social_philosophy",
    "Existentialism", "Stoicism", "Pragmatism", "Utilitarianism",
    "Liberalism", "Conservatism", "Socialism", "Anarchism",
    "Quantum_mechanics", "Special_relativity", "General_relativity",
    "Thermodynamics", "Electromagnetism", "Optics", "Acoustics",
    "Fluid_dynamics", "Statistical_mechanics", "Condensed_matter_physics",
    "Particle_physics", "Nuclear_physics", "Astrophysics", "Plasma_physics",
    "Organic_chemistry", "Inorganic_chemistry", "Physical_chemistry",
    "Biochemistry", "Analytical_chemistry", "Polymer_chemistry",
    "Nanochemistry", "Environmental_chemistry", "Geochemistry",
    "Algebra", "Calculus", "Geometry", "Topology",
    "Number_theory", "Combinatorics", "Probability_theory", "Statistics",
    "Differential_equations", "Linear_algebra", "Abstract_algebra",
    "Mathematical_analysis", "Discrete_mathematics", "Cryptography",
    "Machine_learning_in_statistics", "Bayesian_inference", "Regression_analysis",
    "Classical_music", "Jazz", "Rock_music", "Electronic_music",
    "Hip_hop_music", "Pop_music", "Blues", "Country_music",
    "Opera", "Ballet", "Theater", "Dance",
    "Painting", "Sculpture", "Photography", "Film",
    "Literature", "Poetry", "Novel", "Short_story",
    "Architecture", "Interior_design", "Fashion_design", "Graphic_design",
    "Animation", "Video_game", "Virtual_reality", "Augmented_reality",
    "Artificial_intelligence_in_art", "Digital_art", "Generative_art", "Net_art",
]

FR_TOPICS = [
    "Intelligence_artificielle", "Apprentissage_automatique", "Apprentissage_profond",
    "Réseau_de_neurones", "Traitement_du_langage_naturel", "Vision_par_ordinateur",
    "Robotique", "Informatique_quantique", "Blockchain", "Cybersécurité",
    "Informatique_en_nuage", "Internet_des_objets", "Énergie_renouvelable",
    "Changement_climatique", "Biodiversité", "Écologie", "Évolution",
    "ADN", "Biologie_cellulaire", "Neurosciences", "Sciences_cognitives",
    "Psychologie", "Sociologie", "Anthropologie", "Économie",
    "Science_politique", "Relations_internationales", "Mondialisation",
    "Démocratie", "Droits_de_l'homme", "Éducation", "Santé_publique",
    "Épidémiologie", "Immunologie", "Virologie", "Génie_génétique",
    "Biotechnologie", "Nanotechnologie", "Science_des_matériaux", "Semiconducteur",
    "Photonique", "Laser", "Supraconducteur", "Fusion_nucléaire",
    "Énergie_solaire", "Énergie_éolienne", "Hydroélectricité", "Fission_nucléaire",
    "Véhicule_électrique", "Véhicule_autonome", "Exploration_spatiale", "Mars",
    "Station spatiale_internationale", "Téléscope", "Trou_noir", "Matière_sombre",
    "Cosmologie", "Galaxie", "Supernova", "Exoplanète",
    "Tectonique_des_plaques", "Volcan", "Séisme", "Tsunami",
    "Océan", "Montagne", "Forêt", "Désert",
    "Rivière", "Lac", "Glacier", "Récif_corallien",
    "Agriculture", "Sylviculture", "Pêche", "Exploitation_minière",
    "Architecture", "Urbanisme", "Transport", "Logistique",
    "Télécommunications", "5G", "Satellite", "GPS",
    "Internet", "World_Wide_Web", "Moteur_de_recherche", "Réseau_social",
    "Commerce_électronique", "Marketing_numérique", "Science_des_données",
    "Big_data", "Apprentissage_statistique", "Apprentissage_par_renforcement",
    "Informatique_graphique", "Traitement_d'image", "Reconnaissance_vocale",
    "Reconnaissance_optique_de_caractères", "Théorie_des_jeux", "Cryptographie",
    "Algorithme", "Structure_de_données", "Système_d'exploitation",
    "Base_de_données", "Compilateur", "Génie_logiciel",
    "Développement_agile", "DevOps", "Microservices", "API",
    "Langage_de_programmation", "Python", "Java", "C++",
    "JavaScript", "Rust", "Go", "Kotlin",
    "Première_Guerre_mondiale", "Seconde_Guerre_mondiale", "Guerre_froide",
    "Révolution_industrielle", "Révolution_française", "Renaissance",
    "Lumières", "Révolution_scientifique", "Égypte_antique",
    "Grèce_antique", "Empire_romain", "Empire_byzantin",
    "Empire_ottoman", "Empire_mongol", "Empire_britannique", "Colonialisme",
    "Abolitionnisme", "Féminisme", "Mouvement_des_droits_civiques",
    "Décolonisation", "Nations_unies", "Union_européenne", "OTAN",
    "Organisation_mondiale_du_commerce", "Fonds_monétaire_international",
    "Banque_mondiale", "G20", "BRICS",
    "Philosophie_de_l'esprit", "Éthique", "Épistémologie", "Métaphysique",
    "Logique", "Esthétique", "Philosophie_politique", "Philosophie_sociale",
    "Existentialisme", "Stoïcisme", "Pragmatisme", "Utilitarisme",
    "Libéralisme", "Conservatisme", "Socialisme", "Anarchisme",
    "Mécanique_quantique", "Relativité_restreinte", "Relativité_générale",
    "Thermodynamique", "Électromagnétisme", "Optique", "Acoustique",
    "Mécanique_des_fluides", "Mécanique_statistique", "Physique_de_la_matière_condensée",
    "Physique_des_particules", "Physique_nucléaire", "Astrophysique", "Physique_du_plasma",
    "Chimie_organique", "Chimie_inorganique", "Chimie_physique",
    "Biochimie", "Chimie_analytique", "Chimie_des_polymères",
    "Nanochimie", "Chimie_environnementale", "Géochimie",
    "Algèbre", "Analyse", "Géométrie", "Topologie",
    "Théorie_des_nombres", "Combinatoire", "Théorie_des_probabilités", "Statistiques",
    "Équations_différentielles", "Algèbre_linéaire", "Algèbre_abstraite",
    "Analyse_mathématique", "Mathématiques_discrètes",
    "Musique_classique", "Jazz", "Rock", "Musique_électronique",
    "Hip-hop", "Pop", "Blues", "Country",
    "Opéra", "Ballet", "Théâtre", "Danse",
    "Peinture", "Sculpture", "Photographie", "Cinéma",
    "Littérature", "Poésie", "Roman", "Nouvelle",
    "Architecture", "Design_d'intérieur", "Mode", "Design_graphique",
    "Animation", "Jeu_vidéo", "Réalité_virtuelle", "Réalité_augmentée",
    "Intelligence_artificielle_en_art", "Art_numérique", "Art_génératif",
]

WIKI_EN = "https://en.wikipedia.org/api/rest_v1/page/summary/"
WIKI_FR = "https://fr.wikipedia.org/api/rest_v1/page/summary/"


def fetch_summary(lang: str, title: str) -> str:
    url = WIKI_EN if lang == "en" else WIKI_FR
    encoded = urllib.parse.quote(title.replace(" ", "_"), safe="")
    full_url = url + encoded
    req = urllib.request.Request(full_url, headers={"User-Agent": "LangDetectBot/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("extract", "")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 5 * (attempt + 1)
                print(f"  rate limited, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                print(f"  SKIP {title}: {e}")
                return ""
        except Exception as e:
            print(f"  SKIP {title}: {e}")
            return ""
    print(f"  SKIP {title}: rate limited after 3 retries")
    return ""


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    target_per_lang = int(sys.argv[1]) if len(sys.argv) > 1 else 200

    for lang, topics, wiki_base in [
        ("en", EN_TOPICS, WIKI_EN),
        ("fr", FR_TOPICS, WIKI_FR),
    ]:
        out_path = os.path.join(TRAINING_DIR, f"wiki_{lang}.txt")
        existing = set()
        if os.path.exists(out_path):
            with open(out_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        existing.add(line[:80])

        collected = []
        total_chars = 0
        for i, topic in enumerate(topics):
            if total_chars >= target_per_lang * 1000:
                break
            print(f"[{lang}] {i+1}/{len(topics)}: {topic} ... ", end="", flush=True)
            text = fetch_summary(lang, topic)
            if text:
                text = clean(text)
                prefix = text[:80]
                if prefix not in existing:
                    collected.append(text)
                    existing.add(prefix)
                    total_chars += len(text)
                    print(f"{len(text)} chars (total {total_chars})")
                else:
                    print("duplicate, skip")
            else:
                print("empty, skip")
            time.sleep(1.0)

        with open(out_path, "a", encoding="utf-8") as f:
            for t in collected:
                f.write(t + "\n\n")

        print(f"\n{lang}: appended {len(collected)} paragraphs, {total_chars} chars")
        print(f"Total in file: {total_chars} chars")


if __name__ == "__main__":
    main()
