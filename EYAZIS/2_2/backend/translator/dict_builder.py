"""
Build translation dictionary from parallel EN/FR corpora.
Uses sentence-level alignment from seed paragraphs, not frequency-rank alignment.
Also populates a phrase dictionary for multi-word expressions.
"""
import os
import sys
import re
from collections import Counter

from nltk.tokenize import sent_tokenize

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from translator import dictionary
from translator.pos_tagger import pos_tag_en
from lang_detection.lang_seeds import EN_TRAIN, FR_TRAIN, SEED_PARAGRAPHS

# Common EN→FR phrase translations (multi-word expressions)
PHRASE_PAIRS = [
    # Verbal phrases
    ("give up", "abandonner"), ("look for", "chercher"), ("find out", "découvrir"),
    ("set up", "établir"), ("carry out", "effectuer"), ("take place", "avoir lieu"),
    ("come up with", "proposer"), ("deal with", "traiter"), ("run out", "s'épuiser"),
    ("turn out", "s'avérer"), ("figure out", "comprendre"), ("point out", "souligner"),
    ("bring up", "élever"), ("call for", "demander"), ("end up", "finir par"),
    ("go on", "continuer"), ("hold on", "attendre"), ("keep up", "maintenir"),
    ("look out", "faire attention"), ("make up", "inventer"), ("pick up", "ramasser"),
    ("put off", "reporter"), ("set out", "partir"), ("take over", "prendre le relais"),
    # Prepositional phrases
    ("in order to", "pour"), ("as well as", "ainsi que"), ("in addition to", "en plus de"),
    ("on behalf of", "au nom de"), ("in front of", "devant"), ("because of", "à cause de"),
    ("instead of", "au lieu de"), ("according to", "selon"), ("apart from", "à part"),
    ("as far as", "en ce qui concerne"), ("by means of", "au moyen de"),
    ("in terms of", "en termes de"), ("at the same time", "en même temps"),
    ("for example", "par exemple"), ("for instance", "par exemple"),
    ("in fact", "en fait"), ("of course", "bien sûr"), ("so that", "pour que"),
    ("such as", "tel que"), ("up to", "jusqu'à"), ("as well", "aussi"),
    # CS-specific phrases
    ("machine learning", "apprentissage automatique"),
    ("deep learning", "apprentissage profond"),
    ("neural network", "réseau de neurones"),
    ("data structure", "structure de données"),
    ("operating system", "système d'exploitation"),
    ("file system", "système de fichiers"),
    ("user interface", "interface utilisateur"),
    ("source code", "code source"),
    ("object oriented", "orienté objet"),
    ("artificial intelligence", "intelligence artificielle"),
    ("natural language", "langage naturel"),
    ("computer science", "informatique"),
    ("web browser", "navigateur web"),
    ("memory allocation", "allocation de mémoire"),
    ("binary tree", "arbre binaire"),
    ("linked list", "liste chaînée"),
    ("hash table", "table de hachage"),
    ("search engine", "moteur de recherche"),
    ("cloud computing", "informatique en nuage"),
    ("big data", "méga données"),
    ("open source", "open source"),
    # Common literary / general phrases
    ("point of view", "point de vue"), ("state of the art", "de pointe"),
    ("in other words", "en d'autres termes"), ("on the other hand", "d'un autre côté"),
    ("as a result", "en conséquence"), ("in this case", "dans ce cas"),
    ("each other", "l'un l'autre"), ("more than", "plus que"),
    ("less than", "moins que"), ("rather than", "plutôt que"),
    ("not only", "non seulement"), ("whether or not", "que ce soit ou non"),
    # Existential / copula phrases
    ("there is", "il y a"), ("there are", "il y a"), ("there was", "il y avait"),
    ("there were", "il y avait"), ("there is no", "il n'y a pas"),
    ("it is", "c'est"), ("it was", "c'était"), ("it is not", "ce n'est pas"),
    ("this is", "c'est"), ("that is", "c'est"), ("this was", "c'était"),
    ("here is", "voici"), ("here are", "voici"),
    ("what is", "qu'est-ce que"), ("what are", "qu'est-ce que"),
    ("how is", "comment est"), ("how are", "comment vont"),
    ("where is", "où est"), ("where are", "où sont"),
    ("who is", "qui est"), ("who are", "qui sont"),
    ("when is", "quand est"), ("when are", "quand sont"),
    ("why is", "pourquoi est"), ("why are", "pourquoi sont"),
    ("i am", "je suis"), ("you are", "tu es"), ("he is", "il est"),
    ("she is", "elle est"), ("we are", "nous sommes"), ("they are", "ils sont"),
    ("i was", "j'étais"), ("you was", "tu étais"), ("he was", "il était"),
    ("she was", "elle était"), ("we was", "nous étions"), ("they was", "ils étaient"),
    ("i have", "j'ai"), ("you have", "tu as"), ("he has", "il a"),
    ("she has", "elle a"), ("we have", "nous avons"), ("they have", "ils ont"),
    ("i do", "je fais"), ("you do", "tu fais"), ("he does", "il fait"),
    ("she does", "elle fait"), ("we do", "nous faisons"), ("they do", "ils font"),
    ("i can", "je peux"), ("you can", "tu peux"), ("he can", "il peut"),
    ("she can", "elle peut"), ("we can", "nous pouvons"), ("they can", "ils peuvent"),
    ("i will", "je serai"), ("you will", "tu seras"), ("he will", "il sera"),
    ("she will", "elle sera"), ("we will", "nous serons"), ("they will", "ils seront"),
    ("i must", "je dois"), ("you must", "tu dois"), ("he must", "il doit"),
    ("she must", "elle doit"), ("we must", "nous devons"), ("they must", "ils doivent"),
    ("i should", "je devrais"), ("you should", "tu devrais"),
    ("he should", "il devrait"), ("she should", "elle devrait"),
    ("we should", "nous devrions"), ("they should", "ils devraient"),
    ("i would", "je voudrais"), ("you would", "tu voudrais"),
    ("he would", "il voudrait"), ("she would", "elle voudrait"),
    ("we would", "nous voudrions"), ("they would", "ils voudraient"),
    ("i could", "je pourrais"), ("you could", "tu pourrais"),
    ("he could", "il pourrait"), ("she could", "elle pourrait"),
    ("we could", "nous pourrions"), ("they could", "ils pourraient"),
]

