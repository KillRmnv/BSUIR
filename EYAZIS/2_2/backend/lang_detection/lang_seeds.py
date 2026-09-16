"""
Offline seed texts for Variant 7 (EN/FR language identification).

Two disjoint sets per language:
  - *_TRAIN: expanded (seeded shuffle) into training corpora (~20-40 Kb).
  - *_TEST:  expanded into one ~A4 HTML test document each.

IMPORTANT FOR THE REPORT: these seeds are an offline stand-in. The method
recommends replacing/extending them with Wikipedia articles (20-120 Kb per
language); `build_lang_corpus.py` records the real source + sizes in
corpus_meta.json. Generation method (seed=7 shuffle) is deterministic.
"""

EN_TRAIN = [
    "The history of photography began in the early nineteenth century with the discovery of light-sensitive materials. "
    "In 1826, Joseph Nicephore Niepce produced the first permanent photograph, showing the view from his window in France. "
    "The exposure lasted several hours, and the image was rough by modern standards, yet it proved that light could fix an image. "
    "A decade later, Louis Daguerre introduced the daguerreotype, which reduced exposure time to minutes and delivered sharp detail.",

    "The human brain contains approximately eighty-six billion neurons connected by trillions of synapses. "
    "Each neuron communicates with others through electrical impulses and chemical signals called neurotransmitters. "
    "The cerebral cortex, responsible for conscious thought and language, is only a few millimetres thick but covers a large surface. "
    "Memory formation involves strengthening synaptic connections, a process known as long-term potentiation.",

    "The Industrial Revolution started in Britain in the late eighteenth century and transformed manufacturing forever. "
    "Steam engines powered by coal allowed factories to operate independently of rivers and wind. "
    "Textile mills were among the first to adopt mechanised looms, dramatically increasing cloth production. "
    "Railways then connected distant cities, moving raw materials and finished goods faster than ever before.",

    "Coral reefs occupy less than one percent of the ocean floor but support about a quarter of all marine species. "
    "They are built by tiny animals called coral polyps, which secrete calcium carbonate skeletons over centuries. "
    "Most reef-building corals live in symbiosis with microscopic algae that provide energy through photosynthesis. "
    "Rising sea temperatures cause coral bleaching, when stressed polyps expel their algae and turn white.",

    "The theory of plate tectonics explains the movement of the rigid outer layer of the Earth. "
    "Continents drift on convection currents in the hot mantle below, moving a few centimetres every year. "
    "Where plates collide, mountain ranges rise; where they separate, new oceanic crust is formed. "
    "Earthquakes cluster along plate boundaries, such as the Pacific Ring of Fire.",

    "Coffee is one of the most widely traded agricultural commodities in the world. "
    "The two main cultivated species are Arabica, prized for its mild flavour, and Robusta, which contains more caffeine. "
    "Coffee plants grow best in tropical highlands with rich soil and distinct wet and dry seasons. "
    "After harvesting, the beans are dried, roasted, and ground before brewing.",

    "The Internet originated as a research project funded by the United States Department of Defense in the 1960s. "
    "The ARPANET used packet switching, breaking messages into small blocks that travelled independently. "
    "In the 1980s, the TCP/IP protocol suite became the standard, allowing different networks to interconnect. "
    "The World Wide Web, invented in 1990, made the Internet accessible to ordinary people through browsers.",

    "Machine learning is a branch of artificial intelligence in which computers improve through experience. "
    "Instead of following fixed rules, algorithms adjust internal parameters to fit observed data. "
    "Supervised learning uses labelled examples, while unsupervised learning discovers hidden structure on its own. "
    "Neural networks with many layers, known as deep learning, excel at images, speech, and language.",

    "Solar energy reaches the Earth in quantities far exceeding current human consumption. "
    "Photovoltaic cells convert sunlight directly into electricity using semiconductor materials such as silicon. "
    "The cost of solar panels has fallen dramatically over the past two decades, making them competitive with fossil fuels. "
    "Large solar farms now supply power to entire cities, especially in sunny regions.",

    "The exploration of space began with the launch of the Soviet satellite Sputnik in 1957. "
    "Four years later, Yuri Gagarin became the first human to orbit the Earth. "
    "In 1969, American astronauts landed on the Moon as part of the Apollo programme. "
    "Today, robotic probes study distant planets, while telescopes observe galaxies billions of light-years away.",

    # Wikipedia paragraphs
    "World War II, or the Second World War, was a global conflict between two coalitions: the Allies and the Axis powers. "
    "Nearly all of the world's countries participated, with many engaging in total war on an unprecedented scale. "
    "World War II was the deadliest conflict in history, causing the deaths of 60 to 75 million people, a majority of whom were civilians. "
    "Millions died as a result of massacres, starvation, disease, and genocides including the Holocaust.",

    "The theory of relativity comprises two physics theories by Albert Einstein: special relativity and general relativity, "
    "proposed and published in 1905 and 1915, respectively. Special relativity applies to all physical phenomena in the absence of gravity. "
    "General relativity explains the law of gravitation and its relation to the forces of nature. "
    "It applies to the cosmological and astrophysical realm, including astronomy.",

    "Genetics is the study of genes, genetic variation, and heredity in organisms. "
    "It is an important branch in biology because heredity is vital to organisms' evolution. "
    "Gregor Mendel, a Moravian Augustinian friar working in the 19th century in Brno, was the first to study genetics scientifically. "
    "Mendel studied trait inheritance, patterns in the way traits are handed down from parents to offspring over time.",

    "In modern historiography, ancient Rome is the Roman civilisation from the founding of the Italian city of Rome "
    "in the 8th century BC to the collapse of the Western Roman Empire in the 5th century AD. "
    "It encompasses the Roman Kingdom, the Roman Republic, and the Roman Empire until the fall of the western empire. "
    "Roman culture profoundly influenced Western law, government, art, and language.",

    "Photosynthesis is a system of biological processes by which photopigment-bearing autotrophic organisms "
    "convert light energy typically from sunlight into the chemical energy necessary to fuel their metabolism. "
    "Photosynthetic organisms store the converted chemical energy within the bonds of intracellular organic compounds. "
    "Photosynthesis plays a critical role in producing and maintaining the oxygen content of the Earth's atmosphere.",

    "Nanotechnology is the manipulation of matter with at least one dimension size measuring between 1 to 100 nanometers. "
    "At this scale, surface area and quantum mechanical effects become important in describing the properties of matter. "
    "This definition of nanotechnology includes all types of research and technologies that deal with these distinctive properties. "
    "An earlier understanding referred to the particular goal of precisely manipulating atoms and molecules.",

    "In economics, economic growth is an increase in the quantity and quality of the economic goods and services that a society produces. "
    "It can be measured as the increase in the inflation-adjusted output of an economy in a given year or over a period of time. "
    "It focuses on the economic activities of a country. Factors of growth include capital goods, natural resources, and labour.",

    "A volcanic eruption occurs when material is expelled from a volcanic vent or fissure. "
    "Several types of volcanic eruptions have been distinguished by volcanologists. "
    "These are often named after famous volcanoes where that type of behavior has been observed. "
    "Some volcanoes may exhibit only one characteristic type of eruption during a period of activity.",

    "An antibiotic is a type of antimicrobial substance which is active against bacteria. "
    "It is the most important type of antibacterial agent for fighting bacterial infections. "
    "Antibiotic medications are widely used in the treatment and prevention of such infections. "
    "They may either kill or inhibit the growth of bacteria. A limited number also possess antiprotozoal activity.",

    "The Renaissance was a European period of history and cultural movement taking place at the end of the Late Middle Ages. "
    "It was characterized by the European rediscovery and revival of the literary, philosophical, and artistic achievements of classical antiquity. "
    "Associated with great change in art, architecture, politics, literature, exploration and technology. "
    "The Renaissance was first centered in the Republic of Florence, then spread to the rest of Italy and later throughout Europe.",

    "A satellite or an artificial satellite is an object, typically a spacecraft, placed into orbit around a celestial body. "
    "They have a variety of uses, including communication relay, weather forecasting, navigation, broadcasting, and scientific research. "
    "Additional military uses are reconnaissance, early warning, signals intelligence and, potentially, weapon delivery. "
    "Other satellites include the final rocket stages that place satellites in orbit.",

    "In physics, electromagnetism is an interaction that occurs between particles with electric charge via electromagnetic fields. "
    "The electromagnetic force is one of the four fundamental forces of nature. "
    "It is the dominant force in the interactions of atoms and molecules. "
    "Electromagnetism describes electricity, magnetism, and optics as three closely intertwined phenomena.",

    "The ocean is the body of salt water that covers approximately 70.8 percent of Earth. "
    "The ocean contains 97 percent of Earth's water and is the primary component of Earth's hydrosphere. "
    "It acts as a huge reservoir of heat for Earth's energy budget, as well as for its carbon cycle and water cycle. "
    "The ocean is essential to life on Earth, harbouring most of Earth's animals and protist life.",

    "Mathematics is a field of knowledge concerned with abstract concepts such as numbers, geometric shapes, sets, functions, and probabilities. "
    "It uses logical reasoning and proof to study and establish their properties, often expressed as theorems, formulas, and equations. "
    "Mathematics is used to model and solve problems in science, engineering, technology, economics, and everyday life.",

    "Philosophy is a systematic study of general and fundamental questions concerning topics like existence, knowledge, mind, reason, language, and value. "
    "It is a rational and critical inquiry that reflects on its methods and assumptions. "
    "Philosophy has historically encompassed areas as diverse as metaphysics, epistemology, ethics, and aesthetics.",

    "Archaeology is the study of human activity through the recovery and analysis of material culture. "
    "The archaeological record consists of artifacts, architecture, biofacts or ecofacts, sites, and cultural landscapes. "
    "Archaeology can be considered both a social science and a branch of the humanities. "
    "The discipline involves surveying, excavation, and eventually analysis of data collected to learn more about the past.",

    "Astronomy is a natural science that studies celestial objects and the phenomena that occur in the cosmos. "
    "It uses mathematics, physics, and chemistry to explain their origin and their overall evolution. "
    "Objects of interest include planets, moons, stars, nebulae, galaxies, meteoroids, asteroids, and comets. "
    "Cosmology is the branch of astronomy that studies the universe as a whole.",

    "Biology is the scientific study of life and living organisms. "
    "It is a broad natural science that encompasses a wide range of fields and unifying principles. "
    "Central to biology are five fundamental themes: the cell as the basic unit of life, genes and heredity, "
    "evolution as the driver of biological diversity, energy transformation, and homeostasis.",

    "Chemistry is the scientific study of the properties and behavior of matter. "
    "It is a physical science within the natural sciences that studies matter composition, structure, properties, behavior and changes. "
    "Chemistry also addresses the nature of chemical bonds in chemical compounds. "
    "The discipline includes organic, inorganic, physical, analytical, and biochemistry.",

    "Physics is the scientific study of matter, its fundamental constituents, its motion and behavior through space and time. "
    "It is one of the most fundamental scientific disciplines. "
    "A scientist who specializes in the field of physics is called a physicist. "
    "Physics intersects with many interdisciplinary areas of research, including biophysics and quantum chemistry.",

    "Geography is the study of the lands, features, inhabitants, and phenomena of planet Earth. "
    "Geography is an all-encompassing discipline that seeks an understanding of Earth and its human and natural complexities. "
    "While geography is specific to Earth, many concepts can be applied more broadly to other celestial bodies. "
    "Geography has been called a bridge between natural science and social science disciplines.",

    "Literature is any collection of written work. The term is also used more narrowly for writings considered an art form. "
    "It includes both print and digital writing. In recent centuries, the definition has expanded to include oral literature. "
    "Literature is a method of recording, preserving, and transmitting knowledge and entertainment.",

    "Music is the arrangement of sound to create some combination of form, harmony, melody, rhythm, or otherwise expressive content. "
    "Music is generally agreed to be a cultural universal that is present in all human societies. "
    "Music is often characterized as a highly versatile medium for expressing human creativity. "
    "Music may be performed using a wide variety of musical instruments, including the human voice.",
]

