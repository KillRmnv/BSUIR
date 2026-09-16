#!/usr/bin/env python3
"""Generate ~200 KB of realistic EN and FR training text offline."""

import os
import random

BASE_DIR = os.path.dirname(__file__)
TRAINING_DIR = os.path.join(BASE_DIR, "training")
SEED = 42

EN_BLOCKS = [
    "Artificial intelligence has transformed numerous industries over the past decade. "
    "Machine learning algorithms now power recommendation systems, autonomous vehicles, and medical diagnostics. "
    "Deep neural networks have achieved superhuman performance in image recognition and natural language understanding. "
    "Researchers continue to push the boundaries of what is possible with computational intelligence.",

    "Climate change represents one of the most pressing challenges facing humanity today. "
    "Rising global temperatures are causing more frequent extreme weather events, including hurricanes, droughts, and floods. "
    "Scientists warn that without significant reductions in greenhouse gas emissions, catastrophic consequences are inevitable. "
    "Renewable energy sources such as solar and wind power offer viable alternatives to fossil fuels.",

    "The human brain contains approximately eighty-six billion neurons connected by trillions of synapses. "
    "Each neuron communicates with others through electrical impulses and chemical signals called neurotransmitters. "
    "Memory formation involves strengthening synaptic connections through a process known as long-term potentiation. "
    "Neuroscience research continues to reveal the remarkable complexity of neural circuits.",

    "The Industrial Revolution began in Britain in the late eighteenth century and fundamentally changed manufacturing. "
    "Steam engines powered by coal allowed factories to operate independently of rivers and wind. "
    "Textile mills adopted mechanized looms that dramatically increased cloth production. "
    "Railways connected distant cities and facilitated the movement of raw materials and finished goods.",

    "Quantum computing harnesses the principles of quantum mechanics to process information in fundamentally new ways. "
    "Unlike classical bits that exist as either zero or one, qubits can exist in superposition of both states simultaneously. "
    "This property allows quantum computers to solve certain problems exponentially faster than classical machines. "
    "Major technology companies are investing billions of dollars in quantum research and development.",

    "The Internet originated as a research project funded by the United States Department of Defense in the 1960s. "
    "The ARPANET used packet switching to break messages into small blocks that traveled independently across the network. "
    "In the 1980s, the TCP/IP protocol suite became the standard for interconnecting different networks. "
    "The World Wide Web, invented in 1990, made the Internet accessible to ordinary people through web browsers.",

    "Solar energy reaches the Earth in quantities far exceeding current human consumption. "
    "Photovoltaic cells convert sunlight directly into electricity using semiconductor materials such as silicon. "
    "The cost of solar panels has fallen dramatically over the past two decades. "
    "Large solar farms now supply power to entire cities, especially in sunny regions around the world.",

    "Coral reefs occupy less than one percent of the ocean floor but support approximately a quarter of all marine species. "
    "They are built by tiny animals called coral polyps that secrete calcium carbonate skeletons over centuries. "
    "Most reef-building corals live in symbiosis with microscopic algae that provide energy through photosynthesis. "
    "Rising sea temperatures cause coral bleaching when stressed polyps expel their symbiotic algae.",

    "The theory of plate tectonics explains the movement of the rigid outer layer of the Earth. "
    "Continents drift on convection currents in the hot mantle below, moving a few centimeters every year. "
    "Where plates collide, mountain ranges rise; where they separate, new oceanic crust is formed. "
    "Earthquakes and volcanic eruptions cluster along plate boundaries such as the Pacific Ring of Fire.",

    "Coffee is one of the most widely traded agricultural commodities in the world. "
    "The two main cultivated species are Arabica, prized for its mild flavor, and Robusta, which contains more caffeine. "
    "Coffee plants grow best in tropical highlands with rich soil and distinct wet and dry seasons. "
    "After harvesting, the beans are dried, roasted, and ground before brewing into the popular beverage.",

    "Machine learning is a branch of artificial intelligence in which computers improve through experience. "
    "Instead of following fixed rules, algorithms adjust internal parameters to fit observed data patterns. "
    "Supervised learning uses labeled examples, while unsupervised learning discovers hidden structure on its own. "
    "Neural networks with many layers, known as deep learning, excel at processing images, speech, and language.",

    "The exploration of space began with the launch of the Soviet satellite Sputnik in 1957. "
    "Four years later, Yuri Gagarin became the first human to orbit the Earth successfully. "
    "In 1969, American astronauts landed on the Moon as part of the historic Apollo programme. "
    "Today, robotic probes study distant planets while telescopes observe galaxies billions of light-years away.",

    "Genetics is the study of genes, genetic variation, and heredity in organisms. "
    "It is an important branch of biology because heredity is vital to organisms evolution over time. "
    "Gregor Mendel, working in the nineteenth century, was the first to study genetics scientifically. "
    "He observed that organisms inherit traits by way of discrete units of inheritance we now call genes.",

    "The Renaissance was a European period of cultural and intellectual renewal. "
    "It was characterized by the rediscovery and revival of classical antiquity achievements in literature and art. "
    "The movement began in Italy and spread throughout Europe over the following centuries. "
    "Great artists like Leonardo da Vinci and Michelangelo produced masterpieces that still inspire today.",

    "Photosynthesis is the process by which green plants convert light energy into chemical energy. "
    "Using sunlight, water, and carbon dioxide, plants produce glucose and release oxygen as a byproduct. "
    "This process is fundamental to life on Earth as it provides the base of most food chains. "
    "Photosynthesis also plays a critical role in maintaining the oxygen content of the atmosphere.",

    "Nanotechnology involves manipulating matter at the atomic and molecular scale. "
    "At dimensions between one and one hundred nanometers, materials exhibit unique physical and chemical properties. "
    "Applications range from medical drug delivery systems to advanced materials for electronics. "
    "Researchers are developing nanoscale devices that could revolutionize computing and medicine.",

    "The global economy has become increasingly interconnected through trade and digital communication. "
    "International supply chains span multiple countries and involve complex logistics networks. "
    "Economic growth depends on factors including capital investment, technological innovation, and education. "
    "Governments use fiscal and monetary policies to manage economic cycles and promote stability.",

    "Volcanic eruptions occur when molten rock and gases escape from beneath the Earth surface. "
    "Several types of eruptions have been classified by volcanologists based on their characteristics. "
    "Some volcanoes exhibit explosive eruptions while others produce gentle lava flows. "
    "Volcanic activity is concentrated along plate boundaries where tectonic plates meet or separate.",

    "Antibiotics are antimicrobial substances used to treat bacterial infections in humans and animals. "
    "They work by either killing bacteria directly or inhibiting their growth and reproduction. "
    "The discovery of penicillin by Alexander Fleming in 1928 revolutionized modern medicine. "
    "However, the growing problem of antibiotic resistance threatens to undo decades of medical progress.",

    "Mathematics is a field of knowledge concerned with abstract concepts such as numbers and shapes. "
    "It uses logical reasoning and proof to study and establish properties of mathematical objects. "
    "Mathematics is essential for modeling and solving problems in science, engineering, and economics. "
    "From algebra to calculus, mathematical tools form the foundation of modern technological society.",

    "Philosophy is a systematic study of fundamental questions about existence, knowledge, and values. "
    "It employs rational inquiry and critical analysis to explore topics like mind, reason, and language. "
    "Philosophers have debated the nature of reality and morality for thousands of years. "
    "The discipline encompasses diverse traditions from ancient Greece to contemporary analytic philosophy.",

    "Astronomy is a natural science that studies celestial objects and cosmic phenomena. "
    "It uses mathematics, physics, and chemistry to explain the origin and evolution of the universe. "
    "Objects of interest include planets, stars, galaxies, nebulae, and black holes. "
    "Modern telescopes can observe light from objects billions of light-years away from Earth.",

    "Biology is the scientific study of life and living organisms in all their forms. "
    "It encompasses a wide range of fields from molecular genetics to ecology and evolution. "
    "Central to biology are concepts like the cell as the basic unit of life and DNA as the carrier of genetic information. "
    "Biological research has led to breakthroughs in medicine, agriculture, and environmental science.",

    "Chemistry studies the composition, structure, properties, and reactions of matter. "
    "It is often called the central science because it connects physics with other natural sciences. "
    "Chemical bonds hold atoms together in molecules and determine the properties of substances. "
    "From pharmaceuticals to polymers, chemistry creates materials that shape modern civilization.",

    "Physics is the most fundamental natural science, studying matter, energy, and their interactions. "
    "It seeks to understand the laws that govern the universe from subatomic particles to galaxies. "
    "Key areas include mechanics, thermodynamics, electromagnetism, and quantum theory. "
    "Physics provides the theoretical foundation for engineering, technology, and many scientific disciplines.",

    "Geography studies the lands, features, inhabitants, and phenomena of planet Earth. "
    "It combines physical science with social science to understand human-environment interactions. "
    "Geographers use tools like geographic information systems to analyze spatial patterns and processes. "
    "The discipline bridges natural science and social science, examining both physical landscapes and human societies.",

    "Literature encompasses written works considered to have artistic or intellectual value. "
    "It includes genres such as novels, poetry, drama, and essays that reflect human experience. "
    "Literary works preserve cultural heritage and transmit knowledge across generations. "
    "From ancient epics to modern fiction, literature shapes our understanding of the world and ourselves.",

    "Music is the art of arranging sound to create expressions of emotion and beauty. "
    "It is a cultural universal present in all human societies throughout history. "
    "Musical elements include rhythm, melody, harmony, and timbre that combine to form compositions. "
    "From classical symphonies to contemporary popular music, sound艺术 enriches human culture.",

    "The French Revolution was a period of radical political and social upheaval in France. "
    "It began in 1789 with the storming of the Bastille and led to the end of absolute monarchy. "
    "The revolution proclaimed the rights of man and citizen and established a republic. "
    "Its ideals of liberty, equality, and fraternity influenced political movements worldwide.",

    "World War II was the deadliest conflict in human history, involving nations across the globe. "
    "The war lasted from 1939 to 1945 and resulted in the deaths of an estimated seventy million people. "
    "Major powers formed opposing alliances: the Allies fought against the Axis nations. "
    "The war ended with the unconditional surrender of Germany and Japan after devastating atomic bombings.",

    "Democracy is a system of government where power is vested in the people. "
    "Citizens participate in decision-making either directly or through elected representatives. "
    "Democratic principles include free elections, rule of law, protection of human rights, and freedom of speech. "
    "Democracies vary widely in their structures and practices across different countries and cultures.",

    "Evolution is the process by which species change over successive generations through natural selection. "
    "Organisms with traits better suited to their environment tend to survive and reproduce more successfully. "
    "Over millions of years, this process has produced the incredible diversity of life on Earth. "
    "Charles Darwin theory of evolution by natural selection remains a cornerstone of modern biology.",

    "The Internet has transformed how people communicate, work, and access information globally. "
    "Social media platforms connect billions of users across geographical and cultural boundaries. "
    "E-commerce has revolutionized retail by enabling online shopping and digital payments. "
    "However, concerns about privacy, misinformation, and digital divide persist in the connected world.",

    "Quantum mechanics describes the behavior of matter and energy at the smallest scales. "
    "It reveals that particles can exist in multiple states simultaneously until measured. "
    "The uncertainty principle states that certain pairs of physical properties cannot both be known precisely. "
    "Quantum theory has enabled technologies like lasers, semiconductors, and magnetic resonance imaging.",

    "Artificial neural networks are computing systems inspired by biological neural networks in the brain. "
    "They consist of interconnected nodes that process information using connectionist approaches. "
    "Deep learning models with multiple layers have achieved breakthroughs in pattern recognition. "
    "These systems power applications from voice assistants to medical image analysis and autonomous vehicles.",

    "The Industrial Revolution transformed economies from agrarian to industrial and manufacturing-based. "
    "New inventions like the spinning jenny and power loom revolutionized textile production. "
    "Factory systems replaced cottage industries and drew workers from rural areas to urban centers. "
    "The revolution brought unprecedented economic growth but also social problems like child labor and pollution.",

    "Climate science examines the factors that influence Earth climate patterns over time. "
    "Greenhouse gases trap heat in the atmosphere, creating a warming effect that is intensifying. "
    "Ice core data reveals that current carbon dioxide levels are higher than at any point in the past 800,000 years. "
    "International agreements like the Paris Accord aim to limit global warming and its devastating consequences.",

    "Neuroscience investigates the structure and function of the nervous system and brain. "
    "Brain imaging techniques allow researchers to observe neural activity in real time. "
    "Studies have revealed how different brain regions specialize in tasks like language, memory, and emotion. "
    "Understanding the brain could lead to treatments for neurological disorders like Alzheimer disease and Parkinson disease.",

    "Renewable energy sources are becoming increasingly important for sustainable development. "
    "Solar photovoltaic systems convert sunlight directly into electricity with improving efficiency. "
    "Wind turbines harness kinetic energy from air currents to generate clean power. "
    "Hydroelectric dams use flowing water to produce electricity while providing flood control and irrigation.",

    "Genetic engineering allows scientists to modify organisms by altering their DNA sequences. "
    "Techniques like CRISPR-Cas9 enable precise editing of genes in virtually any organism. "
    "Applications include developing disease-resistant crops, treating genetic disorders, and producing medicines. "
    "However, ethical concerns about designer babies and ecological impacts require careful consideration.",

    "Space exploration has expanded our understanding of the solar system and universe. "
    "Rover missions to Mars have provided evidence of ancient water and potential past life. "
    "The Hubble Space Telescope has captured images of galaxies formed shortly after the Big Bang. "
    "Future missions aim to return humans to the Moon and eventually send crews to Mars and beyond.",

    "Architecture combines art and engineering to design buildings and structures. "
    "Architectural styles reflect cultural values, technological capabilities, and environmental conditions. "
    "Sustainable design principles now emphasize energy efficiency and environmental responsibility. "
    "From ancient pyramids to modern skyscrapers, architecture shapes the built environment we inhabit.",

    "Ecology studies the interactions between organisms and their natural environment. "
    "Ecosystems consist of complex food webs and nutrient cycles that maintain biological balance. "
    "Biodiversity refers to the variety of life forms within an ecosystem, region, or the entire planet. "
    "Human activities like deforestation and pollution threaten ecological stability and species survival.",

    "Telecommunications technology enables instant communication across vast distances. "
    "Fiber optic cables carry data as light pulses at speeds approaching the speed of light. "
    "Satellite networks provide global coverage for broadcasting, navigation, and internet access. "
    "The fifth generation of mobile technology promises faster speeds and connectivity for billions of devices.",

    "Economics analyzes how societies allocate scarce resources to satisfy unlimited wants. "
    "Key concepts include supply and demand, market equilibrium, and the role of government intervention. "
    "Microeconomics studies individual decision-making while macroeconomics examines the economy as a whole. "
    "Economic theories help policymakers understand inflation, unemployment, and economic growth patterns.",

    "Psychology is the scientific study of mind and behavior in humans and animals. "
    "Psychologists use experimental methods, observation, and statistical analysis to understand mental processes. "
    "Major perspectives include cognitive, behavioral, developmental, and social psychology. "
    "Applied psychology addresses practical issues like mental health, education, workplace productivity, and human factors.",

    "The European Union is a political and economic union of twenty-seven member states. "
    "It was established to promote peace, establish a unified economic market, and enhance European cooperation. "
    "EU members share a common currency, the euro, and have eliminated many trade barriers between them. "
    "The union faces challenges including Brexit, migration policy, and maintaining democratic governance.",

    "Education is the process of facilitating learning and the acquisition of knowledge, skills, and values. "
    "Educational systems vary widely across countries in their structure, curriculum, and methods. "
    "Technology is transforming education through online learning platforms and digital resources. "
    "Access to quality education remains a fundamental challenge for achieving equity and social mobility.",

    "Public health focuses on protecting and improving the health of populations through collective action. "
    "Disease prevention, health promotion, and healthcare policy are central to public health practice. "
    "Epidemiology, the study of disease patterns in populations, informs public health interventions. "
    "Global health challenges like pandemics require coordinated international cooperation and response.",

    "Biotechnology uses living organisms and biological processes to develop products and technologies. "
    "Applications span medicine, agriculture, industrial processes, and environmental remediation. "
    "Biofuel production from algae and bacteria offers sustainable alternatives to fossil fuels. "
    "Agricultural biotechnology has produced genetically modified crops with improved yield and pest resistance.",

    "Semiconductor technology is the foundation of modern electronic devices and computing systems. "
    "Silicon chips containing billions of transistors power computers, smartphones, and countless other devices. "
    "Moore Law predicted the doubling of transistor density approximately every two years. "
    "As physical limits approach, researchers explore new materials and architectures to continue advancement.",

    "Photonics is the science and technology of generating, controlling, and detecting light. "
    "Laser technology enables applications from precision manufacturing to medical surgery. "
    "Fiber optic communications use light signals to transmit data at incredibly high speeds. "
    "Photonic sensors provide sensitive measurements in fields ranging from environmental monitoring to medical diagnostics.",

    "Urban planning designs and manages the physical layout of cities and communities. "
    "Effective planning balances housing, transportation, parks, and commercial development. "
    "Sustainable urban design reduces environmental impact while improving quality of life for residents. "
    "Smart city initiatives use technology to optimize infrastructure, transportation, and public services.",

    "Logistics manages the flow of goods, information, and resources from origin to consumption. "
    "Supply chain management coordinates suppliers, manufacturers, distributors, and retailers. "
    "E-commerce has increased demand for efficient last-mile delivery systems in urban areas. "
    "Advanced technologies like robotics and artificial intelligence are transforming warehouse and transportation operations.",

    "Agriculture has fed growing human populations for thousands of years through continuous innovation. "
    "Modern farming uses mechanization, irrigation, and chemical inputs to maximize crop yields. "
    "Sustainable agriculture practices aim to maintain productivity while protecting soil and water resources. "
    "Precision farming uses GPS, sensors, and data analytics to optimize planting, irrigation, and harvesting.",

    "Forestry manages forest resources for environmental, economic, and social benefits. "
    "Sustainable forest management balances timber harvesting with conservation of biodiversity and ecosystem services. "
    "Forests play a crucial role in carbon sequestration, helping mitigate climate change by absorbing carbon dioxide. "
    "Deforestation remains a major concern as tropical forests are cleared for agriculture and development.",

    "Fisheries provide food and livelihoods for billions of people worldwide. "
    "Overfishing has depleted many fish stocks, threatening marine ecosystems and food security. "
    "Aquaculture, or fish farming, now provides more than half of the fish consumed globally. "
    "Sustainable fisheries management aims to maintain healthy fish populations while supporting fishing communities.",

    "Mining extracts valuable minerals and materials from the Earth for industrial use. "
    "The mining industry faces challenges related to environmental impact, worker safety, and resource depletion. "
    "Recycling and urban mining recover valuable materials from electronic waste and other discarded products. "
    "Responsible mining practices seek to minimize ecological damage while meeting society material needs.",

    "Transportation systems move people and goods across cities, countries, and continents. "
    "Public transit, including buses, trains, and subways, reduces traffic congestion and emissions. "
    "Electric and autonomous vehicles promise to transform personal transportation in the coming decades. "
    "Infrastructure investment in roads, bridges, and rail networks is essential for economic development.",

    "Telecommunications networks form the backbone of modern information society. "
    "Mobile networks connect billions of people and enable mobile banking, health services, and education. "
    "Broadband internet access is increasingly considered a basic utility like electricity and water. "
    "Cybersecurity protects these critical networks from attacks that could disrupt essential services.",

    "Social media platforms have transformed how people communicate, share information, and form communities. "
    "Platforms like Facebook, Twitter, and Instagram connect users across geographical and cultural boundaries. "
    "Social media has enabled new forms of activism, entertainment, and business marketing. "
    "Concerns include privacy, mental health impacts, misinformation spread, and effects on democratic discourse.",

    "Data science combines statistics, computer science, and domain knowledge to extract insights from data. "
    "Big data analytics processes massive datasets to identify patterns and trends that inform decision-making. "
    "Machine learning algorithms automatically improve through experience with data. "
    "Data-driven approaches are transforming industries from healthcare to finance to manufacturing.",

    "Algorithms are step-by-step procedures for solving problems and performing computations. "
    "Efficient algorithms can solve complex problems in reasonable time while poor ones may be impractical. "
    "Computer science studies algorithm design, analysis, and optimization for various applications. "
    "From sorting and searching to graph traversal and optimization, algorithms form the core of computing.",

    "Programming languages provide the syntax and semantics for writing computer software. "
    "Different languages are suited for different tasks: Python for data science, JavaScript for web development, C++ for systems programming. "
    "Software engineering applies systematic methods to develop reliable and maintainable software systems. "
    "Agile development methodologies emphasize iterative development, collaboration, and rapid adaptation to change.",

    "Operating systems manage computer hardware and software resources and provide services for applications. "
    "They handle tasks like memory management, process scheduling, and file system organization. "
    "Popular operating systems include Windows, macOS, Linux, and mobile platforms like Android and iOS. "
    "Security features protect systems from malware, unauthorized access, and data breaches.",

    "Database systems organize, store, and retrieve large volumes of data efficiently. "
    "Relational databases use structured query language to manage tabular data with defined relationships. "
    "NoSQL databases handle unstructured data and scale horizontally across distributed systems. "
    "Data warehouses and analytics platforms enable business intelligence and data-driven decision-making.",

    "Compiler design translates source code written in programming languages into machine-executable instructions. "
    "The compilation process involves lexical analysis, parsing, optimization, and code generation phases. "
    "Modern compilers perform sophisticated optimizations to improve program performance. "
    "Compiler theory is a fundamental area of computer science with applications in language design and implementation.",

    "Quantum physics describes the behavior of matter and energy at atomic and subatomic scales. "
    "Particles exhibit wave-particle duality, behaving as both waves and particles depending on observation. "
    "Quantum entanglement creates correlations between particles that persist across any distance. "
    "These mysterious phenomena have no counterpart in classical physics and challenge our understanding of reality.",

    "Thermodynamics studies heat, work, temperature, and their relation to energy and entropy. "
    "The first law states that energy cannot be created or destroyed, only transformed. "
    "The second law introduces entropy, the measure of disorder that always increases in isolated systems. "
    "Thermodynamic principles govern everything from engine efficiency to biological metabolism.",

    "Electromagnetism describes the interaction between electrically charged particles. "
    "Electric fields surround charged particles while magnetic fields arise from moving charges. "
    "Electromagnetic waves, including light, radio waves, and X-rays, travel through space at the speed of light. "
    "Maxwell equations unify electricity and magnetism into a single coherent theory.",

    "Fluid dynamics studies the motion of liquids and gases and the forces acting on them. "
    "The Navier-Stokes equations describe viscous fluid flow but remain unsolved in the general case. "
    "Applications range from weather prediction and aircraft design to blood flow and ocean currents. "
    "Computational fluid dynamics uses numerical methods to simulate complex flow phenomena.",

    "Condensed matter physics studies the properties of solid and liquid matter. "
    "Phase transitions, superconductivity, and magnetism are key phenomena in this field. "
    "Understanding material properties enables the development of new technologies and devices. "
    "Research in this area has led to Nobel Prizes and transformative technological applications.",

    "Particle physics investigates the fundamental constituents of matter and their interactions. "
    "The Standard Model describes quarks, leptons, and force-carrying bosons that make up all known matter. "
    "Particle accelerators like the Large Hadron Collider smash particles together at near light speed. "
    "Discoveries include the Higgs boson, which gives mass to other fundamental particles.",

    "Astrophysics applies physics principles to understand celestial objects and phenomena. "
    "Stars generate energy through nuclear fusion of hydrogen into helium in their cores. "
    "Black holes are regions of spacetime where gravity is so strong that nothing can escape. "
    "The expansion of the universe, first observed by Edwin Hubble, continues to accelerate due to dark energy.",

    "Nuclear physics studies atomic nuclei, their constituents, and interactions. "
    "Nuclear fission splits heavy nuclei to release energy, while fusion combines light nuclei. "
    "Nuclear power plants generate electricity through controlled fission reactions. "
    "Research into controlled fusion promises virtually unlimited clean energy for the future.",

    "Organic chemistry studies carbon-containing compounds and their reactions. "
    "Carbon ability to form four bonds and create chains and rings makes it the basis of all known life. "
    "Organic reactions include substitution, elimination, addition, and rearrangement mechanisms. "
    "This field is essential for pharmaceuticals, polymers, dyes, and many other chemical products.",

    "Inorganic chemistry covers all chemical compounds except the myriad organic ones. "
    "It includes the study of metals, minerals, and organometallic compounds. "
    "Coordination chemistry examines how metal atoms bond with surrounding molecules called ligands. "
    "Inorganic compounds play crucial roles in catalysis, materials science, and biochemistry.",

    "Physical chemistry applies physics concepts to understand chemical systems and reactions. "
    "Chemical kinetics studies reaction rates while thermodynamics examines energy changes. "
    "Quantum chemistry uses quantum mechanics to model molecular structure and bonding. "
    "Spectroscopy analyzes how matter interacts with electromagnetic radiation to reveal molecular properties.",

    "Biochemistry studies chemical processes within living organisms. "
    "Enzymes catalyze biochemical reactions that sustain life, from digestion to DNA replication. "
    "Metabolism encompasses all chemical reactions that convert nutrients into energy and building blocks. "
    "Understanding biochemistry enables drug development, disease diagnosis, and biotechnology applications.",

    "Analytical chemistry develops methods to identify and quantify chemical substances. "
    "Techniques like chromatography, mass spectrometry, and spectroscopy separate and analyze mixtures. "
    "Quality control in manufacturing relies on accurate analytical measurements. "
    "Environmental monitoring uses analytical methods to detect pollutants and assess ecosystem health.",

    "Polymer chemistry focuses on the synthesis and properties of macromolecules. "
    "Polymers like plastics, rubber, and fibers are made of repeating monomer units. "
    "Understanding polymer structure-property relationships enables the design of materials with specific properties. "
    "Biodegradable polymers offer sustainable alternatives to conventional plastics that persist in the environment.",

    "Nanochemistry deals with the synthesis and characterization of materials at the nanometer scale. "
    "Nanoparticles exhibit unique optical, electrical, and catalytic properties different from bulk materials. "
    "Applications include targeted drug delivery, solar cells, and environmental remediation. "
    "Safety and environmental impacts of nanomaterials require careful evaluation and regulation.",

    "Environmental chemistry studies chemical processes occurring in the environment. "
    "It examines the sources, reactions, transport, and effects of chemical species in air, water, and soil. "
    "Pollution chemistry analyzes contaminants and their transformation pathways in ecosystems. "
    "Green chemistry develops chemical processes that minimize waste and reduce hazardous substances.",

    "Geochemistry applies chemistry to understand Earth processes and materials. "
    "It examines the distribution and cycling of elements in rocks, minerals, soils, water, and atmosphere. "
    "Isotope geochemistry uses radioactive decay to date geological materials and trace processes. "
    "Understanding geochemical cycles helps explain climate change, ore formation, and environmental problems.",

    "Algebra studies mathematical symbols and the rules for manipulating these symbols. "
    "From elementary equations to abstract algebraic structures like groups and rings, algebra provides powerful tools. "
    "Linear algebra deals with vectors, matrices, and linear transformations essential for many applications. "
    "Abstract algebra generalizes algebraic concepts to study mathematical structures systematically.",

    "Calculus studies continuous change through derivatives and integrals. "
    "Differential calculus analyzes rates of change while integral calculus computes accumulation of quantities. "
    "The fundamental theorem of calculus connects these two branches in a profound relationship. "
    "Calculus enables the modeling of dynamic systems in physics, engineering, economics, and biology.",

    "Geometry studies shapes, sizes, relative positions, and properties of space. "
    "From Euclidean geometry to differential and algebraic geometry, the field encompasses many branches. "
    "Topology, sometimes called rubber sheet geometry, studies properties preserved under continuous deformations. "
    "Geometric concepts are essential in architecture, engineering, computer graphics, and physics.",

    "Number theory studies properties and relationships of integers and integer-valued functions. "
    "Prime numbers, divisibility, and modular arithmetic are central topics in this ancient branch of mathematics. "
    "Cryptography relies on number-theoretic problems like factoring large numbers for security. "
    "Number theory has applications in computer science, coding theory, and cryptanalysis.",

    "Combinatorics is the mathematics of counting, arrangement, and combination. "
    "It addresses questions about how many ways objects can be selected, ordered, or partitioned. "
    "Graph theory, a related field, studies networks of vertices and edges with diverse applications. "
    "Combinatorial methods are essential in probability, algorithm analysis, and optimization problems.",

    "Probability theory provides a mathematical framework for analyzing random phenomena. "
    "It quantifies uncertainty and enables reasoning about events with incomplete information. "
    "Statistical inference uses probability to draw conclusions from data and test hypotheses. "
    "Bayesian methods update probabilities as new evidence becomes available.",

    "Statistics is the science of collecting, analyzing, interpreting, and presenting data. "
    "Descriptive statistics summarize data through measures like mean, median, and standard deviation. "
    "Inferential statistics uses sample data to make generalizations about larger populations. "
    "Statistical methods are essential in research, business, government, and many other fields.",

    "Differential equations describe relationships between functions and their derivatives. "
    "They model dynamic systems where quantities change continuously over time or space. "
    "Ordinary differential equations involve single-variable functions while partial differential equations involve multiple variables. "
    "Solving differential equations is fundamental to physics, engineering, biology, and economics.",

    "Classical music encompasses art music traditions from Western civilization. "
    "Composers like Bach, Mozart, and Beethoven created works of enduring beauty and complexity. "
    "Symphonies, concertos, sonatas, and operas represent major forms in the classical repertoire. "
    "Classical music continues to influence contemporary composers and performers worldwide.",

    "Jazz originated in African American communities in the early twentieth century. "
    "It blends African rhythmic traditions with European harmonic structures and instrumentation. "
    "Improvisation is a defining characteristic, allowing musicians to create spontaneous melodies. "
    "Legendary performers like Louis Armstrong, Duke Ellington, and Miles Davis shaped the genre evolution.",

    "Rock music emerged in the 1950s from blues, country, and rhythm and blues influences. "
    "It typically features electric guitars, bass, drums, and vocals in a band format. "
    "Subgenres include psychedelic rock, punk, metal, alternative, and indie rock. "
    "Rock has been a dominant force in popular culture, influencing fashion, attitudes, and social movements.",

    "Electronic music uses electronic instruments and technology for composition and performance. "
    "Synthesizers, drum machines, and computer software create sounds impossible with acoustic instruments. "
    "Genres include house, techno, trance, dubstep, and ambient electronic music. "
    "Electronic music festivals attract millions of fans and have become major cultural events.",

    "Hip hop culture encompasses music, dance, art, and fashion originating in African American communities. "
    "Rapping, DJing, breakdancing, and graffiti art are the four foundational elements of hip hop. "
    "Hip hop music has become one of the most popular and influential musical genres globally. "
    "The culture continues to evolve and influence mainstream art, fashion, and social commentary.",

    "Pop music is characterized by catchy melodies, accessible structures, and broad commercial appeal. "
    "It draws influences from many genres including rock, dance, electronic, and world music. "
    "Pop artists often collaborate with songwriters and producers to craft hit songs. "
    "The genre dominates charts and streaming platforms, reflecting contemporary cultural trends.",

    "Opera is a dramatic art form that combines music, singing, and theatrical performance. "
    "Originating in Italy around 1600, opera has produced masterworks by Verdi, Puccini, and Wagner. "
    "Operatic singing requires exceptional vocal technique and dramatic expression. "
    "Major opera houses worldwide continue to stage both classic and contemporary works.",

    "Ballet is a highly technical form of dance with its own vocabulary and aesthetic principles. "
    "It originated in Italian Renaissance courts and developed further in France and Russia. "
    "Classical ballet features precise movements, graceful gestures, and elaborate choreography. "
    "Modern ballet incorporates contemporary themes and experimental movement vocabulary.",

    "Theater is a collaborative art form that uses live performers to tell stories before an audience. "
    "It combines acting, directing, design, and technical elements to create dramatic experiences. "
    "From ancient Greek tragedies to contemporary experimental works, theater has evolved continuously. "
    "Musical theater integrates songs, dialogue, dance, and acting in popular productions.",

    "Painting is the practice of applying pigments to a surface to create images and expressions. "
    "Artists use various techniques including oil, watercolor, acrylic, and mixed media. "
    "From Renaissance masters to contemporary digital artists, painting continues to evolve as an art form. "
    "Major movements include Impressionism, Cubism, Surrealism, and Abstract Expressionism.",

    "Sculpture creates three-dimensional forms by carving, modeling, or assembling materials. "
    "Materials range from stone, metal, and wood to modern plastics and found objects. "
    "Sculptural techniques include subtractive carving, additive modeling, and assemblage. "
    "Public sculptures enhance urban spaces while gallery works explore artistic concepts.",

    "Photography captures and preserves images of reality using light and chemical or digital processes. "
    "From documentary to fine art, photography serves diverse purposes and aesthetic goals. "
    "Digital technology has transformed photography, enabling instant feedback and extensive manipulation. "
    "Photography has become a universal form of visual communication in the digital age.",

    "Film is a medium that combines visual storytelling with sound to create cinematic experiences. "
    "Directors, cinematographers, editors, and actors collaborate to bring stories to life on screen. "
    "Film genres include drama, comedy, action, horror, documentary, and science fiction. "
    "The evolution from silent films to digital cinema reflects technological and artistic advancement.",

    "Poetry uses concentrated language, rhythm, and imagery to express ideas and emotions. "
    "Forms range from sonnets and haiku to free verse and experimental poetry. "
    "Poetic devices include metaphor, simile, alliteration, and personification. "
    "Poetry has been a fundamental mode of human expression across all cultures and historical periods.",

    "The novel is a long work of fiction that explores characters, themes, and narratives. "
    "From classic works by Dickens and Tolstoy to contemporary bestsellers, novels entertain and illuminate. "
    "Literary fiction explores complex themes while genre fiction includes mystery, romance, and science fiction. "
    "The novel remains one of the most popular and influential literary forms worldwide.",

    "Philosophy of mind examines the nature of consciousness, thought, and mental states. "
    "Key debates address whether mind is identical to brain, whether consciousness is physical, and what personal identity involves. "
    "Thought experiments like the Chinese Room and Mary Room test theories about understanding and qualia. "
    "Philosophy of mind intersects with cognitive science, neuroscience, and artificial intelligence research.",

    "Ethics is the branch of philosophy that studies moral principles and values. "
    "It addresses questions about right and wrong, good and evil, justice and injustice. "
    "Major ethical theories include deontology, consequentialism, and virtue ethics. "
    "Applied ethics examines moral issues in specific fields like medicine, business, and environmental policy.",

    "Epistemology studies the nature, sources, and limits of knowledge and belief. "
    "Key questions include what knowledge is, how it is acquired, and what justifies belief. "
    "Rationalism emphasizes reason while empiricism emphasizes sensory experience. "
    "Contemporary epistemology addresses issues like skepticism, testimony, and epistemic justice.",

    "Metaphysics investigates the fundamental nature of reality and existence. "
    "It asks questions about what exists, what properties things have, and how entities relate. "
    "Topics include the nature of time, free will, possibility, and personal identity. "
    "Metaphysical inquiry intersects with physics, logic, and philosophy of mind.",

    "Logic studies the principles of valid reasoning and argumentation. "
    "Formal logic uses symbolic systems to analyze the structure of arguments. "
    "Informal logic examines everyday reasoning and fallacies. "
    "Logic provides foundational tools for mathematics, computer science, and philosophy.",

    "Aesthetics is the branch of philosophy dealing with beauty, art, and taste. "
    "It examines questions about the nature of aesthetic experience and judgment. "
    "Key concepts include beauty, sublimity, elegance, and artistic expression. "
    "Aesthetics intersects with psychology, sociology, and cultural studies.",

    "Political philosophy examines the nature of government, justice, rights, and law. "
    "It addresses questions about the ideal state, political obligation, and social contract. "
    "Thinkers like Locke, Rousseau, and Rawls have shaped modern political thought. "
    "Contemporary political philosophy addresses issues like equality, liberty, and global justice.",

    "Social philosophy studies society, social institutions, and their influence on individuals. "
    "It examines topics like class, race, gender, and social norms. "
    "Critical theory analyzes power structures and seeks human emancipation from oppression. "
    "Social philosophy intersects with sociology, psychology, and political theory.",

    "Existentialism emphasizes individual freedom, choice, and responsibility in an apparently meaningless universe. "
    "Key thinkers include Kierkegaard, Nietzsche, Heidegger, and Sartre. "
    "Existentialist themes appear in literature, psychology, and theology as well as philosophy. "
    "The philosophy confronts fundamental questions about meaning, anxiety, authenticity, and death.",

    "Stoicism is an ancient philosophy that teaches virtue, reason, and acceptance of fate. "
    "Stoics believed that wisdom comes from understanding what is within our control and what is not. "
    "The philosophy emphasizes living in accordance with nature and developing inner resilience. "
    "Stoic thinkers include Epictetus, Seneca, and Marcus Aurelius, whose writings remain widely read.",

    "Pragmatism is a philosophical tradition that evaluates theories based on their practical consequences. "
    "Developed by Peirce, James, and Dewey, pragmatism emphasizes action and problem-solving. "
    "It rejects the idea that knowledge is a passive mirror of nature, viewing it instead as a tool for action. "
    "Pragmatism has influenced education, politics, and the philosophy of science.",

    "Utilitarianism is an ethical theory that advocates actions producing the greatest good for the greatest number. "
    "Developed by Bentham and Mill, it focuses on consequences rather than intentions or rules. "
    "Utilitarian reasoning underlies cost-benefit analysis and public policy decision-making. "
    "Criticisms include concerns about justice, individual rights, and the measurement of happiness.",

    "Liberalism is a political philosophy emphasizing individual liberty, equality, and democratic governance. "
    "It supports free markets, civil rights, and limited government interference in personal affairs. "
    "Classical liberalism emphasizes economic freedom while social liberalism adds social justice concerns. "
    "Liberal democracy combines liberal principles with representative government and rule of law.",

    "Conservatism emphasizes tradition, social stability, and gradual change over radical reform. "
    "Conservatives generally value established institutions, family, religion, and national identity. "
    "The philosophy varies across cultures and time periods in its specific commitments. "
    "Contemporary conservatism addresses issues like immigration, globalization, and cultural change.",

    "Socialism advocates social ownership and democratic control of the means of production. "
    "It emphasizes equality, cooperation, and meeting basic needs over profit maximization. "
    "Socialist movements have influenced labor rights, welfare states, and economic policy worldwide. "
    "Democratic socialism seeks to achieve socialist goals through democratic political processes.",

    "Anarchism advocates the abolition of the state and all forms of hierarchical authority. "
    "Anarchists believe in voluntary cooperation, mutual aid, and direct action. "
    "The philosophy encompasses diverse traditions including anarcho-communism and anarcho-capitalism. "
    "Anarchist ideas have influenced social movements, labor struggles, and political theory.",

    "Organic chemistry studies the structure, properties, and reactions of carbon-containing compounds. "
    "Organic molecules form the basis of all living organisms and many important industrial materials. "
    "Reactions involve the breaking and forming of covalent bonds between carbon atoms and other elements. "
    "Understanding organic chemistry is essential for pharmaceuticals, plastics, and agricultural chemicals.",

    "Inorganic chemistry encompasses the study of all elements and compounds except those primarily based on carbon. "
    "This includes metals, minerals, and coordination compounds with diverse structures and properties. "
    "Catalysis, materials science, and bioinorganic chemistry are major research areas. "
    "Inorganic compounds serve important roles in industrial processes and biological systems.",

    "Physical chemistry applies physical principles to understand chemical phenomena. "
    "Thermochemistry, kinetics, quantum chemistry, and spectroscopy are major subdisciplines. "
    "Understanding energy changes, reaction rates, and molecular structure informs chemical applications. "
    "Physical chemistry bridges physics and chemistry, providing theoretical foundations for both fields.",

    "Biochemistry explores the chemical processes and substances that occur within living organisms. "
    "Proteins, nucleic acids, carbohydrates, and lipids are the major biomolecules studied. "
    "Enzyme kinetics, metabolic pathways, and signal transduction are key research areas. "
    "Biochemical knowledge underpins medicine, biotechnology, and our understanding of life itself.",

    "Analytical chemistry develops and applies methods to identify and quantify chemical substances. "
    "Chromatographic separation, spectroscopic detection, and electrochemical sensing are fundamental techniques. "
    "Quality assurance, environmental monitoring, and forensic science rely on analytical chemistry. "
    "Modern analytical chemistry increasingly uses automation and miniaturization for faster analysis.",

    "The periodic table organizes chemical elements by their atomic number and electron configuration. "
    "Groups share similar chemical properties while periods show trends in atomic size and reactivity. "
    "Elements range from hydrogen, the lightest, to synthetic superheavy elements. "
    "The table provides a powerful framework for understanding chemical behavior and predicting reactions.",

    "Chemical bonding holds atoms together in molecules and crystals. "
    "Ionic bonds involve electron transfer while covalent bonds share electrons between atoms. "
    "Metallic bonds delocalize electrons across a lattice of metal cations. "
    "Understanding bonding explains molecular geometry, reactivity, and material properties.",

    "Reaction kinetics studies how fast chemical reactions occur and what factors affect their rates. "
    "Rate laws describe the relationship between concentration and reaction speed. "
    "Catalysts accelerate reactions by providing alternative pathways with lower activation energy. "
    "Kinetic studies inform industrial process optimization and drug design.",

    "Equilibrium describes the state where forward and reverse reaction rates are equal. "
    "Le Chatelier principle predicts how equilibrium shifts in response to changes in conditions. "
    "Chemical equilibrium is essential for understanding acid-base chemistry, solubility, and complex ion formation. "
    "Industrial processes like ammonia synthesis exploit equilibrium principles for efficient production.",

    "Acids and bases are fundamental chemical species that react with each other in neutralization reactions. "
    "The pH scale measures acidity and alkalinity on a logarithmic scale. "
    "Buffer solutions resist changes in pH and are important in biological and industrial systems. "
    "Understanding acid-base chemistry is crucial for biochemistry, environmental science, and medicine.",

    "Electrochemistry studies chemical reactions that produce or are driven by electrical energy. "
    "Galvanic cells convert chemical energy to electricity while electrolytic cells use electricity to drive reactions. "
    "Batteries, fuel cells, and corrosion prevention are important applications. "
    "Electrochemical methods are used in analysis, synthesis, and environmental remediation.",

    "Thermochemistry examines heat changes in chemical reactions and physical processes. "
    "Enthalpy, entropy, and Gibbs free energy determine reaction spontaneity and equilibrium. "
    "Calorimetry measures heat flow while Hess law allows calculation of enthalpy changes. "
    "Thermochemical data informs energy production, materials processing, and environmental chemistry.",

    "Spectroscopy studies the interaction between matter and electromagnetic radiation. "
    "Different spectroscopic techniques probe molecular structure, composition, and dynamics. "
    "UV-visible, infrared, nuclear magnetic resonance, and mass spectrometry are widely used methods. "
    "Spectroscopic analysis is essential in chemistry, physics, biology, and materials science.",

    "Crystallography determines the arrangement of atoms in crystalline solids. "
    "X-ray diffraction reveals the three-dimensional structure of crystals and molecules. "
    "Crystal structures influence material properties like strength, conductivity, and optical behavior. "
    "Crystallographic techniques have solved structures of proteins, viruses, and many important materials.",

    "Chromatography separates mixtures based on differential partitioning between stationary and mobile phases. "
    "Gas chromatography, liquid chromatography, and thin-layer chromatography are common techniques. "
    "Chromatographic methods are essential in pharmaceutical analysis, environmental testing, and forensic science. "
    "High-performance and ultra-performance systems enable rapid, high-resolution separations.",

    "Mass spectrometry measures the mass-to-charge ratio of ions to identify and quantify molecules. "
    "Ionization techniques, mass analyzers, and detectors are key components of mass spectrometers. "
    "Tandem mass spectrometry provides structural information through fragmentation patterns. "
    "Applications include proteomics, metabolomics, drug testing, and environmental analysis.",

    "Nuclear magnetic resonance spectroscopy exploits the magnetic properties of certain atomic nuclei. "
    "NMR provides detailed information about molecular structure, dynamics, and chemical environment. "
    "Solution-state and solid-state NMR techniques serve different analytical needs. "
    "NMR is indispensable in chemistry, biochemistry, materials science, and medical imaging.",

    "Infrared spectroscopy measures the absorption of infrared radiation by molecular vibrations. "
    "Different functional groups absorb at characteristic frequencies, enabling molecular identification. "
    "Fourier transform infrared spectroscopy provides rapid, high-resolution spectral analysis. "
    "IR spectroscopy is widely used in qualitative analysis and quantitative determination.",

    "Ultraviolet-visible spectroscopy measures electronic transitions in molecules. "
    "Conjugated systems and transition metal complexes show characteristic absorption bands. "
    "Beer-Lambert law relates absorbance to concentration for quantitative analysis. "
    "UV-Vis spectroscopy is used in chemical analysis, biochemistry, and environmental monitoring.",

    "Fluorescence spectroscopy measures the emission of light by molecules after excitation. "
    "Fluorescent molecules and probes are widely used in biological research and medical diagnostics. "
    "Fluorescence microscopy enables high-resolution imaging of cellular structures and processes. "
    "Time-resolved fluorescence provides information about molecular dynamics and interactions.",

    "Raman spectroscopy measures inelastic scattering of light to probe molecular vibrations. "
    "It provides complementary information to infrared spectroscopy for molecular identification. "
    "Raman techniques require minimal sample preparation and can analyze aqueous solutions. "
    "Surface-enhanced Raman spectroscopy amplifies signals for trace analysis and nanomaterial characterization.",
]