# Common EN→FR word pairs for bootstrapping (expanded from original)
COMMON_TRANSLATIONS = [
    ("the", "le", "DT", "DET"), ("a", "un", "DT", "DET"),
    ("an", "un", "DT", "DET"),
    ("is", "est", "VBZ", "V"), ("am", "suis", "VBP", "V"),
    ("are", "êtes", "VBP", "V"), ("was", "étais", "VBD", "V"),
    ("were", "étions", "VBD", "V"),
    ("have", "avons", "VBP", "V"), ("has", "a", "VBZ", "V"), ("had", "avait", "VBD", "V"),
    ("will", "sera", "MD", "V"), ("can", "peut", "MD", "V"),
    ("could", "pourrait", "MD", "V"), ("would", "serait", "MD", "V"),
    ("should", "devrait", "MD", "V"), ("may", "peut", "MD", "V"),
    ("must", "doit", "MD", "V"), ("shall", "devra", "MD", "V"),
    ("might", "pourrait", "MD", "V"),
    # Irregular verb forms — all persons
    ("suis", "suis", "VBP", "V"), ("es", "es", "VBP", "V"), ("est", "est", "VBZ", "V"),
    ("sommes", "sommes", "VBP", "V"), ("êtes", "êtes", "VBP", "V"), ("sont", "sont", "VBP", "V"),
    ("étais", "étais", "VBD", "V"), ("était", "était", "VBD", "V"),
    ("étions", "étions", "VBD", "V"), ("étiez", "étiez", "VBD", "V"), ("étaient", "étaient", "VBD", "V"),
    ("ai", "ai", "VBP", "V"), ("as", "as", "VBP", "V"), ("a", "a", "VBZ", "V"),
    ("avons", "avons", "VBP", "V"), ("avez", "avez", "VBP", "V"), ("ont", "ont", "VBP", "V"),
    ("fais", "fais", "VBP", "V"), ("fait", "fait", "VBZ", "V"),
    ("faisons", "faisons", "VBP", "V"), ("faites", "faites", "VBP", "V"), ("font", "font", "VBP", "V"),
    ("vais", "vais", "VBP", "V"), ("vas", "vas", "VBP", "V"), ("va", "va", "VBZ", "V"),
    ("allons", "allons", "VBP", "V"), ("allez", "allez", "VBP", "V"), ("vont", "vont", "VBP", "V"),
    ("peux", "peux", "VBP", "V"), ("peut", "peut", "VBZ", "V"),
    ("pouvons", "pouvons", "VBP", "V"), ("pouvez", "pouvez", "VBP", "V"), ("peuvent", "peuvent", "VBP", "V"),
    ("serai", "serai", "VBP", "V"), ("seras", "seras", "VBP", "V"), ("sera", "sera", "VBZ", "V"),
    ("serons", "serons", "VBP", "V"), ("serez", "serez", "VBP", "V"), ("seront", "seront", "VBP", "V"),
    ("dois", "dois", "VBP", "V"), ("doit", "doit", "VBZ", "V"),
    ("devons", "devons", "VBP", "V"), ("devez", "devez", "VBP", "V"), ("doivent", "doivent", "VBP", "V"),
    ("devrai", "devrai", "VBP", "V"), ("devras", "devras", "VBP", "V"), ("devra", "devra", "VBZ", "V"),
    ("devrons", "devrons", "VBP", "V"), ("devrez", "devrez", "VBP", "V"), ("devront", "devront", "VBP", "V"),
    ("devrais", "devrais", "VBP", "V"), ("devrait", "devrait", "VBZ", "V"),
    ("devrions", "devrions", "VBP", "V"), ("devriez", "devriez", "VBP", "V"), ("devraient", "devraient", "VBP", "V"),
    ("voudrais", "voudrais", "VBP", "V"), ("voudrait", "voudrait", "VBZ", "V"),
    ("voudrions", "voudrions", "VBP", "V"), ("voudriez", "voudriez", "VBP", "V"), ("voudraient", "voudraient", "VBP", "V"),
    ("pourrais", "pourrais", "VBP", "V"), ("pourrait", "pourrait", "VBZ", "V"),
    ("pourrions", "pourrions", "VBP", "V"), ("pourriez", "pourriez", "VBP", "V"), ("pourraient", "pourraient", "VBP", "V"),
    ("and", "et", "CC", "CON"), ("or", "ou", "CC", "CON"),
    ("but", "mais", "CC", "CON"), ("not", "ne pas", "RB", "ADV"),
    ("in", "dans", "IN", "PRE"), ("on", "sur", "IN", "PRE"),
    ("at", "à", "IN", "PRE"), ("to", "à", "TO", "PRE"),
    ("for", "pour", "IN", "PRE"), ("with", "avec", "IN", "PRE"),
    ("from", "de", "IN", "PRE"), ("of", "de", "IN", "PRE"),
    ("by", "par", "IN", "PRE"), ("about", "à propos de", "IN", "PRE"),
    ("into", "dans", "IN", "PRE"), ("through", "à travers", "IN", "PRE"),
    ("during", "pendant", "IN", "PRE"), ("before", "avant", "IN", "PRE"),
    ("after", "après", "IN", "PRE"), ("above", "au-dessus de", "IN", "PRE"),
    ("below", "au-dessous de", "IN", "PRE"), ("between", "entre", "IN", "PRE"),
    ("under", "sous", "IN", "PRE"), ("over", "sur", "IN", "PRE"),
    ("this", "ce", "DT", "DET"), ("that", "ce", "DT", "DET"),
    ("these", "ces", "DT", "DET"), ("those", "ces", "DT", "DET"),
    ("it", "il", "PRP", "PRO"), ("he", "il", "PRP", "PRO"),
    ("she", "elle", "PRP", "PRO"), ("we", "nous", "PRP", "PRO"),
    ("they", "ils", "PRP", "PRO"), ("you", "vous", "PRP", "PRO"),
    ("i", "je", "PRP", "PRO"), ("me", "me", "PRP", "PRO"),
    ("my", "mon", "PRP$", "DET"), ("his", "son", "PRP$", "DET"),
    ("her", "sa", "PRP$", "DET"), ("our", "notre", "PRP$", "DET"),
    ("their", "leur", "PRP$", "DET"),
    ("what", "quoi", "WP", "PRO"), ("which", "lequel", "WDT", "PRO"),
    ("who", "qui", "WP", "PRO"), ("whom", "qui", "WP", "PRO"),
    ("where", "où", "WRB", "ADV"), ("when", "quand", "WRB", "ADV"),
    ("how", "comment", "WRB", "ADV"), ("why", "pourquoi", "WRB", "ADV"),
    ("if", "si", "IN", "CON"), ("because", "parce que", "IN", "CON"),
    ("although", "bien que", "IN", "CON"), ("while", "tandis que", "IN", "CON"),
    ("however", "cependant", "RB", "ADV"), ("also", "aussi", "RB", "ADV"),
    ("very", "très", "RB", "ADV"), ("here", "ici", "RB", "ADV"),
    ("there", "là", "RB", "ADV"),
    ("good", "bon", "JJ", "ADJ"), ("bad", "mauvais", "JJ", "ADJ"),
    ("big", "grand", "JJ", "ADJ"), ("small", "petit", "JJ", "ADJ"),
    ("new", "nouveau", "JJ", "ADJ"), ("old", "ancien", "JJ", "ADJ"),
    ("first", "premier", "JJ", "ADJ"), ("last", "dernier", "JJ", "ADJ"),
    ("long", "long", "JJ", "ADJ"), ("great", "grand", "JJ", "ADJ"),
    ("little", "petit", "JJ", "ADJ"), ("own", "propre", "JJ", "ADJ"),
    ("other", "autre", "JJ", "ADJ"), ("important", "important", "JJ", "ADJ"),
    ("different", "différent", "JJ", "ADJ"), ("large", "grand", "JJ", "ADJ"),
    ("high", "élevé", "JJ", "ADJ"), ("low", "bas", "JJ", "ADJ"),
    ("early", "tôt", "JJ", "ADJ"), ("young", "jeune", "JJ", "ADJ"),
    ("make", "faire", "VB", "V"), ("go", "aller", "VB", "V"),
    ("do", "faire", "VB", "V"), ("say", "dire", "VB", "V"),
    ("get", "obtenir", "VB", "V"), ("know", "savoir", "VB", "V"),
    ("take", "prendre", "VB", "V"), ("see", "voir", "VB", "V"),
    ("come", "venir", "VB", "V"), ("think", "penser", "VB", "V"),
    ("look", "regarder", "VB", "V"), ("want", "vouloir", "VB", "V"),
    ("give", "donner", "VB", "V"), ("use", "utiliser", "VB", "V"),
    ("find", "trouver", "VB", "V"), ("tell", "dire", "VB", "V"),
    ("ask", "demander", "VB", "V"), ("work", "travailler", "VB", "V"),
    ("seem", "sembler", "VB", "V"), ("feel", "sentir", "VB", "V"),
    ("try", "essayer", "VB", "V"), ("leave", "quitter", "VB", "V"),
    ("call", "appeler", "VB", "V"), ("need", "besoin", "VB", "V"),
    ("become", "devenir", "VB", "V"), ("keep", "garder", "VB", "V"),
    ("let", "laisser", "VB", "V"), ("begin", "commencer", "VB", "V"),
    ("show", "montrer", "VB", "V"), ("hear", "entendre", "VB", "V"),
    ("play", "jouer", "VB", "V"), ("run", "courir", "VB", "V"),
    ("move", "bouger", "VB", "V"), ("live", "vivre", "VB", "V"),
    ("believe", "croire", "VB", "V"), ("bring", "apporter", "VB", "V"),
    ("happen", "arriver", "VB", "V"), ("write", "écrire", "VB", "V"),
    ("provide", "fournir", "VB", "V"), ("sit", "asseoir", "VB", "V"),
    ("stand", "se tenir", "VB", "V"), ("lose", "perdre", "VB", "V"),
    ("pay", "payer", "VB", "V"), ("meet", "rencontrer", "VB", "V"),
    ("include", "inclure", "VB", "V"), ("continue", "continuer", "VB", "V"),
    ("set", "définir", "VB", "V"), ("learn", "apprendre", "VB", "V"),
    ("change", "changer", "VB", "V"), ("lead", "mener", "VB", "V"),
    ("understand", "comprendre", "VB", "V"), ("watch", "regarder", "VB", "V"),
    ("follow", "suivre", "VB", "V"), ("stop", "arrêter", "VB", "V"),
    ("create", "créer", "VB", "V"), ("speak", "parler", "VB", "V"),
    ("read", "lire", "VB", "V"), ("spend", "dépenser", "VB", "V"),
    ("grow", "grandir", "VB", "V"), ("open", "ouvrir", "VB", "V"),
    ("walk", "marcher", "VB", "V"), ("win", "gagner", "VB", "V"),
    ("offer", "offrir", "VB", "V"), ("remember", "se souvenir", "VB", "V"),
    ("love", "aimer", "VB", "V"), ("consider", "considérer", "VB", "V"),
    ("appear", "apparaître", "VB", "V"), ("buy", "acheter", "VB", "V"),
    ("wait", "attendre", "VB", "V"), ("serve", "servir", "VB", "V"),
    ("die", "mourir", "VB", "V"), ("send", "envoyer", "VB", "V"),
    ("expect", "attendre", "VB", "V"), ("build", "construire", "VB", "V"),
    ("stay", "rester", "VB", "V"), ("fall", "tomber", "VB", "V"),
    ("cut", "couper", "VB", "V"), ("reach", "atteindre", "VB", "V"),
    ("remain", "rester", "VB", "V"), ("suggest", "suggérer", "VB", "V"),
    ("raise", "élever", "VB", "V"), ("pass", "passer", "VB", "V"),
    ("sell", "vendre", "VB", "V"), ("require", "nécessiter", "VB", "V"),
    ("report", "rapporter", "VB", "V"), ("decide", "décider", "VB", "V"),
    ("develop", "développer", "VB", "V"), ("eat", "manger", "VB", "V"),
    ("put", "mettre", "VB", "V"),
    ("one", "un", "CD", "NUM"), ("two", "deux", "CD", "NUM"),
    ("three", "trois", "CD", "NUM"), ("many", "beaucoup", "JJ", "ADV"),
    ("some", "quelques", "DT", "DET"), ("all", "tous", "DT", "DET"),
    ("no", "aucun", "DT", "DET"),
    ("world", "monde", "NN", "NC"), ("time", "temps", "NN", "NC"),
    ("year", "année", "NN", "NC"), ("people", "personnes", "NNS", "NC"),
    ("way", "chemin", "NN", "NC"), ("day", "jour", "NN", "NC"),
    ("man", "homme", "NN", "NC"), ("woman", "femme", "NN", "NC"),
    ("child", "enfant", "NN", "NC"), ("life", "vie", "NN", "NC"),
    ("hand", "main", "NN", "NC"), ("part", "partie", "NN", "NC"),
    ("place", "endroit", "NN", "NC"), ("case", "cas", "NN", "NC"),
    ("week", "semaine", "NN", "NC"), ("company", "entreprise", "NN", "NC"),
    ("system", "système", "NN", "NC"), ("program", "programme", "NN", "NC"),
    ("question", "question", "NN", "NC"), ("government", "gouvernement", "NN", "NC"),
    ("number", "nombre", "NN", "NC"), ("night", "nuit", "NN", "NC"),
    ("point", "point", "NN", "NC"), ("home", "maison", "NN", "NC"),
    ("water", "eau", "NN", "NC"), ("room", "chambre", "NN", "NC"),
    ("mother", "mère", "NN", "NC"), ("area", "zone", "NN", "NC"),
    ("money", "argent", "NN", "NC"), ("story", "histoire", "NN", "NC"),
    ("fact", "fait", "NN", "NC"), ("month", "mois", "NN", "NC"),
    ("right", "droite", "NN", "NC"), ("study", "étude", "NN", "NC"),
    ("book", "livre", "NN", "NC"), ("eye", "œil", "NN", "NC"),
    ("job", "emploi", "NN", "NC"), ("word", "mot", "NN", "NC"),
    ("business", "entreprise", "NN", "NC"), ("issue", "problème", "NN", "NC"),
    ("side", "côté", "NN", "NC"), ("kind", "genre", "NN", "NC"),
    ("head", "tête", "NN", "NC"), ("house", "maison", "NN", "NC"),
    ("service", "service", "NN", "NC"), ("friend", "ami", "NN", "NC"),
    ("father", "père", "NN", "NC"), ("power", "pouvoir", "NN", "NC"),
    ("hour", "heure", "NN", "NC"), ("line", "ligne", "NN", "NC"),
    ("end", "fin", "NN", "NC"), ("member", "membre", "NN", "NC"),
    ("car", "voiture", "NN", "NC"), ("city", "ville", "NN", "NC"),
    ("community", "communauté", "NN", "NC"), ("name", "nom", "NN", "NC"),
    ("president", "président", "NN", "NC"), ("team", "équipe", "NN", "NC"),
    ("minute", "minute", "NN", "NC"), ("idea", "idée", "NN", "NC"),
    ("body", "corps", "NN", "NC"), ("information", "information", "NN", "NC"),
    ("river", "rivière", "NN", "NC"), ("computer", "ordinateur", "NN", "NC"),
    ("science", "science", "NN", "NC"), ("music", "musique", "NN", "NC"),
    ("art", "art", "NN", "NC"), ("language", "langue", "NN", "NC"),
    ("result", "résultat", "NN", "NC"), ("process", "processus", "NN", "NC"),
    ("research", "recherche", "NN", "NC"), ("data", "données", "NNS", "NC"),
    ("technology", "technologie", "NN", "NC"), ("student", "étudiant", "NN", "NC"),
    ("university", "université", "NN", "NC"), ("history", "histoire", "NN", "NC"),
    ("problem", "problème", "NN", "NC"), ("solution", "solution", "NN", "NC"),
    ("method", "méthode", "NN", "NC"), ("analysis", "analyse", "NN", "NC"),
    ("model", "modèle", "NN", "NC"), ("image", "image", "NN", "NC"),
    ("view", "vue", "NN", "NC"), ("level", "niveau", "NN", "NC"),
    ("experience", "expérience", "NN", "NC"), ("knowledge", "connaissance", "NN", "NC"),
    ("test", "test", "NN", "NC"), ("development", "développement", "NN", "NC"),
    ("product", "produit", "NN", "NC"), ("market", "marché", "NN", "NC"),
    ("position", "position", "NN", "NC"), ("interest", "intérêt", "NN", "NC"),
    ("century", "siècle", "NN", "NC"), ("society", "société", "NN", "NC"),
    ("nature", "nature", "NN", "NC"), ("table", "table", "NN", "NC"),
    ("school", "école", "NN", "NC"), ("state", "état", "NN", "NC"),
    ("country", "pays", "NN", "NC"), ("teacher", "enseignant", "NN", "NC"),
    ("education", "éducation", "NN", "NC"),
    ("branch", "branche", "NN", "NC"), ("data", "données", "NNS", "NC"),
    ("clear", "clair", "JJ", "ADJ"), ("possible", "possible", "JJ", "ADJ"),
    ("certain", "certain", "JJ", "ADJ"), ("following", "suivant", "JJ", "ADJ"),
    ("several", "plusieurs", "JJ", "ADJ"), ("current", "actuel", "JJ", "ADJ"),
    ("political", "politique", "JJ", "ADJ"), ("recent", "récent", "JJ", "ADJ"),
    ("medical", "médical", "JJ", "ADJ"), ("full", "plein", "JJ", "ADJ"),
    ("similar", "similaire", "JJ", "ADJ"), ("available", "disponible", "JJ", "ADJ"),
    ("common", "commun", "JJ", "ADJ"), ("major", "majeur", "JJ", "ADJ"),
    ("simple", "simple", "JJ", "ADJ"), ("natural", "naturel", "JJ", "ADJ"),
    ("significant", "significatif", "JJ", "ADJ"), ("hard", "dur", "JJ", "ADJ"),
    ("strong", "fort", "JJ", "ADJ"), ("true", "vrai", "JJ", "ADJ"),
    ("whole", "entier", "JJ", "ADJ"), ("free", "libre", "JJ", "ADJ"),
    ("better", "meilleur", "JJR", "ADJ"), ("special", "spécial", "JJ", "ADJ"),
    ("easy", "facile", "JJ", "ADJ"), ("red", "rouge", "JJ", "ADJ"),
    ("green", "vert", "JJ", "ADJ"), ("blue", "bleu", "JJ", "ADJ"),
    ("white", "blanc", "JJ", "ADJ"), ("black", "noir", "JJ", "ADJ"),
    ("now", "maintenant", "RB", "ADV"), ("then", "alors", "RB", "ADV"),
    ("just", "juste", "RB", "ADV"), ("only", "seulement", "RB", "ADV"),
    ("even", "même", "RB", "ADV"), ("still", "encore", "RB", "ADV"),
    ("already", "déjà", "RB", "ADV"), ("always", "toujours", "RB", "ADV"),
    ("never", "jamais", "RB", "ADV"), ("often", "souvent", "RB", "ADV"),
    ("together", "ensemble", "RB", "ADV"), ("well", "bien", "RB", "ADV"),
    ("really", "vraiment", "RB", "ADV"), ("almost", "presque", "RB", "ADV"),
    ("enough", "assez", "RB", "ADV"), ("too", "aussi", "RB", "ADV"),
    ("far", "loin", "RB", "ADV"),
    # CS-specific
    ("algorithm", "algorithme", "NN", "NC"), ("function", "fonction", "NN", "NC"),
    ("variable", "variable", "NN", "NC"), ("class", "classe", "NN", "NC"),
    ("object", "objet", "NN", "NC"), ("interface", "interface", "NN", "NC"),
    ("network", "réseau", "NN", "NC"), ("database", "base de données", "NN", "NC"),
    ("server", "serveur", "NN", "NC"), ("client", "client", "NN", "NC"),
    ("application", "application", "NN", "NC"), ("architecture", "architecture", "NN", "NC"),
    ("framework", "cadre", "NN", "NC"), ("library", "bibliothèque", "NN", "NC"),
    ("code", "code", "NN", "NC"), ("file", "fichier", "NN", "NC"),
    ("directory", "répertoire", "NN", "NC"), ("memory", "mémoire", "NN", "NC"),
    ("processor", "processeur", "NN", "NC"), ("screen", "écran", "NN", "NC"),
    ("keyboard", "clavier", "NN", "NC"), ("software", "logiciel", "NN", "NC"),
    ("hardware", "matériel", "NN", "NC"), ("internet", "Internet", "NN", "NC"),
    ("website", "site web", "NN", "NC"), ("email", "courriel", "NN", "NC"),
    ("digital", "numérique", "JJ", "ADJ"), ("virtual", "virtuel", "JJ", "ADJ"),
    ("automatic", "automatique", "JJ", "ADJ"), ("artificial", "artificiel", "JJ", "ADJ"),
    ("intelligent", "intelligent", "JJ", "ADJ"), ("complex", "complexe", "JJ", "ADJ"),
    ("effective", "efficace", "JJ", "ADJ"), ("efficient", "efficace", "JJ", "ADJ"),
    ("modern", "moderne", "JJ", "ADJ"), ("traditional", "traditionnel", "JJ", "ADJ"),
    ("basic", "basique", "JJ", "ADJ"), ("general", "général", "JJ", "ADJ"),
    ("specific", "spécifique", "JJ", "ADJ"), ("technical", "technique", "JJ", "ADJ"),
    ("professional", "professionnel", "JJ", "ADJ"),
    ("analyze", "analyser", "VB", "V"), ("compare", "comparer", "VB", "V"),
    ("observe", "observer", "VB", "V"), ("measure", "mesurer", "VB", "V"),
    ("calculate", "calculer", "VB", "V"), ("design", "concevoir", "VB", "V"),
    ("implement", "implémenter", "VB", "V"), ("evaluate", "évaluer", "VB", "V"),
    ("describe", "décrire", "VB", "V"), ("explain", "expliquer", "VB", "V"),
    ("discuss", "discuter", "VB", "V"), ("present", "présenter", "VB", "V"),
    ("propose", "proposer", "VB", "V"), ("conclude", "conclure", "VB", "V"),
    ("determine", "déterminer", "VB", "V"), ("establish", "établir", "VB", "V"),
    ("identify", "identifier", "VB", "V"), ("examine", "examiner", "VB", "V"),
    ("investigate", "enquêter", "VB", "V"), ("demonstrate", "démontrer", "VB", "V"),
    ("illustrate", "illustrer", "VB", "V"), ("reveal", "révéler", "VB", "V"),
    ("indicate", "indiquer", "VB", "V"), ("represent", "représenter", "VB", "V"),
    ("contain", "contenir", "VB", "V"), ("consist", "consister", "VB", "V"),
    ("depend", "dépendre", "VB", "V"), ("affect", "affecter", "VB", "V"),
    ("influence", "influencer", "VB", "V"), ("cause", "causer", "VB", "V"),
    ("produce", "produire", "VB", "V"), ("receive", "recevoir", "VB", "V"),
    ("obtain", "obtenir", "VB", "V"), ("generate", "générer", "VB", "V"),
    ("compute", "calculer", "VB", "V"), ("process", "traiter", "VB", "V"),
    ("store", "stocker", "VB", "V"), ("transmit", "transmettre", "VB", "V"),
    ("convert", "convertir", "VB", "V"), ("translate", "traduire", "VB", "V"),
    ("transform", "transformer", "VB", "V"), ("apply", "appliquer", "VB", "V"),
    ("combine", "combiner", "VB", "V"), ("separate", "séparer", "VB", "V"),
    ("select", "sélectionner", "VB", "V"), ("extract", "extraire", "VB", "V"),
    ("filter", "filtrer", "VB", "V"), ("sort", "trier", "VB", "V"),
    ("merge", "fusionner", "VB", "V"), ("classify", "classer", "VB", "V"),
    ("group", "grouper", "VB", "V"), ("organize", "organiser", "VB", "V"),
    ("manage", "gérer", "VB", "V"), ("control", "contrôler", "VB", "V"),
    ("monitor", "surveiller", "VB", "V"), ("optimize", "optimiser", "VB", "V"),
    ("improve", "améliorer", "VB", "V"), ("enhance", "améliorer", "VB", "V"),
    ("modify", "modifier", "VB", "V"), ("update", "mettre à jour", "VB", "V"),
    ("configure", "configurer", "VB", "V"), ("initialize", "initialiser", "VB", "V"),
    ("execute", "exécuter", "VB", "V"), ("perform", "effectuer", "VB", "V"),
    ("operate", "opérer", "VB", "V"), ("connect", "connecter", "VB", "V"),
    ("disconnect", "déconnecter", "VB", "V"), ("copy", "copier", "VB", "V"),
    ("delete", "supprimer", "VB", "V"), ("save", "sauvegarder", "VB", "V"),
    ("load", "charger", "VB", "V"), ("download", "télécharger", "VB", "V"),
    ("upload", "téléverser", "VB", "V"), ("search", "rechercher", "VB", "V"),
    ("browse", "parcourir", "VB", "V"), ("navigate", "naviguer", "VB", "V"),
    ("display", "afficher", "VB", "V"), ("print", "imprimer", "VB", "V"),
    ("record", "enregistrer", "VB", "V"), ("pause", "mettre en pause", "VB", "V"),
    ("start", "démarrer", "VB", "V"), ("restart", "redémarrer", "VB", "V"),
    ("reset", "réinitialiser", "VB", "V"), ("cancel", "annuler", "VB", "V"),
    ("confirm", "confirmer", "VB", "V"), ("validate", "valider", "VB", "V"),
    ("verify", "vérifier", "VB", "V"), ("check", "vérifier", "VB", "V"),
    ("debug", "déboguer", "VB", "V"), ("trace", "tracer", "VB", "V"),
    ("log", "journaliser", "VB", "V"), ("notify", "notifier", "VB", "V"),
    ("alert", "alerter", "VB", "V"), ("warn", "avertir", "VB", "V"),
    ("request", "demander", "VB", "V"), ("respond", "répondre", "VB", "V"),
    ("accept", "accepter", "VB", "V"), ("reject", "rejeter", "VB", "V"),
    ("approve", "approuver", "VB", "V"), ("allow", "permettre", "VB", "V"),
    ("restrict", "restreindre", "VB", "V"), ("lock", "verrouiller", "VB", "V"),
    ("unlock", "déverrouiller", "VB", "V"), ("encrypt", "chiffrer", "VB", "V"),
    ("decrypt", "déchiffrer", "VB", "V"), ("authenticate", "authentifier", "VB", "V"),
    ("authorize", "autoriser", "VB", "V"),
    ("parallel", "parallèle", "JJ", "ADJ"), ("serial", "série", "JJ", "ADJ"),
    ("synchronous", "synchrone", "JJ", "ADJ"), ("asynchronous", "asynchrone", "JJ", "ADJ"),
    ("concurrent", "concurrent", "JJ", "ADJ"), ("sequential", "séquentiel", "JJ", "ADJ"),
    ("iterative", "itératif", "JJ", "ADJ"), ("recursive", "récursif", "JJ", "ADJ"),
    ("linear", "linéaire", "JJ", "ADJ"), ("static", "statique", "JJ", "ADJ"),
    ("dynamic", "dynamique", "JJ", "ADJ"), ("local", "local", "JJ", "ADJ"),
    ("global", "global", "JJ", "ADJ"), ("public", "public", "JJ", "ADJ"),
    ("private", "privé", "JJ", "ADJ"), ("abstract", "abstrait", "JJ", "ADJ"),
    ("concrete", "concret", "JJ", "ADJ"), ("final", "final", "JJ", "ADJ"),
    ("constant", "constante", "JJ", "ADJ"), ("mutable", "mutable", "JJ", "ADJ"),
    ("generic", "générique", "JJ", "ADJ"), ("atomic", "atomique", "JJ", "ADJ"),
    ("distributed", "distribué", "JJ", "ADJ"), ("centralized", "centralisé", "JJ", "ADJ"),
    ("scalable", "évolutif", "JJ", "ADJ"), ("robust", "robuste", "JJ", "ADJ"),
    ("flexible", "flexible", "JJ", "ADJ"), ("reliable", "fiable", "JJ", "ADJ"),
    ("secure", "sûr", "JJ", "ADJ"), ("stable", "stable", "JJ", "ADJ"),
    ("portable", "portable", "JJ", "ADJ"), ("compatible", "compatible", "JJ", "ADJ"),
    ("standard", "standard", "JJ", "ADJ"), ("open", "ouvert", "JJ", "ADJ"),
    ("closed", "fermé", "JJ", "ADJ"),
    ("trial", "essai", "NN", "NC"), ("license", "licence", "NN", "NC"),
    ("copyright", "droit d'auteur", "NN", "NC"), ("patent", "brevet", "NN", "NC"),
    ("programming", "programmation", "NN", "NC"),
    ("engineering", "ingénierie", "NN", "NC"),
    ("mathematics", "mathématiques", "NN", "NC"), ("physics", "physique", "NN", "NC"),
    ("chemistry", "chimie", "NN", "NC"), ("biology", "biologie", "NN", "NC"),
    ("design", "conception", "NN", "NC"), ("implementation", "implémentation", "NN", "NC"),
    ("evaluation", "évaluation", "NN", "NC"), ("optimization", "optimisation", "NN", "NC"),
    ("simulation", "simulation", "NN", "NC"), ("automation", "automatisation", "NN", "NC"),
    ("theory", "théorie", "NN", "NC"), ("hypothesis", "hypothèse", "NN", "NC"),
    ("experiment", "expérience", "NN", "NC"), ("observation", "observation", "NN", "NC"),
    ("measurement", "mesure", "NN", "NC"), ("prediction", "prédiction", "NN", "NC"),
    ("classification", "classification", "NN", "NC"), ("clustering", "regroupement", "NN", "NC"),
    ("pattern", "motif", "NN", "NC"), ("feature", "caractéristique", "NN", "NC"),
    ("parameter", "paramètre", "NN", "NC"), ("constant", "constante", "NN", "NC"),
    ("input", "entrée", "NN", "NC"), ("output", "sortie", "NN", "NC"),
    ("error", "erreur", "NN", "NC"), ("exception", "exception", "NN", "NC"),
    ("warning", "avertissement", "NN", "NC"), ("success", "succès", "NN", "NC"),
    ("failure", "échec", "NN", "NC"), ("performance", "performance", "NN", "NC"),
    ("efficiency", "efficacité", "NN", "NC"), ("reliability", "fiabilité", "NN", "NC"),
    ("availability", "disponibilité", "NN", "NC"), ("security", "sécurité", "NN", "NC"),
    ("privacy", "confidentialité", "NN", "NC"), ("scalability", "évolutivité", "NN", "NC"),
    ("usability", "utilisabilité", "NN", "NC"), ("quality", "qualité", "NN", "NC"),
    ("quantity", "quantité", "NN", "NC"), ("cost", "coût", "NN", "NC"),
    ("benefit", "avantage", "NN", "NC"), ("risk", "risque", "NN", "NC"),
    ("opportunity", "opportunité", "NN", "NC"), ("challenge", "défi", "NN", "NC"),
    ("solution", "solution", "NN", "NC"), ("strategy", "stratégie", "NN", "NC"),
    ("plan", "plan", "NN", "NC"), ("goal", "objectif", "NN", "NC"),
    ("objective", "objectif", "NN", "NC"), ("target", "cible", "NN", "NC"),
    ("milestone", "jalon", "NN", "NC"), ("deadline", "échéance", "NN", "NC"),
    ("schedule", "calendrier", "NN", "NC"), ("budget", "budget", "NN", "NC"),
    ("resource", "ressource", "NN", "NC"), ("tool", "outil", "NN", "NC"),
    ("document", "document", "NN", "NC"), ("file", "fichier", "NN", "NC"),
    ("record", "enregistrement", "NN", "NC"), ("log", "journal", "NN", "NC"),
    ("report", "rapport", "NN", "NC"), ("summary", "résumé", "NN", "NC"),
    ("detail", "détail", "NN", "NC"), ("specification", "spécification", "NN", "NC"),
    ("requirement", "exigence", "NN", "NC"), ("constraint", "contrainte", "NN", "NC"),
    ("condition", "condition", "NN", "NC"), ("rule", "règle", "NN", "NC"),
    ("policy", "politique", "NN", "NC"), ("procedure", "procédure", "NN", "NC"),
    ("protocol", "protocole", "NN", "NC"), ("standard", "norme", "NN", "NC"),
    ("figure", "figure", "NN", "NC"), ("table", "tableau", "NN", "NC"),
    ("chart", "graphique", "NN", "NC"), ("diagram", "diagramme", "NN", "NC"),
    ("graph", "graphe", "NN", "NC"), ("picture", "image", "NN", "NC"),
    ("illustration", "illustration", "NN", "NC"), ("visualization", "visualisation", "NN", "NC"),
    ("example", "exemple", "NN", "NC"), ("sample", "échantillon", "NN", "NC"),
    ("scenario", "scénario", "NN", "NC"), ("validation", "validation", "NN", "NC"),
    ("verification", "vérification", "NN", "NC"),
    ("user", "utilisateur", "NN", "NC"), ("administrator", "administrateur", "NN", "NC"),
    ("developer", "développeur", "NN", "NC"), ("designer", "concepteur", "NN", "NC"),
    ("engineer", "ingénieur", "NN", "NC"), ("analyst", "analyste", "NN", "NC"),
    ("manager", "gestionnaire", "NN", "NC"), ("team", "équipe", "NN", "NC"),
    ("group", "groupe", "NN", "NC"), ("department", "département", "NN", "NC"),
    ("organization", "organisation", "NN", "NC"), ("institution", "institution", "NN", "NC"),
    ("meeting", "réunion", "NN", "NC"), ("conference", "conférence", "NN", "NC"),
    ("report", "rapport", "NN", "NC"), ("publication", "publication", "NN", "NC"),
    ("article", "article", "NN", "NC"), ("paper", "article", "NN", "NC"),
    ("thesis", "thèse", "NN", "NC"), ("book", "livre", "NN", "NC"),
    ("translation", "traduction", "NN", "NC"), ("interpretation", "interprétation", "NN", "NC"),
    ("adaptation", "adaptation", "NN", "NC"), ("transformation", "transformation", "NN", "NC"),
    ("conversion", "conversion", "NN", "NC"), ("modification", "modification", "NN", "NC"),
    ("revision", "révision", "NN", "NC"), ("correction", "correction", "NN", "NC"),
    ("editing", "édition", "NN", "NC"), ("publishing", "publication", "NN", "NC"),
    ("distribution", "distribution", "NN", "NC"), ("marketing", "marketing", "NN", "NC"),
    ("promotion", "promotion", "NN", "NC"), ("sales", "ventes", "NNS", "NC"),
    ("revenue", "revenu", "NN", "NC"), ("profit", "profit", "NN", "NC"),
    ("loss", "perte", "NN", "NC"), ("expense", "dépense", "NN", "NC"),
    ("income", "revenu", "NN", "NC"), ("investment", "investissement", "NN", "NC"),
    ("return", "rendement", "NN", "NC"), ("capital", "capital", "NN", "NC"),
    ("transaction", "transaction", "NN", "NC"), ("payment", "paiement", "NN", "NC"),
    ("order", "commande", "NN", "NC"), ("delivery", "livraison", "NN", "NC"),
    ("supply", "approvisionnement", "NN", "NC"), ("demand", "demande", "NN", "NC"),
    ("market", "marché", "NN", "NC"), ("competition", "concurrence", "NN", "NC"),
    ("economy", "économie", "NN", "NC"), ("society", "société", "NN", "NC"),
    ("culture", "culture", "NN", "NC"), ("civilization", "civilisation", "NN", "NC"),
    ("geography", "géographie", "NN", "NC"), ("philosophy", "philosophie", "NN", "NC"),
    ("art", "art", "NN", "NC"), ("literature", "littérature", "NN", "NC"),
    ("theater", "théâtre", "NN", "NC"), ("cinema", "cinéma", "NN", "NC"),
    ("film", "film", "NN", "NC"), ("photography", "photographie", "NN", "NC"),
    ("painting", "peinture", "NN", "NC"), ("sculpture", "sculpture", "NN", "NC"),
]