EN_TEST = [
    "Jazz emerged in New Orleans at the beginning of the twentieth century from African and European musical traditions. "
    "Its defining features are improvisation, syncopated rhythms, and the swing feel that makes listeners move. "
    "Legendary performers such as Louis Armstrong and Duke Ellington brought jazz to concert halls around the world. "
    "Later styles like bebop and modal jazz pushed harmony and tempo to new extremes.",

    "The water cycle describes how water moves between oceans, atmosphere, and land. "
    "Heat from the Sun evaporates surface water, and rising vapour cools to form clouds. "
    "Precipitation returns water to rivers and lakes, from where it flows back to the sea. "
    "Underground reservoirs, called aquifers, store fresh water for wells and springs.",

    "The printing press with movable type was developed by Johannes Gutenberg around 1440. "
    "It allowed books to be produced hundreds of times faster than by hand copying. "
    "Cheap printed texts spread literacy and new ideas across Europe within decades. "
    "Historians consider the press one of the most influential inventions in history.",

    "Vaccination trains the immune system to recognise dangerous pathogens before infection. "
    "A vaccine contains a weakened or partial form of the microbe that cannot cause serious illness. "
    "When vaccinated people encounter the real disease, their bodies respond quickly and effectively. "
    "Mass immunisation has eliminated smallpox and nearly defeated polio worldwide.",

    "The Eiffel Tower was built for the World Exhibition held in Paris in 1889. "
    "Its iron lattice reaches a height of three hundred and thirty metres, antenna included. "
    "Initially criticised by artists, it gradually became the most recognisable symbol of France. "
    "Millions of visitors climb its stairs or take lifts to the observation decks every year.",
]