FR_BLOCKS = [
    "L'intelligence artificielle a transformé de nombreuses industries au cours de la dernière décennie. "
    "Les algorithmes d'apprentissage automatique alimentent désormais les systèmes de recommandation, les véhicules autonomes et le diagnostic médical. "
    "Les réseaux neuronaux profonds ont atteint des performances supérieures à celles des humains dans la reconnaissance d'images et la compréhension du langage naturel. "
    "Les chercheurs continuent de repousser les limites de ce qui est possible avec l'intelligence computationnelle.",

    "Le changement climatique représente l'un des défis les plus pressants auxquels l'humanité est confrontée aujourd'hui. "
    "La hausse des températures mondiales provoque des événements météorologiques extrêmes plus fréquents, notamment ouragans, sécheresses et inondations. "
    "Les scientifiques avertissent que sans réductions significatives des émissions de gaz à effet de serre, des conséquences catastrophiques sont inévitables. "
    "Les sources d'énergie renouvelable comme le solaire et l'éolien offrent des alternatives viables aux combustibles fossiles.",

    "Le cerveau humain contient environ quatre-vingt-six milliards de neurones reliés par des billions de synapses. "
    "Chaque neurone communique avec les autres grâce à des impulsions électriques et à des messagers chimiques appelés neurotransmetteurs. "
    "La formation de la mémoire repose sur le renforcement des connexions synaptiques par un processus connu sous le nom de potentialisation à long terme. "
    "Les recherches en neurosciences continuent de révéler la remarquable complexité des circuits neuronaux.",

    "La révolution industrielle a commencé en Grande-Bretagne à la fin du dix-huitième siècle et a fondamentalement changé la fabrication. "
    "Les machines à vapeur alimentées au charbon ont permis aux usines de fonctionner indépendamment des rivières et du vent. "
    "Les filatures ont adopté des métiers à tisser mécaniques qui ont considérablement augmenté la production de tissu. "
    "Les chemins de fer ont relié les villes éloignées et facilité le transport de matières premières et de produits finis.",

    "L'informatique quantique exploite les principes de la mécanique quantique pour traiter l'information de nouvelles manières fondamentales. "
    "Contrairement aux bits classiques qui existent comme zéro ou un, les qubits peuvent exister en superposition des deux états simultanément. "
    "Cette propriété permet aux ordinateurs quantiques de résoudre certains problèmes exponentiellement plus rapidement que les machines classiques. "
    "Les grandes entreprises technologiques investissent des milliards de dollars dans la recherche et le développement quantiques.",

    "Internet trouve son origine dans un programme de recherche financé par le ministère américain de la défense dans les années soixante. "
    "Le réseau ARPANET utilise la commutation de paquets pour découper les messages en petits blocs qui voyagent indépendamment. "
    "Dans les années quatre-vingt, la suite de protocoles TCP/IP est devenue la norme pour l'interconnexion des réseaux différents. "
    "Le World Wide Web, inventé en 1990, a rendu Internet accessible aux gens ordinaires grâce aux navigateurs web.",

    "L'énergie solaire parvient sur Terre en quantités bien supérieures à la consommation actuelle de l'humanité. "
    "Les cellules photovoltaïques convertissent directement la lumière en électricité grâce à des matériaux semiconducteurs comme le silicium. "
    "Le coût des panneaux solaires a chuté de façon spectaculaire au cours des deux dernières décennies. "
    "De grandes centrales solaires alimentent désormais des villes entières, surtout dans les régions ensoleillées du monde.",

    "Les récifs coralliens couvrent moins d'un pour cent des fonds marins mais abritent environ un quart de toutes les espèces marines. "
    "Ils sont construits par de minuscules animaux appelés polypes coralliens qui sécrètent des squelettes de carbonate de calcium. "
    "La plupart des coraux constructeurs de récifs vivent en symbiose avec des algues microscopiques qui fournissent de l'énergie par photosynthèse. "
    "La hausse des températures de la mer provoque le blanchissement des coraux lorsque les polypes stressés expulsent leurs algues symbiotiques.",

    "La théorie de la tectonique des plaques explique le mouvement de la couche externe rigide de la Terre. "
    "Les continents dérivent sur les courants de convection du manteau chaud, se déplaçant de quelques centimètres par an. "
    "Là où les plaques se heurtent, des chaînes de montagnes s'élèvent ; là où elles s'écartent, une croûte océanique neuve se forme. "
    "Les séismes et les éruptions volcaniques se concentrent le long des frontières de plaques comme la ceinture de feu du Pacifique.",

    "Le café compte parmi les matières premières agricoles les plus échangées dans le monde. "
    "Les deux principales espèces cultivées sont l'arabica, apprécié pour sa douceur, et le robusta, plus riche en caféine. "
    "Les caféiers prospèrent sur les hauts plateaux tropicaux aux sols riches, avec des saisons sèches et humides marquées. "
    "Après la récolte, les grains sont séchés, torréfiés puis moulus avant d'être infusés pour obtenir la boisson populaire.",

    "L'apprentissage automatique est une branche de l'intelligence artificielle où les ordinateurs progressent par l'expérience. "
    "Au lieu de suivre des règles figées, les algorithmes ajustent leurs paramètres internes pour s'adapter aux données observées. "
    "L'apprentissage supervisé utilise des exemples étiquetés, tandis que le non supervisé découvre seul les structures cachées. "
    "Les réseaux de neurones profonds, connus sous le nom d'apprentissage profond, excellent dans le traitement des images, de la parole et du langage.",

    "L'exploration spatiale commence avec le lancement du satellite soviétique Spoutnik en 1957. "
    "Quatre ans plus tard, Youri Gagarine devient le premier homme à orbiter autour de la Terre. "
    "En 1969, des astronautes américains se posent sur la Lune dans le cadre du programme historique Apollo. "
    "Aujourd'hui, des sondes robotiques étudient les planètes lointaines pendant que les télescopes observent des galaxies.",

    "La génétique est la science qui étudie les gènes, la variation génétique et l'hérédité chez les organismes. "
    "C'est une branche importante de la biologie car l'hérédité est essentielle à l'évolution des organismes. "
    "Gregor Mendel, travaillant au dix-neuvième siècle, a été le premier à étudier la génétique scientifiquement. "
    "Il a observé que les organismes héritent des traits par des unités d'hérédité discrètes que nous appelons désormais gènes.",

    "La Renaissance a été une période de renouveau culturel et intellectuel en Europe. "
    "Elle se caractérisait par la redécouverte et la relance des réalisations de l'Antiquité classique en littérature et en art. "
    "Le mouvement a commencé en Italie et s'est propagé dans toute l'Europe au cours des siècles suivants. "
    "De grands artistes comme Léonard de Vinci et Michel-Ange ont produit des chefs-d'œuvre qui inspirent encore aujourd'hui.",

    "La photosynthèse est le processus par lequel les plantes vertes convertissent l'énergie lumineuse en énergie chimique. "
    "En utilisant la lumière du soleil, l'eau et le dioxyde de carbone, les plantes produisent du glucose et libèrent de l'oxygène. "
    "Ce processus est fondamental pour la vie sur Terre car il fournit la base de la plupart des chaînes alimentaires. "
    "La photosynthèse joue également un rôle crucial dans le maintien de la teneur en oxygène de l'atmosphère.",

    "La nanotechnologie consiste à manipuler la matière à l'échelle atomique et moléculaire. "
    "À des dimensions comprises entre un et cent nanomètres, les matériaux présentent des propriétés physiques et chimiques uniques. "
    "Les applications vont des systèmes d'administration de médicaments aux matériaux avancés pour l'électronique. "
    "Les chercheurs développent des dispositifs à l'échelle nanométrique qui pourraient révolutionner l'informatique et la médecine.",

    "L'économie mondiale est devenue de plus en plus interconnectée grâce au commerce et à la communication numérique. "
    "Les chaînes d'approvisionnement mondiales traversent plusieurs pays et impliquent des réseaux logistiques complexes. "
    "La croissance économique dépend de facteurs tels que l'investissement en capital, l'innovation technologique et l'éducation. "
    "Les gouvernements utilisent des politiques budgétaires et monétaires pour gérer les cycles économiques et promouvoir la stabilité.",

    "Les éruptions volcaniques se produisent lorsque la roche en fusion et les gaz s'échappent du sous-sol terrestre. "
    "Plusieurs types d'éruptions ont été classés par les volcanologues selon leurs caractéristiques. "
    "Certains volcans présentent des éruptions explosives tandis que d'autres produisent des coulées de lave paisibles. "
    "L'activité volcanique est concentrée le long des frontières de plaques où les plaques tectoniques se rencontrent ou s'écartent.",

    "Les antibiotiques sont des substances antimicrobiennes utilisées pour traiter les infections bactériennes chez l'homme et les animaux. "
    "Ils agissent en tuant directement les bactéries ou en inhibant leur croissance et leur reproduction. "
    "La découverte de la pénicilline par Alexander Fleming en 1928 a révolutionné la médecine moderne. "
    "Cependant, le problème croissant de la résistance aux antibiotiques menace d'annuler des décennies de progrès médicaux.",

    "Les mathématiques sont un domaine de connaissances concernant les concepts abstraits tels que les nombres et les formes. "
    "Elles utilisent le raisonnement logique et la preuve pour étudier et établir les propriétés des objets mathématiques. "
    "Les mathématiques sont essentielles pour modéliser et résoudre des problèmes en science, ingénierie et économie. "
    "De l'algèbre au calcul différentiel, les outils mathématiques forment la fondation de la société technologique moderne.",

    "La philosophie est une étude systématique des questions fondamentales sur l'existence, la connaissance et les valeurs. "
    "Elle utilise l'enquête rationnelle et l'analyse critique pour explorer des sujets comme l'esprit, la raison et le langage. "
    "Les philosophes débattent de la nature de la réalité et de la moralité depuis des milliers d'années. "
    "La discipline englobe des traditions diverses de la Grèce ancienne à la philosophie analytique contemporaine.",

    "L'astronomie est une science naturelle qui étudie les objets célestes et les phénomènes cosmiques. "
    "Elle utilise les mathématiques, la physique et la chimie pour expliquer l'origine et l'évolution de l'univers. "
    "Les objets d'intérêt incluent les planètes, les étoiles, les galaxies, les nébuleuses et les trous noirs. "
    "Les télescopes modernes peuvent observer la lumière d'objets situés à des milliards d'années-lumière de la Terre.",

    "La biologie est l'étude scientifique de la vie et des organismes vivants sous toutes leurs formes. "
    "Elle englobe un large éventail de domaines de la génétique moléculaire à l'écologie en passant par l'évolution. "
    "Les concepts centraux incluent la cellule comme unité de base de la vie et l'ADN comme porteur d'informations génétiques. "
    "La recherche biologique a conduit à des percées en médecine, agriculture et science environnementale.",

    "La chimie étudie la composition, la structure, les propriétés et les réactions de la matière. "
    "Elle est souvent appelée science centrale car elle relie la physique aux autres sciences naturelles. "
    "Les liaisons chimiques maintiennent les atomes ensemble dans les molécules et déterminent les propriétés des substances. "
    "Des médicaments aux polymères, la chimie crée des matériaux qui façonnent la civilisation moderne.",

    "La physique est la science naturelle la plus fondamentale, étudiant la matière, l'énergie et leurs interactions. "
    "Elle cherche à comprendre les lois qui régissent l'univers des particules subatomiques aux galaxies. "
    "Les domaines clés incluent la mécanique, la thermodynamique, l'électromagnétisme et la théorie quantique. "
    "La physique fournit la base théorique pour l'ingénierie, la technologie et de nombreuses disciplines scientifiques.",

    "La géographie étude les terres, les caractéristiques, les habitants et les phénomènes de la planète Terre. "
    "Elle combine la science physique avec la science sociale pour comprendre les interactions homme-environnement. "
    "Les géographes utilisent des outils comme les systèmes d'information géographique pour analyser les schémas spatiaux. "
    "La discipline fait le pont entre les sciences naturelles et les sciences sociales.",

    "La littérature englobe les œuvres écrites considérées comme ayant une valeur artistique ou intellectuelle. "
    "Elle comprend des genres tels que les romans, la poésie, le théâtre et les essais qui reflètent l'expérience humaine. "
    "Les œuvres littéraires préservent le patrimoine culturel et transmettent le savoir d'une génération à l'autre. "
    "Des épopées anciennes à la fiction contemporaine, la littérature façonne notre compréhension du monde.",

    "La musique est l'art d'organiser le son pour créer des expressions d'émotion et de beauté. "
    "C'est un universel culturel présent dans toutes les sociétés humaines tout au long de l'histoire. "
    "Les éléments musicaux incluent le rythme, la mélodie, l'harmonie et le timbre qui se combinent pour former des compositions. "
    "Des symphonies classiques à la musique populaire contemporaine, l'art sonore enrichit la culture humaine.",

    "La Révolution française a été une période de bouleversements politiques et sociaux radicaux en France. "
    "Elle a commencé en 1789 avec la prise de la Bastille et a conduit à la fin de la monarchie absolue. "
    "La révolution a proclamé les droits de l'homme et du citoyen et a établi une république. "
    "Ses idéaux de liberté, d'égalité et de fraternité ont influencé les mouvements politiques du monde entier.",

    "La Seconde Guerre mondiale a été le conflit le plus meurtrier de l'histoire humaine, impliquant des nations du monde entier. "
    "Le conflit a duré de 1939 à 1945 et a entraîné la mort d'environ soixante-dix millions de personnes. "
    "Les grandes puissances ont formé des alliances opposées : les Alliés se sont battus contre les nations de l'Axe. "
    "La guerre s'est terminée par la capitulation sans condition de l'Allemagne et du Japon après des bombardements atomiques dévastateurs.",

    "La démocratie est un système de gouvernement où le pouvoir est conféré au peuple. "
    "Les citoyens participent à la prise de décision directement ou par l'intermédiaire de représentants élus. "
    "Les principes démocratiques incluent les élections libres, l'État de droit, la protection des droits de l'homme et la liberté d'expression. "
    "Les démocraties varient considérablement dans leurs structures et pratiques à travers différents pays et cultures.",

    "L'évolution est le processus par lequel les espèces changent au fil des générations successives par sélection naturelle. "
    "Les organismes dotés de traits mieux adaptés à leur environnement tendent à survivre et à se reproduire avec plus de succès. "
    "Au fil de millions d'années, ce processus a produit l'incroyable diversité de la vie sur Terre. "
    "La théorie de l'évolution par sélection naturelle de Charles Darwin reste un pilier de la biologie moderne.",

    "Internet a transformé la façon dont les gens communiquent, travaillent et accèdent à l'information. "
    "Les plateformes de médias sociaux connectent des milliards d'utilisateurs à travers les frontières géographiques et culturelles. "
    "Le commerce électronique a révolutionné le commerce de détail en permettant les achats en ligne et les paiements numériques. "
    "Cependant, les préoccupations concernant la vie privée, la désinformation et la fracture numérique persistent.",

    "La mécanique quantique décrit le comportement de la matière et de l'énergie à plus petite échelle. "
    "Elle révèle que les particules peuvent exister dans plusieurs états simultanément jusqu'à ce qu'elles soient mesurées. "
    "Le principe d'incertitude stipule que certaines paires de propriétés physiques ne peuvent pas être connues avec précision. "
    "La théorie quantique a permis des technologies comme les lasers, les semi-conducteurs et l'imagerie par résonance magnétique.",

    "Les réseaux neuronaux artificiels sont des systèmes informatiques inspirés des réseaux neuronaux biologiques du cerveau. "
    "Ils se composent de nœuds interconnectés qui traitent l'information en utilisant des approches connexionnistes. "
    "Les modèles d'apprentissage profond à plusieurs couches ont obtenu des percées dans la reconnaissance de formes. "
    "Ces systèmes alimentent des applications des assistants vocaux à l'analyse d'images médicales.",

    "La révolution industrielle a transformé les économies agricoles en économies industrielles et manufacturières. "
    "De nouvelles inventions comme le Jenny spinning et le métier à tisser mécanique ont révolutionné la production textile. "
    "Le système des usines a remplacé les industries domestiques et a attiré les travailleurs des zones rurales vers les centres urbains. "
    "La révolution a apporté une croissance économique sans précédent mais aussi des problèmes sociaux.",

    "La science du climat examine les facteurs qui influencent les modèles climatiques de la Terre au fil du temps. "
    "Les gaz à effet de serre piègent la chaleur dans l'atmosphère, créant un effet de réchauffement qui s'intensifie. "
    "Les données des carottes de glace révèlent que les niveaux actuels de dioxyde de carbone sont plus élevés qu'à tout moment des 800 derniers millénaires. "
    "Les accords internationaux comme l'Accord de Paris visent à limiter le réchauffement mondial.",

    "Les neurosciences étudient la structure et le fonctionnement du système nerveux et du cerveau. "
    "Les techniques d'imagerie cérébrale permettent aux chercheurs d'observer l'activité neuronale en temps réel. "
    "Des études ont révélé comment différentes régions cérébrales se spécialisent dans des tâches comme le langage, la mémoire et l'émotion. "
    "La compréhension du cerveau pourrait mener à des traitements pour les troubles neurologiques.",

    "Les sources d'énergie renouvelable deviennent de plus en plus importantes pour le développement durable. "
    "Les systèmes photovoltaïques solaires convertissent la lumière du soleil directement en électricité avec une efficacité croissante. "
    "Les éoliennes exploitent l'énergie cinétique des courants aériens pour générer de l'électricité propre. "
    "Les barrages hydroélectriques utilisent l'eau qui coule pour produire de l'électricité tout en fournissant contrôle des inondations.",

    "Le génie génétique permet aux scientifiques de modifier des organismes en altérant leurs séquences d'ADN. "
    "Des techniques comme CRISPR-Cas9 permettent l'édition précise des gènes dans pratiquement tout organisme. "
    "Les applications incluent le développement de cultures résistantes aux maladies et le traitement des troubles génétiques. "
    "Cependant, les préoccupations éthiques concernant les bébés design et les impacts écologiques nécessitent une considération attentive.",

    "L'exploration spatiale a élargi notre compréhension du système solaire et de l'univers. "
    "Les missions de rovers sur Mars ont fourni des preuves d'eau ancienne et de vie passée potentielle. "
    "Le télescope spatial Hubble a capturé des images de galaxies formées peu après le Big Bang. "
    "Les futures missions visent à ramener des humains sur la Lune et éventuellement à envoyer des équipages vers Mars.",

    "L'architecture combine l'art et l'ingénierie pour concevoir des bâtiments et des structures. "
    "Les styles architecturaux reflètent les valeurs culturelles, les capacités technologiques et les conditions environnementales. "
    "Les principes de conception durable mettent désormais l'accent sur l'efficacité énergétique et la responsabilité environnementale. "
    "Des pyramides anciennes aux gratte-ciels modernes, l'architecture façonne l'environnement bâti que nous habitons.",

    "L'écologie étudie les interactions entre les organismes et leur environnement naturel. "
    "Les écosystèmes se composent de réseaux alimentaires complexes et de cycles de nutriments qui maintiennent l'équilibre biologique. "
    "La biodiversité fait référence à la variété des formes de vie au sein d'un écosystème, d'une région ou de la planète entière. "
    "Les activités humaines comme la déforestation et la pollution menacent la stabilité écologique et la survie des espèces.",

    "Les télécommunications permettent une communication instantanée à de grandes distances. "
    "Les câbles à fibres optiques transportent des données sous forme d'impulsions lumineuses à des vitesses proches de la vitesse de la lumière. "
    "Les réseaux satellitaires fournissent une couverture mondiale pour la diffusion, la navigation et l'accès à Internet. "
    "La cinquième génération de technologie mobile promet des vitesses plus rapides et une connectivité pour des milliards d'appareils.",

    "L'économie analyse comment les sociétés allouent des ressources rares pour satisfaire des besoins illimités. "
    "Les concepts clés incluent l'offre et la demande, l'équilibre du marché et le rôle de l'intervention gouvernementale. "
    "La microéconomie étudie les décisions individuelles tandis que la macroéconomie examine l'économie dans son ensemble. "
    "Les théories économiques aident les décideurs à comprendre l'inflation, le chômage et la croissance économique.",

    "La psychologie est l'étude scientifique de l'esprit et du comportement chez les humains et les animaux. "
    "Les psychologues utilisent des méthodes expérimentales, l'observation et l'analyse statistique pour comprendre les processus mentaux. "
    "Les perspectives majeures incluent la psychologie cognitive, comportementale, développementale et sociale. "
    "La psychologie appliquée aborde des questions pratiques comme la santé mentale et l'éducation.",

    "L'Union européenne est une union politique et économique de vingt-sept États membres. "
    "Elle a été établie pour promouvoir la paix, établir un marché économique unifié et renforcer la coopération européenne. "
    "Les membres de l'UE partagent une monnaie commune, l'euro, et ont éliminé de nombreuses barrières commerciales. "
    "L'union fait face à des défis incluant le Brexit, la politique de migration et le maintien de la gouvernance démocratique.",

    "L'éducation est le processus de facilitation de l'apprentissage et de l'acquisition de connaissances et de compétences. "
    "Les systèmes éducatifs varient considérablement d'un pays à l'autre dans leur structure et leurs méthodes. "
    "La technologie transforme l'éducation grâce aux plateformes d'apprentissage en ligne et aux ressources numériques. "
    "L'accès à une éducation de qualité reste un défi fondamental pour atteindre l'équité et la mobilité sociale.",

    "La santé publique se concentre sur la protection et l'amélioration de la santé des populations. "
    "La prévention des maladies, la promotion de la santé et les politiques de santé sont centrales. "
    "L'épidémiologie, l'étude des modèles de maladies dans les populations, éclaire les interventions de santé publique. "
    "Les défis mondiaux comme les pandémies nécessitent une coopération internationale coordonnée.",

    "La biotechnologie utilise des organismes vivants et des processus biologiques pour développer des produits. "
    "Les applications couvrent la médecine, l'agriculture, les procédés industriels et le remédiation environnementale. "
    "La production de biocarburants à partir d'algues et de bactéries offre des alternatives durables aux combustibles fossiles. "
    "La biotechnologie agricole a produit des cultures génétiquement modifiées avec un rendement amélioré.",

    "La technologie des semi-conducteurs est le fondement des appareils électroniques modernes. "
    "Les puces en silicium contenant des milliards de transistors alimentent ordinateurs, smartphones et innombrables appareils. "
    "La loi de Moore a prédit le doublement de la densité de transistors environ tous les deux ans. "
    "À mesure que les limites physiques approchent, les chercheurs explorent de nouveaux matériaux et architectures.",

    "La photonique est la science et la technologie de la génération, du contrôle et de la détection de la lumière. "
    "La technologie laser permet des applications de la fabrication de précision à la chirurgie médicale. "
    "Les communications par fibres optiques utilisent des signaux lumineux pour transmettre des données à des vitesses incroyablement élevées. "
    "Les capteurs photoniques fournissent des mesures sensibles dans des domaines allant du monitoring environnemental au diagnostic médical.",

    "L'urbanisme conçoit et gère l'aménagement physique des villes et des communautés. "
    "Une planification efficace équilibre le logement, le transport, les parcs et le développement commercial. "
    "La conception urbaine durable réduit l'impact environnemental tout en améliorant la qualité de vie. "
    "Les initiatives de ville intelligente utilisent la technologie pour optimiser les infrastructures et les services publics.",

    "La logistique gère les flux de biens, d'informations et de ressources de l'origine à la consommation. "
    "La gestion de la chaîne d'approvisionnement coordonne fournisseurs, fabricants, distributeurs et détaillants. "
    "Le commerce électronique a augmenté la demande pour des systèmes de livraison efficaces en milieu urbain. "
    "Des technologies avancées comme la robotique et l'intelligence artificielle transforment les opérations d'entrepôt.",

    "L'agriculture a nourri les populations humaines croissantes pendant des milliers d'années. "
    "L'agriculture moderne utilise la mécanisation, l'irrigation et les intrants chimiques pour maximiser les rendements. "
    "Les pratiques agricoles visent à maintenir la productivité tout en protégeant les ressources en sol et en eau. "
    "L'agriculture de précision utilise le GPS, les capteurs et l'analyse de données pour optimiser les opérations.",

    "La sylviculture gère les ressources forestières pour des bénéfices environnementaux, économiques et sociaux. "
    "La gestion durable des forêts équilibre la récolte de bois avec la conservation de la biodiversité. "
    "Les forêts jouent un rôle crucial dans le séquestration du carbone, aidant à atténuer le changement climatique. "
    "La déforestation reste une préoccupation majeure alors que les forêts tropicales sont défrichées pour l'agriculture.",

    "Les pêcheries fournissent de la nourriture et des moyens de subsistance à des milliards de personnes. "
    "La surpêche a épuisé de nombreux stocks de poissons, menaçant les écosystèmes marins et la sécurité alimentaire. "
    "L'aquaculture, ou pisciculture, fournit désormais plus de la moitié des poissons consommés dans le monde. "
    "La gestion durable des pêcheries vise à maintenir des populations de poissons saines.",

    "L'exploitation minière extrait des minéraux et matériaux précieux de la Terre pour un usage industriel. "
    "L'industrie minière fait face à des défis liés à l'impact environnemental et à l'épuisement des ressources. "
    "Le recyclage et l'exploitation minière urbaine récupèrent des matériaux précieux des déchets électroniques. "
    "Les pratiques minières responsables cherchent à minimiser les dommages écologiques.",

    "Les systèmes de transport déplacent les personnes et les biens à travers les villes, les pays et les continents. "
    "Le transport en commun, y compris bus, trains et métros, réduit la congestion et les émissions. "
    "Les véhicules électriques et autonomes promettent de transformer le transport personnel. "
    "L'investissement dans les infrastructures est essentiel pour le développement économique.",

    "Les réseaux de télécommunications forment l'épine dorsale de la société de l'information moderne. "
    "Les réseaux mobiles connectent des milliards de personnes et permettent la banque mobile et la santé mobile. "
    "L'accès à Internet à large bande est de plus en plus considéré comme une utilité de base. "
    "La cybersécurité protège ces réseaux critiques contre les attaques.",

    "Les plateformes de médias sociaux ont transformé la façon dont les gens communiquent et partagent l'information. "
    "Des plateformes comme Facebook, Twitter et Instagram connectent les utilisateurs à travers les frontières. "
    "Les médias sociaux ont permis de nouvelles formes d'activisme, de divertissement et de marketing. "
    "Les préoccupations incluent la vie privée, les impacts sur la santé mentale et la désinformation.",

    "La science des données combine statistiques, informatique et connaissances du domaine pour extraire des informations des données. "
    "L'analyse de big data traite des ensembles massifs de données pour identifier des tendances. "
    "Les algorithmes d'apprentissage automatique s'améliorent automatiquement grâce à l'expérience. "
    "Les approches basées sur les données transforment des industries de la santé à la finance.",

    "Les algorithmes sont des procédures pas à pas pour résoudre des problèmes et effectuer des calculs. "
    "Les algorithmes efficaces peuvent résoudre des problèmes complexes en un temps raisonnable. "
    "L'informatique étudie la conception, l'analyse et l'optimisation des algorithmes pour diverses applications. "
    "Du tri à la recherche en passant par l'optimisation, les algorithmes forment le cœur de l'informatique.",

    "Les langages de programmation fournissent la syntaxe et la sémantique pour écrire des logiciels. "
    "Différentes langages sont adaptés à différentes tâches : Python pour les données, JavaScript pour le web. "
    "Le génie logiciel applique des méthodes systématiques pour développer des logiciels fiables. "
    "Les méthodologies agiles soulignent le développement itératif et la collaboration.",

    "Les systèmes d'exploitation gèrent le matériel et les logiciels informatiques et fournissent des services aux applications. "
    "Ils gèrent des tâches comme la gestion de la mémoire, l'ordonnancement des processus et l'organisation des fichiers. "
    "Les systèmes d'exploitation populaires incluent Windows, macOS, Linux et les plateformes mobiles. "
    "Les fonctionnalités de sécurité protègent les systèmes contre les logiciels malveillants et les accès non autorisés.",

    "Les systèmes de bases de données organisent, stockent et récupèrent de grands volumes de données efficacement. "
    "Les bases de données relationnelles utilisent le langage SQL pour gérer des données tabulaires. "
    "Les bases NoSQL gèrent les données non structurées et s'échelonnent horizontalement. "
    "Les entrepôts de données et les plateformes d'analyse permettent l'intelligence économique.",

    "La conception de compilateurs traduit le code source en instructions exécutables par la machine. "
    "Le processus de compilation implique l'analyse lexicale, l'analyse syntaxique, l'optimisation et la génération de code. "
    "Les compilateurs modernes effectuent des optimisations sophistiquées pour améliorer les performances. "
    "La théorie des compilateurs est un domaine fondamental de l'informatique.",

    "La physique quantique décrit le comportement de la matière et de l'énergie à l'échelle atomique et subatomique. "
    "Les particules présentent une dualité onde-corpuscule, se comportant à la fois comme des ondes et des particules. "
    "L'intrication quantique crée des corrélations entre des particules qui persistent quelle que soit la distance. "
    "Ces phénomènes mystérieux n'ont pas d'équivalent en physique classique.",

    "La thermodynamique étudie la chaleur, le travail, la température et leur relation avec l'énergie et l'entropie. "
    "La première loi stipule que l'énergie ne peut être ni créée ni détruite, seulement transformée. "
    "La deuxième loi introduit l'entropie, la mesure du désordre qui augmente toujours dans les systèmes isolés. "
    "Les principes thermodynamiques régissent l'efficacité des moteurs et le métabolisme biologique.",

    "L'électromagnétisme décrit l'interaction entre les particules électriquement chargées. "
    "Les champs électriques entourent les particules chargées tandis que les champs magnétiques proviennent des charges en mouvement. "
    "Les ondes électromagnétiques, y compris la lumière, voyagent dans l'espace à la vitesse de la lumière. "
    "Les équations de Maxwell unifient l'électricité et le magnétisme en une seule théorie cohérente.",

    "La dynamique des fluides étudie le mouvement des liquides et des gaz et les forces qui les agissent. "
    "Les équations de Navier-Stokes décrivent l'écoulement de fluides visqueux mais restent non résolues en général. "
    "Les applications vont de la prévision météorologique à la conception d'avions en passant par le flux sanguin. "
    "La dynamique des fluides computationnelle utilise des méthodes numériques pour simuler des phénomènes complexes.",

    "La physique de la matière condensée étudie les propriétés de la matière solide et liquide. "
    "Les transitions de phase, la supraconductivité et le magnétisme sont des phénomènes clés. "
    "La compréhension des propriétés des matériaux permet le développement de nouvelles technologies. "
    "La recherche dans ce domaine a conduit à des prix Nobel et à des applications technologiques.",

    "La physique des particules étudie les constituants fondamentaux de la matière et leurs interactions. "
    "Le Modèle Standard décrit les quarks, les leptons et les bosons porteurs de force. "
    "Les accélérateurs de particules comme le Grand Collisionneur de hadrons percutent des particules. "
    "Les découvertes incluent le boson de Higgs qui donne de la masse aux particules fondamentales.",

    "L'astrophysique applique les principes de la physique pour comprendre les objets célestes. "
    "Les étoiles génèrent de l'énergie par la fusion nucléaire de l'hydrogène en hélium dans leurs cœurs. "
    "Les trous noirs sont des régions de l'espace-temps où la gravité est si forte que rien ne peut s'échapper. "
    "L'expansion de l'univers continue d'accélérer en raison de l'énergie sombre.",

    "La physique nucléaire étudie les noyaux atomiques, leurs constituants et leurs interactions. "
    "La fission nucléaire divise les noyaux lourds pour libérer de l'énergie, tandis que la fusion combine les noyaux légers. "
    "Les centrales nucléaires produisent de l'électricité par des réactions de fission contrôlées. "
    "La recherche sur la fusion contrôlée promet une énergie propre et illimitée pour l'avenir.",

    "La chimie organique étudie les composés contenant du carbone et leurs réactions. "
    "La capacité du carbone à former quatre liaisons et créer des chaînes et des cycles en fait la base de toute vie connue. "
    "Les réactions organiques incluent la substitution, l'élimination, l'addition et les réarrangements. "
    "Ce domaine est essentiel pour les médicaments, les polymères et les colorants.",

    "La chimie inorganique couvre tous les composés chimiques sauf les composés organiques. "
    "Elle inclut l'étude des métaux, des minéraux et des composés organométalliques. "
    "La chimie de coordination examine comment les atomes métalliques se lient aux molécules environnantes. "
    "Les composés inorganiques jouent des rôles cruciaux dans la catalyse et les sciences des matériaux.",

    "La chimie physique applique les concepts de la physique pour comprendre les systèmes chimiques. "
    "La cinétique chimique étudie les vitesses de réaction tandis que la thermodynamique examine les changements d'énergie. "
    "La chimie quantique utilise la mécanique quantique pour modéliser la structure moléculaire. "
    "La spectroscopie analyse comment la matière interagit avec le rayonnement électromagnétique.",

    "La biochimie étudie les processus chimiques au sein des organismes vivants. "
    "Les enzymes catalysent les réactions biochimiques qui soutiennent la vie, de la digestion à la réplication de l'ADN. "
    "Le métabolisme englobe toutes les réactions chimiques qui convertissent les nutriments en énergie. "
    "La compréhension de la biochimie permet le développement de médicaments et le diagnostic de maladies.",

    "La chimie analytique développe des méthodes pour identifier et quantifier les substances chimiques. "
    "Des techniques comme la chromatographie, la spectrométrie de masse et la spectroscopie séparent et analysent les mélanges. "
    "Le contrôle qualité en fabrication repose sur des mesures analytiques précises. "
    "Le monitoring environnemental utilise des méthodes analytiques pour détecter les polluants.",

    "La chimie des polymères se concentre sur la synthèse et les propriétés des macromolécules. "
    "Les polymères comme les plastiques, le caoutchouc et les fibres sont composés d'unités monomères répétitives. "
    "La compréhension des relations structure-propriétés permet la conception de matériaux spécifiques. "
    "Les polymères biodégradables offrent des alternatives durables aux plastiques conventionnels.",

    "La nanochimie traite de la synthèse et de la caractérisation de matériaux à l'échelle du nanomètre. "
    "Les nanoparticules présentent des propriétés optiques, électriques et catalytiques uniques. "
    "Les applications incluent l'administration ciblée de médicaments, les cellules solaires et le remédiation environnementale. "
    "Les impacts sur la santé et l'environnement des nanomatériaux nécessitent une évaluation attentive.",

    "La chimie environnementale étudie les processus chimiques se produisant dans l'environnement. "
    "Elle examine les sources, réactions, transport et effets des espèces chimiques dans l'air, l'eau et le sol. "
    "La chimie de la pollution analyse les contaminants et leurs voies de transformation. "
    "La chimie verte développe des procédés chimiques qui minimisent les déchets et réduisent les substances dangereuses.",

    "La géochimie applique la chimie pour comprendre les processus et matériaux terrestres. "
    "Elle examine la distribution et le cycle des éléments dans les roches, minéraux, sols, eau et atmosphère. "
    "La géochimie isotopique utilise la désintégration radioactive pour dater les matériaux géologiques. "
    "La compréhension des cycles géochimiques aide à expliquer le changement climatique et la formation de minerais.",

    "L'algèbre étudie les symboles mathématiques et les règles pour manipuler ces symboles. "
    "Des équations élémentaires aux structures algébriques abstraites comme les groupes et les anneaux, l'algèbre fournit des outils puissants. "
    "L'algèbre linéaire traite des vecteurs, matrices et transformations linéaires essentielles pour de nombreuses applications. "
    "L'algèbre abstraite généralise les concepts algébriques pour étudier les structures mathématiques.",

    "Le calcul différentiel et intégral étudie le changement continu à travers les dérivées et les intégrales. "
    "Le calcul différentiel analyse les taux de changement tandis que le calcul intégral calcule l'accumulation. "
    "Le théorème fondamental du calcul relie ces deux branches dans une relation profonde. "
    "Le calcul permet la modélisation des systèmes dynamiques en physique, ingénierie et biologie.",

    "La géométrie étudie les formes, les tailles, les positions relatives et les propriétés de l'espace. "
    "De la géométrie euclidienne à la géométrie différentielle, le domaine englobe de nombreuses branches. "
    "La topologie, parfois appelée géométrie en caoutchouc, étudie les propriétés préservées sous déformations continues. "
    "Les concepts géométriques sont essentiels en architecture, en infographie et en physique.",

    "La théorie des nombres étudie les propriétés des entiers et des fonctions à valeurs entières. "
    "Les nombres premiers, la divisibilité et l'arithmodulaire sont des sujets centraux. "
    "La cryptographie repose sur des problèmes de théorie des nombres comme la factorisation de grands nombres. "
    "La théorie des nombres a des applications en informatique et en théorie du codage.",

    "La combinatoire est les mathématiques du comptage, de l'arrangement et de la combinaison. "
    "Elle traite des questions sur le nombre de façons dont les objets peuvent être sélectionnés ou ordonnés. "
    "La théorie des graphes, un domaine lié, étudie les réseaux de sommets et d'arêtes. "
    "Les méthodes combinatoires sont essentielles en probabilité et en optimisation.",

    "La théorie des probabilités fournit un cadre mathématique pour analyser les phénomènes aléatoires. "
    "Elle quantifie l'incertitude et permet le raisonnement sur des événements avec des informations incomplètes. "
    "L'inférence statistique utilise les probabilités pour tirer des conclusions des données. "
    "Les méthodes bayésiennes mettent à jour les probabilités lorsque de nouvelles preuves sont disponibles.",

    "Les statistiques sont la science de collecter, analyser, interpréter et présenter des données. "
    "Les statistiques descriptives résument les données par des mesures comme la moyenne et l'écart-type. "
    "Les statistiques inférentielles utilisent des échantillons pour faire des généralisations. "
    "Les méthodes statistiques sont essentielles dans la recherche, les affaires et le gouvernement.",

    "Les équations différentielles décrivent les relations entre les fonctions et leurs dérivées. "
    "Elles modélisent les systèmes dynamiques où les quantités changent continuellement. "
    "Les équations différentielles ordinaires impliquent des fonctions à une variable tandis que les partielles en impliquent plusieurs. "
    "La résolution des équations différentielles est fondamentale en physique et en ingénierie.",

    "La musique classique englobe les traditions de musique savante de la civilisation occidentale. "
    "Des compositeurs comme Bach, Mozart et Beethoven ont créé des œuvres d'une beauté durable. "
    "Symphonies, concertos, sonates et opéras représentent les principales formes du répertoire classique. "
    "La musique classique continue d'influencer les compositeurs et interprètes du monde entier.",

    "Le jazz est né dans les communautés afro-américaines au début du vingtième siècle. "
    "Il mélange les traditions rythmiques africaines avec les structures harmoniques européennes. "
    "L'improvisation est une caractéristique déterminante, permettant aux musiciens de créer des mélodies spontanées. "
    "Des artistes légendaires comme Louis Armstrong et Duke Ellington ont façonné le genre.",

    "La musique rock a émergé dans les années 1950 à partir du blues, du country et du rhythm and blues. "
    "Elle présente généralement des guitares électriques, une basse, des batteries et des voix dans un format groupe. "
    "Les sous-genres incluent le rock psychédélique, le punk, le métal et le rock alternatif. "
    "Le rock a été une force dominante dans la culture populaire, influençant la mode et les mouvements sociaux.",

    "La musique électronique utilise des instruments électroniques et la technologie pour la composition et l'exécution. "
    "Les synthétiseurs, boîtes à rythmes et logiciels informatiques créent des sons impossibles avec des instruments acoustiques. "
    "Les genres incluent la house, la techno, la trance et la musique électronique ambiante. "
    "Les festivals de musique électronique attirent des millions de fans.",

    "Le hip-hop englobe la musique, la danse, l'art et la mode originating dans les communautés afro-américaines. "
    "Le rap, le DJing, le breakdance et le graffiti art sont les quatre éléments fondamentaux. "
    "La musique hip-hop est devenue l'un des genres les plus populaires au monde. "
    "La culture continue d'évoluer et d'influencer l'art mainstream et le commentaire social.",

    "La musique pop est caractérisée par des mélodies accrocheuses, des structures accessibles et un large attrait commercial. "
    "Elle s'inspire de nombreux genres incluant le rock, la danse et la musique électronique. "
    "Les artistes pop collaborent souvent avec des auteurs-compositeurs pour créer des tubes. "
    "Le genre domine les classements et les plateformes de streaming.",

    "L'opéra est une forme dramatique qui combine musique, chant et performance théâtrale. "
    "Né en Italie autour de 1600, l'opéra a produit des chefs-d'œuvre de Verdi, Puccini et Wagner. "
    "Le chant lyrique nécessite une technique vocale exceptionnelle et une expression dramatique. "
    "Les grandes maisons d'opéra continuent de monter des œuvres classiques et contemporaines.",

    "Le ballet est une forme de danse très technique avec son propre vocabulaire et ses principes esthétiques. "
    "Il est originaire des cours italiennes de la Renaissance et s'est développé en France et en Russie. "
    "Le ballet classique présente des mouvements précis, des gestes gracieux et une chorégraphie élaborée. "
    "Le ballet moderne intègre des thèmes contemporains et un vocabulaire de mouvement expérimental.",

    "Le théâtre est une forme d'art collaborative qui utilise des artistes vivants pour raconter des histoires. "
    "Il combine la mise en scène, la direction, la conception et les éléments techniques. "
    "Des tragédies grecques aux œuvres expérimentales contemporaines, le théâtre a évolué continuellement. "
    "Le théâtre musical intègre chansons, dialogues, danse et acting dans des productions populaires.",

    "La peinture est la pratique d'appliquer des pigments sur une surface pour créer des images. "
    "Les artistes utilisent diverses techniques incluant l'huile, l'aquarelle, l'acrylique et les médias mixtes. "
    "Des maîtres de la Renaissance aux artistes numériques contemporains, la peinture continue d'évoluer. "
    "Les mouvements majeurs incluent l'impressionnisme, le cubisme, le surréalisme et l'expressionnisme abstrait.",

    "La sculpture crée des formes tridimensionnelles en sculptant, modelant ou assemblant des matériaux. "
    "Les matériaux vont de la pierre, du métal et du bois aux plastiques modernes et objets trouvés. "
    "Les techniques sculpturales incluent la taille soustractive, le modelage additif et l'assemblage. "
    "Les sculptures publiques embellissent les espaces urbains tandis que les œuvres de galerie explorent des concepts artistiques.",

    "La photographie capture et préserve des images de la réalité en utilisant la lumière. "
    "Du documentaire aux beaux-arts, la photographie sert des objectifs esthétiques divers. "
    "La technologie numérique a transformé la photographie, permettant un retour instantané. "
    "La photographie est devenue une forme universelle de communication visuelle à l'ère numérique.",

    "Le cinéma est un medium qui combine le storytelling visuel avec le son. "
    "Les réalisateurs, directeurs de la photographie, monteurs et acteurs collaborent pour donner vie à des histoires. "
    "Les genres cinématographiques incluent le drame, la comédie, l'action, l'horreur et le documentaire. "
    "L'évolution du cinéma muet au cinéma numérique reflète l'avancement technologique.",

    "La poésie utilise un langage concentré, un rythme et des images pour exprimer des idées et des émotions. "
    "Les formes vont des sonnets et du haïku en vers libre et de la poésie expérimentale. "
    "Les dispositifs poétiques incluent la métaphore, la similitude, l'allitération et la personnification. "
    "La poésie a été un mode fondamental d'expression humaine à travers toutes les cultures.",

    "Le roman est une œuvre de fiction longue qui explore des personnages, des thèmes et des récits. "
    "Des œuvres classiques de Dickens et Tolstoï aux best-sellers contemporains, les romans divertissent et éclairent. "
    "La fiction littéraire explore des thèmes complexes tandis que la fiction de genre inclut le mystère et la science-fiction. "
    "Le roman reste l'une des formes littéraires les plus populaires et influentes dans le monde.",

    "La philosophie de l'esprit examine la nature de la conscience, de la pensée et des états mentaux. "
    "Les débats clés portent sur l'identité de l'esprit et du cerveau, la physicalité de la conscience et l'identité personnelle. "
    "Les expériences de pensée comme la Chinoise et la Chambre de Mary testent les théories sur la compréhension. "
    "La philosophie de l'esprit intersecte les sciences cognitives, les neurosciences et l'intelligence artificielle.",

    "L'éthique est la branche de la philosophie qui étudie les principes moraux et les valeurs. "
    "Elle traite des questions sur le bien et le mal, la justice et l'injustice. "
    "Les grandes théories éthiques incluent le déontologisme, le conséquentialisme et l'éthique de la vertu. "
    "L'éthique appliquée examine les questions morales dans des domaines spécifiques comme la médecine.",

    "L'épistémologie étudie la nature, les sources et les limites de la connaissance et de la croyance. "
    "Les questions clés incluent ce qu'est la connaissance, comment elle est acquise et ce qui justifie la croyance. "
    "Le rationalisme met l'accent sur la raison tandis que l'empirisme souligne l'expérience sensorielle. "
    "L'épistémologie contemporaine aborde le scepticisme et la justice épistémique.",

    "La métaphysique investigate la nature fondamentale de la réalité et de l'existence. "
    "Elle pose des questions sur ce qui existe, quelles propriétés ont les choses et comment les entités se rapportent. "
    "Les sujets incluent la nature du temps, le libre arbitre, la possibilité et l'identité personnelle. "
    "L'enquête métaphysique intersecte la physique, la logique et la philosophie de l'esprit.",

    "La logique étudie les principes du raisonnement valide et de l'argumentation. "
    "La logique formelle utilise des systèmes symboliques pour analyser la structure des arguments. "
    "La logique informelle examine le raisonnement quotidien et les sophismes. "
    "La logique fournit des outils fondamentaux pour les mathématiques, l'informatique et la philosophie.",

    "L'esthétique est la branche de la philosophie traitant de la beauté, de l'art et du goût. "
    "Elle examine des questions sur la nature de l'expérience esthétique et du jugement. "
    "Les concepts clés incluent la beauté, le sublime, l'élégance et l'expression artistique. "
    "L'esthétique intersecte la psychologie, la sociologie et les études culturelles.",

    "La philosophie politique examine la nature du gouvernement, de la justice, des droits et de la loi. "
    "Elle traite des questions sur l'État idéal, l'obligation politique et le contrat social. "
    "Des penseurs comme Locke, Rousseau et Rawls ont façonné la pensée politique moderne. "
    "La philosophie politique contemporaine aborde l'égalité, la liberté et la justice mondiale.",

    "La philosophie sociale étudie la société, les institutions sociales et leur influence sur les individus. "
    "Elle examine des sujets comme la classe, la race, le genre et les normes sociales. "
    "La théorie critique analyse les structures de pouvoir et cherche l'émancipation humaine. "
    "La philosophie sociale intersecte la sociologie, la psychologie et la théorie politique.",

    "L'existentialisme met l'accent sur la liberté individuelle, le choix et la responsabilité dans un univers apparemment dépourvu de sens. "
    "Les penseurs clés incluent Kierkegaard, Nietzsche, Heidegger et Sartre. "
    "Les thèmes existentialistes apparaissent en littérature, en psychologie et en théologie. "
    "La philosophie confronte des questions fondamentales sur le sens, l'anxiété et l'authenticité.",

    "Le stoïcisme est une philosophie ancienne qui enseigne la vertu, la raison et l'acceptation du destin. "
    "Les stoïciens croyaient que la sagesse vient de comprendre ce qui est en notre contrôle et ce qui ne l'est pas. "
    "La philosophie met l'accent sur la vie en accord avec la nature et le développement de la résilience intérieure. "
    "Des penseurs stoïciens comme Épictète, Sénèque et Marc Aurèle continuent d'être largement lus.",

    "Le pragmatisme est une tradition philosophique qui évalue les théories par leurs conséquences pratiques. "
    "Développé par Peirce, James et Dewey, le pragmatisme souligne l'action et la résolution de problèmes. "
    "Il rejette l'idée que la connaissance est un miroir passif de la nature, la voyant comme un outil d'action. "
    "Le pragmatisme a influencé l'éducation, la politique et la philosophie des sciences.",

    "L'utilitarisme est une théorie éthique qui préconise les actions produisant le plus grand bien pour le plus grand nombre. "
    "Développé par Bentham et Mill, il se concentre sur les conséquences plutôt que sur les intentions. "
    "Le raisonnement utilitariste sous-tend l'analyse coûts-avantages et la prise de décision publique. "
    "Les critiques incluent des préoccupations sur la justice et les droits individuels.",

    "Le libéralisme est une philosophie politique mettant l'accent sur la liberté individuelle, l'égalité et la gouvernance démocratique. "
    "Il soutient les marchés libres, les droits civils et la limitation de l'ingérence gouvernementale. "
    "Le libéralisme classique met l'accent sur la liberté économique tandis que le libéralisme social ajoute la justice sociale. "
    "La démocratie libérale combine les principes libéraux avec un gouvernement représentatif.",

    "Le conservatisme met l'accent sur la tradition, la stabilité sociale et le changement graduel. "
    "Les conservateurs valoriser généralement les institutions établies, la famille, la religion et l'identité nationale. "
    "La philosophie varie selon les cultures et les époques dans ses engagements spécifiques. "
    "Le conservatisme contemporain aborde l'immigration, la mondialisation et le changement culturel.",

    "Le socialisme préconise la propriété sociale et le contrôle démocratique des moyens de production. "
    "Il met l'accent sur l'égalité, la coopération et la satisfaction des besoins fondamentaux. "
    "Les mouvements socialistes ont influencé les droits du travail et les États providence dans le monde. "
    "Le socialisme démocratique cherche à atteindre les objectifs socialistes par des processus politiques démocratiques.",

    "L'anarchisme préconise l'abolition de l'État et de toutes les formes d'autorité hiérarchique. "
    "Les anarchistes croient en la coopération volontaire, l'entraide et l'action directe. "
    "La philosophie englobe des traditions diverses incluant l'anarcho-communisme et l'anarcho-capitalisme. "
    "Les idées anarchistes ont influencé les mouvements sociaux et la théorie politique.",

    "La chimie organique étudie la structure, les propriétés et les réactions des composés contenant du carbone. "
    "Les molécules organiques forment la base de tous les organismes vivants et de nombreux matériaux industriels. "
    "Les réactions impliquent la rupture et la formation de liaisons covalentes entre atomes de carbone. "
    "La compréhension de la chimie organique est essentielle pour les médicaments et les plastiques.",

    "La chimie inorganique englobe l'étude de tous les éléments et composés excepté ceux basés sur le carbone. "
    "Cela inclut les métaux, les minéraux et les composés de coordination avec des structures diverses. "
    "La catalyse, les sciences des matériaux et la chimie bioinorganique sont des domaines de recherche majeurs. "
    "Les composés inorganiques jouent des rôles importants dans les procédés industriels et biologiques.",

    "La chimie physique applique les principes physiques pour comprendre les phénomènes chimiques. "
    "La thermochimie, la cinétique, la chimie quantique et la spectroscopie sont des sous-disciplines majeures. "
    "La compréhension des changements d'énergie, des vitesses de réaction et de la structure moléculaire informe les applications chimiques. "
    "La chimie physique fait le pont entre la physique et la chimie.",

    "La biochimie explore les processus et substances chimiques qui se produisent au sein des organismes vivants. "
    "Les protéines, acides nucléiques, glucides et lipides sont les principales biomolécules étudiées. "
    "La cinétique enzymatique, les voies métaboliques et la transduction de signaux sont des domaines clés. "
    "Les connaissances biochimiques soutiennent la médecine et la biotechnologie.",

    "La chimie analytique développe et applique des méthodes pour identifier et quantifier les substances chimiques. "
    "La séparation chromatographique, la détection spectroscopique et le capteur électrochimique sont des techniques fondamentales. "
    "L'assurance qualité, le monitoring environnemental et la science forensique reposent sur la chimie analytique. "
    "La chimie analytique moderne utilise de plus en plus l'automatisation et la miniaturisation.",

    "Le tableau périodique organise les éléments chimiques par leur numéro atomique et leur configuration électronique. "
    "Les groupes partagent des propriétés chimiques similaires tandis que les périodes montrent des tendances. "
    "Les éléments vont de l'hydrogène, le plus léger, aux éléments superlourds synthétiques. "
    "Le tableau fournit un cadre puissant pour comprendre le comportement chimique.",

    "La liaison chimique maintient les atomes ensemble dans les molécules et les cristaux. "
    "Les liaisons ioniques impliquent le transfert d'électrons tandis que les liaisons covalentes partagent des électrons. "
    "Les liaisons métalliques délocalisent les électrons à travers un réseau de cations métalliques. "
    "La compréhension des liaisons explique la géométrie moléculaire et les propriétés des matériaux.",

    "La cinétique chimique étudie la vitesse des réactions chimiques et les facteurs qui les affectent. "
    "Les lois de vitesse décrivent la relation entre la concentration et la vitesse de réaction. "
    "Les catalyseurs accélèrent les réactions en fournissant des voies alternatives à plus basse énergie. "
    "Les études cinétiques informent l'optimisation des procédés industriels.",

    "L'équilibre décrit l'état où les vitesses des réactions directe et inverse sont égales. "
    "Le principe de Le Chatelier prédit comment l'équilibre se déplace en réponse aux changements. "
    "L'équilibre chimique est essentiel pour comprendre la chimie acido-basique et la solubilité. "
    "Les procédés industriels comme la synthèse d'ammoniaque exploitent les principes d'équilibre.",

    "Les acides et les bases sont des espèces chimiques fondamentales qui réagissent entre elles. "
    "L'échelle pH mesure l'acidité et l'alcalinité sur une échelle logarithmique. "
    "Les solutions tampons résistent aux changements de pH et sont importantes en biologie. "
    "La compréhension de la chimie acido-basique est cruciale pour la biochimie et la médecine.",

    "L'électrochimie étudie les réactions chimiques qui produisent ou sont alimentées par de l'énergie électrique. "
    "Les piles galvaniques convertissent l'énergie chimique en électricité tandis que les cellules électrolytiques utilisent l'électricité. "
    "Les batteries, les piles à combustible et la prévention de la corrosion sont des applications importantes. "
    "Les méthodes électrochimiques sont utilisées dans l'analyse et la synthèse.",

    "La thermochimie examine les changements de chaleur dans les réactions chimiques et les processus physiques. "
    "L'enthalpie, l'entropie et l'énergie libre de Gibbs déterminent la spontanéité des réactions. "
    "La calorimétrie mesure le flux de chaleur tandis que la loi de Hess permet le calcul des variations d'enthalpie. "
    "Les données thermochimiques informent la production d'énergie et le traitement des matériaux.",

    "La spectroscopie étudie l'interaction entre la matière et le rayonnement électromagnétique. "
    "Différentes techniques spectroscopiques sondent la structure moléculaire et la dynamique. "
    "La spectroscopie UV-visible, infrarouge, RMN et spectrométrie de masse sont largement utilisées. "
    "L'analyse spectroscopique est essentielle en chimie, physique et biologie.",

    "La cristallographie détermine l'arrangement des atomes dans les solides cristallins. "
    "La diffraction des rayons X révèle la structure tridimensionnelle des cristaux et des molécules. "
    "Les structures cristallines influencent les propriétés des matériaux comme la résistance et la conductivité. "
    "Les techniques cristallographiques ont résolu des structures de protéines et de virus.",

    "La chromatographie sépare les mélanges basé sur le partage différentiel entre phases stationnaire et mobile. "
    "La chromatographie gazeuse, liquide et en couche mince sont des techniques courantes. "
    "Les méthodes chromatographiques sont essentielles dans l'analyse pharmaceutique et environnementale. "
    "Les systèmes haute performance permettent des séparations rapides et à haute résolution.",

    "La spectrométrie de masse mesure le rapport masse-charge des ions pour identifier les molécules. "
    "Les techniques d'ionisation, les analyseurs de masse et les détecteurs sont des composants clés. "
    "La spectrométrie de masse en tandem fournit des informations structurales par fragmentation. "
    "Les applications incluent la protéomique, la métabolomique et les tests de drogues.",

    "La spectroscopie RMN exploite les propriétés magnétiques de certains noyaux atomiques. "
    "La RMN fournit des informations détaillées sur la structure moléculaire et l'environnement chimique. "
    "Les techniques RMN en solution et à l'état solide servent des besoins analytiques différents. "
    "La RMN est indispensable en chimie, biochimie et imagerie médicale.",

    "La spectroscopie infrarouge mesure l'absorption du rayonnement infrarouge par les vibrations moléculaires. "
    "Les différents groupes fonctionnels absorbent à des fréquences caractéristiques, permettant l'identification moléculaire. "
    "La spectroscopie infrarouge à transformée de Fourier fournit une analyse rapide et à haute résolution. "
    "La spectroscopie IR est largement utilisée pour l'analyse qualitative et quantitative.",

    "La spectroscopie ultraviolet-visible mesure les transitions électroniques dans les molécules. "
    "Les systèmes conjugués et les complexes de métaux de transition présentent des bandes d'absorption caractéristiques. "
    "La loi de Beer-Lambert relie l'absorbance à la concentration pour l'analyse quantitative. "
    "La spectroscopie UV-Vis est utilisée en chimie, biochimie et monitoring environnemental.",

    "La spectroscopie de fluorescence mesure l'émission de lumière par les molécules après excitation. "
    "Les molécules et sondes fluorescentes sont largement utilisées en recherche biologique et diagnostic médical. "
    "La microscopie à fluorescence permet l'imagerie à haute résolution des structures cellulaires. "
    "La fluorescence résolue temporellement fournit des informations sur la dynamique moléculaire.",

    "La spectroscopie Raman mesure la diffusion inélastique de la lumière pour sonder les vibrations moléculaires. "
    "Elle fournit des informations complémentaires à la spectroscopie infrarouge pour l'identification moléculaire. "
    "Les techniques Raman nécessitent une préparation minimale de l'échantillon. "
    "La spectroscopie Raman amplifiée en surface amplifie les signaux pour l'analyse de traces.",

    "La chimie des polymères se concentre sur la synthèse et les propriétés des macromolécules. "
    "Les polymères comme les plastiques et les fibres sont composés d'unités monomères répétitives. "
    "La compréhension des relations structure-propriétés permet la conception de matériaux spécifiques. "
    "Les polymères biodégradables offrent des alternatives durables aux plastiques conventionnels.",

    "La nanochimie traite de la synthèse et de la caractérisation de matériaux à l'échelle du nanomètre. "
    "Les nanoparticules présentent des propriétés optiques et catalytiques uniques. "
    "Les applications incluent l'administration de médicaments et les cellules solaires. "
    "Les impacts des nanomatériaux nécessitent une évaluation attentive.",
]


def main():
    os.makedirs(TRAINING_DIR, exist_ok=True)
    rng = random.Random(SEED)

    for lang, blocks in [("en", EN_BLOCKS), ("fr", FR_BLOCKS)]:
        out_path = os.path.join(TRAINING_DIR, f"{lang}.txt")
        # Shuffle blocks
        shuffled = list(blocks)
        rng.shuffle(shuffled)

        text = "\n\n".join(shuffled) + "\n"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

        chars = len(text.encode("utf-8"))
        print(f"{lang}.txt: {len(shuffled)} blocks, {chars/1024:.1f} KB")


if __name__ == "__main__":
    main()