def _tokenize(text: str) -> list:
    return [w.lower() for w in re.findall(r"[a-zA-Zàâäéèêëîïôöùûüçÿœæ]+", text.lower())]


# French function words to exclude from seed alignment
_FR_STOP = {
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'la', 'l', "l'",
    'et', 'ou', 'mais', 'donc', 'or', 'ni', 'car',
    'est', 'sont', 'était', 'étaient', 'a', 'ont', 'avait', 'avaient',
    'dans', 'sur', 'avec', 'pour', 'par', 'sans', 'sous', 'entre', 'chez',
    'pas', 'ne', 'plus', 'très', 'bien', 'aussi', 'encore', 'alors',
    'je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles',
    'me', 'te', 'se', 'lui', 'leur', 'y', 'en',
    'ce', 'cette', 'ces', 'cet', 'qui', 'que', 'quoi', 'dont', 'où',
    'son', 'sa', 'ses', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes',
    'notre', 'nos', 'votre', 'vos', 'leurs',
    'été', 'être', 'avoir', 'faire', 'dire', 'aller', 'pouvoir', 'vouloir',
    'comme', 'même', 'si', 'tout', 'fait', 'peut', 'doit', 'va',
}

# POS tags that should be excluded from alignment (function words)
_FR_EXCLUDE_POS = {'DT', 'DET', 'IN', 'PRE', 'CC', 'CON', 'PRP', 'PRO', 'MD', 'TO', 'WP', 'WDT', 'WRB'}