FR_TRAIN = [
    "L'histoire de la photographie commence au début du dix-neuvième siècle avec la découverte des matériaux sensibles à la lumière. "
    "En 1826, Joseph Nicéphore Niépce réalise la première photographie permanente depuis la fenêtre de sa maison en France. "
    "Le temps de pose dure plusieurs heures et l'image reste grossière, mais elle prouve que la lumière peut fixer une image. "
    "Dix ans plus tard, Louis Daguerre présente le daguerréotype, qui réduit la pose à quelques minutes avec un détail remarquable.",

    "Le cerveau humain contient environ quatre-vingt-six milliards de neurones reliés par des billions de synapses. "
    "Chaque neurone communique avec les autres grâce à des impulsions électriques et à des messagers chimiques appelés neurotransmetteurs. "
    "Le cortex cérébral, siège de la pensée consciente et du langage, ne mesure que quelques millimètres d'épaisseur. "
    "La formation de la mémoire repose sur le renforcement des connexions synaptiques.",

    "La révolution industrielle naît en Grande-Bretagne à la fin du dix-huitième siècle et transforme durablement la production. "
    "Les machines à vapeur alimentées au charbon permettent aux usines de fonctionner loin des rivières et du vent. "
    "Les filatures adoptent parmi les premières les métiers à tisser mécaniques, ce qui multiplie la production de tissu. "
    "Les chemins de fer relient ensuite les villes et transportent matières premières et marchandises.",

    "Les récifs coralliens couvrent moins d'un pour cent des fonds marins mais abritent un quart des espèces marines. "
    "Ils sont construits par de minuscules animaux, les polypes coralliens, qui sécrètent des squelettes de carbonate de calcium. "
    "La plupart des coraux vivent en symbiose avec des algues microscopiques qui fournissent de l'énergie par photosynthèse. "
    "La hausse des températures provoque le blanchissement, quand les polypes stressés expulsent leurs algues.",

    "La théorie de la tectonique des plaques explique le mouvement de la couche externe rigide de la Terre. "
    "Les continents dérivent sur les courants de convection du manteau chaud, de quelques centimètres par an. "
    "Là où les plaques se heurtent, des chaînes de montagnes s'élèvent ; là où elles s'écartent, une croûte neuve se forme. "
    "Les séismes se concentrent le long des frontières de plaques, comme la ceinture de feu du Pacifique.",

    "Le café compte parmi les matières premières agricoles les plus échangées dans le monde. "
    "Les deux principales espèces cultivées sont l'arabica, apprécié pour sa douceur, et le robusta, plus riche en caféine. "
    "Les caféiers prospèrent sur les hauts plateaux tropicaux aux sols riches, avec des saisons sèches et humides marquées. "
    "Après la récolte, les grains sont séchés, torréfiés puis moulus avant l'infusion.",

    "Internet trouve son origine dans un programme de recherche financé par le ministère américain de la défense dans les années soixante. "
    "Le réseau ARPANET utilise la commutation de paquets : les messages sont découpés en blocs qui voyagent séparément. "
    "Dans les années quatre-vingt, la suite de protocoles TCP/IP devient la norme et relie les réseaux entre eux. "
    "Le Web, inventé en 1990, ouvre ensuite Internet au grand public grâce aux navigateurs.",

    "L'apprentissage automatique est une branche de l'intelligence artificielle où les ordinateurs progressent par l'expérience. "
    "Au lieu de suivre des règles figées, les algorithmes ajustent leurs paramètres internes en fonction des données observées. "
    "L'apprentissage supervisé utilise des exemples étiquetés, tandis que le non supervisé découvre seul les structures cachées. "
    "Les réseaux de neurones profonds excellent dans l'image, la parole et le langage.",

    "L'énergie solaire parvient sur Terre en quantités bien supérieures à la consommation actuelle de l'humanité. "
    "Les cellules photovoltaïques convertissent directement la lumière en électricité grâce à des semi-conducteurs comme le silicium. "
    "Le coût des panneaux solaires a chuté de façon spectaculaire depuis vingt ans, les rendant compétitifs face aux énergies fossiles. "
    "De grandes centrales solaires alimentent aujourd'hui des villes entières, surtout dans les régions ensoleillées.",

    "L'exploration spatiale commence avec le lancement du satellite soviétique Spoutnik en 1957. "
    "Quatre ans plus tard, Youri Gagarine devient le premier homme à orbiter autour de la Terre. "
    "En 1969, des astronautes américains se posent sur la Lune dans le cadre du programme Apollo. "
    "Aujourd'hui, des sondes robotiques étudient les planètes lointaines pendant que les télescopes observent des galaxies.",

    "L'intelligence artificielle est l'ensemble des systèmes informatiques capables d'effectuer des tâches typiquement associées à l'intelligence, "
    "telles que l'apprentissage, le raisonnement, la résolution de problèmes, la perception ou la prise de décision. "
    "L'intelligence artificielle est également le champ de recherche visant à développer de tels systèmes. "
    "Les applications vont des voitures autonomes aux systèmes de recommandation en passant par les assistants virtuels.",

    "L'informatique quantique est le sous-domaine de l'informatique qui traite des calculateurs quantiques et des modèles de calcul associés. "
    "L'informatique quantique utilise des phénomènes décrits par la mécanique quantique, comme l'intrication quantique ou la superposition quantique. "
    "Les opérations n'y reposent plus sur la manipulation de bits dans un état 1 ou 0, mais de qubits en superposition d'états 1 et 0.",

    "Le changement climatique est l'effet de l'augmentation rapide de la température moyenne de la surface terrestre en cours aux XXe et XXIe siècles. "
    "L'une comme l'autre sont attribuées aux émissions de gaz à effet de serre d'origine humaine. "
    "Le réchauffement en cours depuis le milieu du XXe siècle et provoqué par les activités humaines a des conséquences sans précédent sur le système climatique de la Terre.",

    "La démocratie est, à l'origine, un régime politique dans lequel le pouvoir appartient au peuple, qui l'exerce directement ou par l'intermédiaire de représentants élus. "
    "Elle repose sur des principes fondamentaux tels que la participation citoyenne, la liberté d'expression, l'égalité devant la loi, et le respect de droits fondamentaux.",

    "En biologie, l'évolution est la transformation du monde vivant au cours du temps, qui se manifeste par des changements phénotypiques des organismes à travers les générations. "
    "L'évolution explique la biodiversité sur Terre. L'histoire des espèces peut ainsi être pensée et représentée sous la forme d'un arbre phylogénétique.",

    "Le Système solaire est le système planétaire du Soleil, étoile autour de laquelle tourne la planète Terre. "
    "Il est composé de cette étoile et des objets célestes gravitant autour d'elle : les huit planètes confirmées accompagnées de plus de deux cents satellites naturels connus.",

    "La Révolution française est une période d'intenses bouleversements politiques et sociaux en France et dans ses colonies. "
    "Elle met fin à l'Ancien Régime, notamment à la monarchie absolue, remplacée par la monarchie constitutionnelle puis par la Première République.",

    "La Seconde Guerre mondiale est un conflit armé à l'échelle planétaire qui dure du 1er septembre 1939 au 2 septembre 1945. "
    "Ce conflit oppose schématiquement les Alliés et l'Axe. Ce fut le conflit le plus meurtrier de l'histoire humaine.",

    "La théorie de la relativité renvoie le plus souvent à deux théories complémentaires élaborées par Albert Einstein. "
    "La relativité restreinte de 1905 et la relativité générale de 1915. "
    "La relativité galiléenne, plus ancienne, s'applique à la mécanique newtonienne.",

    "La génétique est la science qui étudie l'organisation, le fonctionnement, la régulation et la modification des gènes. "
    "Elle étudie leur transmission d'une génération à l'autre que dans leur expression au sein d'un même individu.",

    "La Rome antique est à la fois la ville de Rome et l'État qu'elle fonde dans l'Antiquité. "
    "L'idée de Rome antique est inséparable de celle de la culture latine. "
    "Sa domination a laissé d'importantes traces archéologiques et de nombreux témoignages littéraires.",

    "La photosynthèse est le processus bioénergétique qui permet à des organismes de biosynthétiser de la matière organique en utilisant l'énergie lumineuse, l'eau et le dioxyde de carbone.",

    "Les nanosciences et nanotechnologies peuvent être définies comme l'ensemble des études et des procédés de fabrication et de manipulation de structures, de dispositifs et de systèmes matériels à l'échelle du nanomètre.",

    "La croissance économique est la variation positive de la production de biens et de services dans une économie sur une période donnée. "
    "En pratique, l'indicateur le plus utilisé pour la mesurer est le produit intérieur brut (PIB).",

    "Une éruption volcanique est un phénomène géologique caractérisé par l'émission, par un volcan, de laves ou de pyroclastes accompagnés de gaz volcaniques. "
    "Ce phénomène constitue une catastrophe naturelle ayant un impact local ou mondial.",

    "Un antibiotique est une substance naturelle ou synthétique qui tue les bactéries ou bloque leur croissance. "
    "Lorsque la substance est utilisée de manière externe pour tuer la bactérie par contact, on ne parle pas d'antibiotique mais d'antiseptique.",

    "La Renaissance est un mouvement de l'histoire européenne associé à la remise à l'honneur de la littérature, de la philosophie et des arts de l'Antiquité gréco-romaine. "
    "Ce mouvement a pour point de départ l'Italie et se situe chronologiquement à cheval entre le Moyen Âge tardif et l'époque moderne.",

    "Un satellite artificiel est un objet fabriqué par l'être humain, envoyé dans l'espace à l'aide d'un lanceur et gravitant autour d'une planète ou d'un satellite naturel comme la Lune.",

    "L'électromagnétisme, aussi appelé interaction électromagnétique, est la branche de la physique qui étudie les interactions entre particules chargées électriquement.",

    "Un océan est souvent défini, en géographie, comme une vaste étendue d'eau salée comprise entre deux continents. "
    "Approximativement 70,8 pour cent de la surface de la Terre est recouverte par l'océan mondial.",

    "Les mathématiques sont un ensemble de connaissances abstraites résultant de raisonnements logiques appliqués à des objets divers. "
    "Elles sont aussi le domaine de recherche développant ces connaissances, ainsi que la discipline qui les enseigne.",

    "La philosophie est une démarche qui vise à la compréhension du monde et de la vie par une réflexion rationnelle et critique. "
    "C'est une recherche de la vérité qui est guidée par un questionnement sur le monde, la connaissance et l'existence humaine.",

    "L'archéologie est une discipline scientifique dont l'objectif est d'étudier l'être humain à travers l'ensemble des vestiges matériels ayant subsisté au cours des siècles.",

    "L'astronomie est la discipline scientifique qui étudie les objets célestes afin d'expliquer leurs propriétés physiques et chimiques ainsi que leur origine et leur évolution.",

    "La biologie est la science du vivant. Elle recouvre une partie des sciences de la nature et de l'histoire naturelle des êtres vivants.",

    "La chimie est une science de la nature qui étudie la composition de la matière et ses transformations, plus précisément les atomes, par leurs assemblages nommés molécules.",

    "La physique est une science qui étudie, modélise et formalise les phénomènes naturels de l'Univers. "
    "Elle correspond à l'étude du monde qui nous entoure sous toutes ses formes.",

    "La géographie est une science centrée sur le présent, ayant pour objet la description de la Terre et en particulier l'étude des phénomènes physiques, biologiques et humains qui se produisent sur le globe terrestre.",

    "La littérature est l'ensemble des œuvres écrites ou orales auxquelles on reconnaît une valeur esthétique. "
    "C'est un art exprimant un idéal de beauté. Grâce aux productions littéraires, elle permet de manifester des émotions.",
]

FR_TEST = [
    "Le jazz naît à La Nouvelle-Orléans au début du vingtième siècle, du croisement des traditions musicales africaines et européennes. "
    "Ses traits distinctifs sont l'improvisation, les rythmes syncopés et le swing qui donne envie de danser. "
    "Des musiciens légendaires comme Louis Armstrong et Duke Ellington portent le jazz dans les salles du monde entier. "
    "Des styles ultérieurs comme le bebop repoussent l'harmonie et le tempo vers de nouveaux extrêmes.",

    "Le cycle de l'eau décrit la circulation de l'eau entre les océans, l'atmosphère et les continents. "
    "La chaleur du Soleil évapore les eaux de surface, et la vapeur qui s'élève se refroidit pour former les nuages. "
    "Les précipitations ramènent l'eau vers les rivières et les lacs, d'où elle retourne à la mer. "
    "Les nappes souterraines, appelées aquifères, stockent l'eau douce des puits et des sources.",

    "La presse à caractères mobiles est mise au point par Johannes Gutenberg vers 1440. "
    "Elle permet de produire des livres des centaines de fois plus vite que la copie à la main. "
    "Les textes imprimés bon marché diffusent l'alphabétisation et les idées neuves à travers l'Europe en quelques décennies. "
    "Les historiens comptent la presse parmi les inventions les plus influentes de l'histoire.",

    "La vaccination apprend au système immunitaire à reconnaître les agents pathogènes avant l'infection. "
    "Un vaccin contient une forme affaiblie du microbe, incapable de provoquer une maladie grave. "
    "Quand une personne vaccinée rencontre la vraie maladie, son organisme réagit vite et efficacement. "
    "La vaccination de masse a éradiqué la variole et presque vaincu la poliomyélite.",

    "La tour Eiffel est construite pour l'Exposition universelle organisée à Paris en 1889. "
    "Sa structure en fer culmine à trois cent trente mètres, antenne comprise. "
    "D'abord critiquée par les artistes, elle devient peu à peu le symbole le plus célèbre de la France. "
    "Des millions de visiteurs gravissent ses escaliers ou empruntent ses ascenseurs chaque année.",
]

SEED_PARAGRAPHS = [{"en": en, "fr": fr} for en, fr in zip(EN_TRAIN, FR_TRAIN)]