def _split_sentences(text: str) -> list:
    """Split text into sentences."""
    return sent_tokenize(text)


def build_from_seed_paragraphs() -> int:
    """Build word dictionary from parallel EN/FR seed paragraphs using sentence alignment.

    Each seed paragraph is a parallel block (EN_TRAIN[i] ≈ FR_TRAIN[i]).
    We split each paragraph into sentences, align by position, then align
    tokens within each sentence pair by position.
    Filters out function words and articles to avoid garbage pairs.
    """
    total = 0
    en_paragraphs = EN_TRAIN
    fr_paragraphs = FR_TRAIN

    for en_para, fr_para in zip(en_paragraphs, fr_paragraphs):
        en_sents = _split_sentences(en_para)
        fr_sents = _split_sentences(fr_para)

        min_sents = min(len(en_sents), len(fr_sents))
        for si in range(min_sents):
            en_tokens = _tokenize(en_sents[si])
            fr_tokens = _tokenize(fr_sents[si])

            min_len = min(len(en_tokens), len(fr_tokens))
            for ti in range(min_len):
                en_word = en_tokens[ti]
                fr_word = fr_tokens[ti]

                # Skip function words on either side
                if en_word in _FR_STOP or fr_word in _FR_STOP:
                    continue
                if len(en_word) <= 2 or len(fr_word) <= 2:
                    continue
                # Skip if word lengths are too different (bad alignment)
                if abs(len(en_word) - len(fr_word)) > max(len(en_word), len(fr_word)) * 0.6:
                    continue

                # Get POS for English word
                tagged = pos_tag_en(en_word)
                pos = tagged[0][1] if tagged else ""

                # Skip function word POS
                if pos in _FR_EXCLUDE_POS:
                    continue

                dictionary.add_entry(en_word, fr_word, pos, "", frequency=3)
                total += 1

    return total


def build_phrases() -> int:
    """Populate the phrase dictionary with common multi-word expressions."""
    entries = [{"source": s, "target": t, "freq": 10} for s, t in PHRASE_PAIRS]
    return dictionary.bulk_add_phrases(entries)


def bootstrap_dictionary() -> int:
    """Load the hardcoded common translations into the DB."""
    entries = []
    seen = set()
    for source, target, s_pos, t_pos in COMMON_TRANSLATIONS:
        key = (source.lower(), target.lower(), s_pos)
        if key not in seen:
            seen.add(key)
            entries.append({
                "source": source,
                "target": target,
                "source_pos": s_pos,
                "target_pos": t_pos,
                "freq": 10,
            })
    return dictionary.bulk_add(entries)


def build_all() -> dict:
    """Build complete dictionary: bootstrap + seed paragraphs + phrases."""
    word_count = bootstrap_dictionary()
    seed_count = build_from_seed_paragraphs()
    phrase_count = build_phrases()
    return {
        "word_entries": word_count,
        "seed_pairs": seed_count,
        "phrase_entries": phrase_count,
    }
