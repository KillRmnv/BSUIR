package com.example;

import java.io.*;
import java.util.Iterator;
import java.util.List;  
import java.util.Scanner;
import org.apache.jena.ontology.*;
import org.apache.jena.query.*;
import org.apache.jena.rdf.model.*;
import org.apache.jena.util.FileManager;
import org.apache.jena.vocabulary.OWL;
import org.apache.jena.vocabulary.RDF;  

public class OntologyQuery {

    public static final String MY_NS =
        "http://www.technical-sciences.org/ontology#";
    
    private OntModel model;
    private Scanner scanner;
    private static final int MAX_STATS_ITERATIONS = 10000;
    private static final long STATS_TIMEOUT_MS = 5000;

    public static void main(String[] args) {
        OntologyQuery app = new OntologyQuery();
        app.run();
    }

    public void run() {
        scanner = new Scanner(System.in);

        System.out.println("=== Jena Ontology Query Tool ===");
        System.out.println();

        initializeModel();
        loadOntologies();

        boolean running = true;
        while (running) {
            printMenu();
            int choice = readChoice();

            switch (choice) {
                case 1:
                    queryIndustrySector();
                    break;
                case 2:
                    queryResearchObject();
                    break;
                case 3:
                    queryTechnicalDiscipline();
                    break;
                case 4:
                    queryCustom();
                    break;
                case 5:
                    showModelStatsSafe();
                    break;
                case 0:
                    running = false;
                    System.out.println("Выход...");
                    break;
                default:
                    System.out.println("Неверный выбор!");
            }

            if (running) {
                System.out.println("\nНажмите Enter для продолжения...");
                scanner.nextLine();
            }
        }

        scanner.close();
    }

    private void initializeModel() {
        System.out.println("Выбор reasoner'а:");
        System.out.println("1. OWL_MEM (без reasoner'а)");
        System.out.println("2. OWL_MEM_RDFS_INF (RDFS инференс)");
        System.out.println("3. OWL_MEM_RULE_INF (OWL правила) - рекомендуется");
        System.out.println("4. OWL_MEM_MICRO_RULE_INF (легкий OWL)");
        System.out.println("5. OWL_MEM_MINI_RULE_INF (средний OWL)");

        int reasonerChoice = readChoice();
        OntModelSpec spec;

        switch (reasonerChoice) {
            case 1:
                spec = OntModelSpec.OWL_MEM;
                System.out.println("Выбрано: без reasoner'а");
                break;
            case 2:
                spec = OntModelSpec.OWL_MEM_RDFS_INF;
                System.out.println("Выбрано: RDFS инференс");
                break;
            case 4:
                spec = OntModelSpec.OWL_MEM_MICRO_RULE_INF;
                System.out.println("Выбрано: OWL Micro");
                break;
            case 5:
                spec = OntModelSpec.OWL_MEM_MINI_RULE_INF;
                System.out.println("Выбрано: OWL Mini");
                break;
            case 3:
            default:
                spec = OntModelSpec.OWL_MEM_RULE_INF;
                System.out.println("Выбрано: OWL Rule Inf");
                break;
        }

        System.out.println("Создание модели...");
        model = ModelFactory.createOntologyModel(spec);
        System.out.println("Модель создана.\n");
    }

    /**
     * Загрузка онтологий с автоматическим разрешением импортов
     */
     /**
      * Загрузка онтологий с автоматической подгрузкой локальных импортов
      */
     private void loadOntologies() {
         System.out.println("=== Загрузка онтологий ===");
 
         // Включаем динамическую загрузку импортов
         model.setDynamicImports(true);
         System.out.println("Автозагрузка импортов: включена");
 
         // Твоя основная онтология
         System.out.print("Введите путь к основной онтологии (или Enter для default): ");
         String mainPath = scanner.nextLine().trim();
 
         if (mainPath.isEmpty()) {
             mainPath = "src/main/resources/ALL.rdf";
         }
 
         try {
             System.out.println("Загрузка: " + mainPath);
             FileManager.get().readModel(model, mainPath);
             System.out.println("✓ Основная онтология загружена");
             
             
             // Загружаем импорты отдельно от основной загрузки
             loadImportsSafely();
             
         } catch (Exception e) {
             System.err.println("✗ Ошибка загрузки основной онтологии: " + e.getMessage());
             e.printStackTrace();
         }
 
         // Автоматическая подгрузка локальных внешних онтологий
         loadLocalExternalOntologies();
 
         // Ручное добавление внешних онтологий
         boolean loadingExternal = true;
         while (loadingExternal) {
             System.out.print("\nДобавить внешнюю онтологию вручную? (y/n): ");
             String answer = scanner.nextLine().trim().toLowerCase();
 
             if (answer.equals("y")) {
                 System.out.print("Путь к файлу или URL: ");
                 String extPath = scanner.nextLine().trim();
 
                 try {
                     System.out.println("Загрузка: " + extPath);
                     model.read(extPath);
                     System.out.println("✓ Внешняя онтология загружена");
                 } catch (Exception e) {
                     System.err.println("✗ Ошибка: " + e.getMessage());
                 }
             } else {
                 loadingExternal = false;
             }
         }
 
         System.out.println("\nЗагрузка завершена.");
         showModelStatsSafe();
         showNamespaces();
     }
 
     /**
      * Безопасная загрузка импортов (не прерывает выполнение при ошибке)
      */
     private void loadImportsSafely() {
         System.out.println("Загрузка импортированных онтологий...");
         
         try {
             StmtIterator imports = model.listStatements(null, OWL.imports, (RDFNode) null);
             int count = 0;
             int failed = 0;
             
             while (imports.hasNext()) {
                 Statement stmt = imports.nextStatement();
                 if (stmt.getObject().isResource()) {
                     String importUri = stmt.getResource().getURI();
                     System.out.println("  Найден импорт: " + importUri);
                     
                     try {
                         model.read(importUri);
                         System.out.println("  ✓ Загружен: " + importUri);
                         count++;
                     } catch (Exception e) {
                         System.out.println("  ✗ Не удалось загрузить: " + importUri);
                         System.out.println("    (будет использована локальная версия если есть)");
                         failed++;
                     }
                 }
             }
             
             System.out.println("Загружено импортов: " + count + ", не удалось: " + failed);
             
         } catch (Exception e) {
             System.out.println("  (ошибка при поиске импортов: " + e.getMessage() + ")");
         }
     }
 
     /**
      * Автоматическая загрузка локальных внешних онтологий
      */
     private void loadLocalExternalOntologies() {
         System.out.println("\nАвтоматическая подгрузка локальных онтологий...");
         
         // Список локальных файлов для загрузки
         String[] localFiles = {
             "src/main/resources/ModSci.ttl",
             "src/main/resources/EDAM.owl",
             "src/main/resources/ontologiev3.owl"
         };
         
         int loaded = 0;
         for (String file : localFiles) {
             File f = new File(file);
             if (f.exists()) {
                 try {
                     System.out.print("  Загрузка " + file + " ... ");
                     
                     // Определяем формат по расширению
                     String lang = file.endsWith(".ttl") ? "TURTLE" : "RDF/XML";
                     model.read(file, lang);
                     
                     System.out.println("✓");
                     loaded++;
                 } catch (Exception e) {
                     System.out.println("✗ (" + e.getMessage() + ")");
                 }
             } else {
                 System.out.println("  Пропуск " + file + " (файл не найден)");
             }
         }
         
         System.out.println("Загружено локальных онтологий: " + loaded);
     }
 
     /**
      * Показать все namespace в модели
      */
     private void showNamespaces() {
         System.out.println("\n=== Namespace в модели ===");
         java.util.Map<String, String> nsMap = model.getNsPrefixMap();
         for (java.util.Map.Entry<String, String> entry : nsMap.entrySet()) {
             System.out.println("  " + entry.getKey() + " : " + entry.getValue());
         }
         System.out.println();
     }

    /**
     * Принудительная загрузка всех owl:imports
     */
    private void loadImports() {
        System.out.println("Загрузка импортированных онтологий...");
        
        // Находим все owl:imports
        StmtIterator imports = model.listStatements(null, OWL.imports, (RDFNode) null);
        int count = 0;
        
        while (imports.hasNext()) {
            Statement stmt = imports.nextStatement();
            if (stmt.getObject().isResource()) {
                String importUri = stmt.getResource().getURI();
                System.out.println("  Найден импорт: " + importUri);
                
                try {
                    // Пробуем загрузить
                    model.read(importUri);
                    System.out.println("  ✓ Загружен: " + importUri);
                    count++;
                } catch (Exception e) {
                    System.err.println("  ✗ Не удалось загрузить: " + importUri);
                    System.err.println("    Причина: " + e.getMessage());
                }
            }
        }
        
        if (count == 0) {
            System.out.println("  (импорты не найдены или уже загружены)");
        } else {
            System.out.println("Загружено импортов: " + count);
        }
    }

    private void showModelStatsSafe() {
        System.out.println("\n=== Статистика модели ===");
        System.out.println("Триплетов: " + model.size());

        long startTime = System.currentTimeMillis();
        
        int classCount = countWithSparql("SELECT (COUNT(DISTINCT ?c) AS ?count) WHERE { ?c a <http://www.w3.org/2002/07/owl#Class> }");
        if (classCount == -1) {
            classCount = countWithLimit(model.listClasses());
        }
        System.out.println("Классов: " + classCount);

        int individualCount = countWithSparql("SELECT (COUNT(DISTINCT ?i) AS ?count) WHERE { ?i a <http://www.w3.org/2002/07/owl#NamedIndividual> }");
        if (individualCount == -1) {
            individualCount = countWithLimit(model.listIndividuals());
        }
        System.out.println("Индивидуалов: " + individualCount);

        int propertyCount = countWithSparql("SELECT (COUNT(DISTINCT ?p) AS ?count) WHERE { ?p a <http://www.w3.org/2002/07/owl#ObjectProperty> }");
        if (propertyCount == -1) {
            propertyCount = countWithLimit(model.listAllOntProperties());
        }
        System.out.println("Свойств: " + propertyCount);

        long duration = System.currentTimeMillis() - startTime;
        System.out.println("Время подсчета: " + duration + " мс");
        
        if (duration > STATS_TIMEOUT_MS) {
            System.out.println("⚠️  Предупреждение: подсчет занял много времени.");
            System.out.println("   Рекомендация: используйте reasoner попроще (OWL_MEM_MICRO_RULE_INF)");
        }
        System.out.println();
    }

    private int countWithSparql(String queryString) {
        try {
            Query query = QueryFactory.create(queryString);
            try (QueryExecution qexec = QueryExecutionFactory.create(query, model)) {
                ResultSet results = qexec.execSelect();
                if (results.hasNext()) {
                    QuerySolution soln = results.nextSolution();
                    Literal count = soln.getLiteral("count");
                    return count.getInt();
                }
            }
        } catch (Exception e) {
            return -1;
        }
        return 0;
    }

    private <T> int countWithLimit(Iterator<T> iterator) {
        int count = 0;
        long startTime = System.currentTimeMillis();
        
        while (iterator.hasNext()) {
            iterator.next();
            count++;
            
            if (count >= MAX_STATS_ITERATIONS) {
                System.out.println("  (прервано после " + MAX_STATS_ITERATIONS + " элементов)");
                break;
            }
            
            if (count % 1000 == 0) {
                if (System.currentTimeMillis() - startTime > STATS_TIMEOUT_MS) {
                    System.out.println("  (таймаут: подсчет прерван)");
                    break;
                }
            }
        }
        return count;
    }

    private void printMenu() {
        System.out.println("\n=== МЕНЮ ЗАПРОСОВ ===");
        System.out.println("1. IndustrySector (с эквивалентными классами)");
        System.out.println("2. ResearchObject (с подклассами и эквивалентами)");
        System.out.println("3. TechnicalDiscipline (все подклассы + внешние)");
        System.out.println("4. Произвольный SPARQL запрос");
        System.out.println("5. Статистика модели");
        System.out.println("0. Выход");
        System.out.print("\nВыбор: ");
    }

    private int readChoice() {
        try {
            String input = scanner.nextLine().trim();
            return Integer.parseInt(input);
        } catch (NumberFormatException e) {
            return -1;
        }
    }

    private void queryIndustrySector() {
        System.out.println("\n=== Запрос: IndustrySector ===");

        String queryString = """
            PREFIX my: <http://www.technical-sciences.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT DISTINCT ?industry ?label ?sourceClass
            WHERE {
              {
                ?industry a my:IndustrySector .
                BIND(my:IndustrySector AS ?sourceClass)
              }
              UNION
              {
                ?eqClass owl:equivalentClass my:IndustrySector .
                ?industry a ?eqClass .
                BIND(?eqClass AS ?sourceClass)
              }
              UNION
              {
                my:IndustrySector owl:equivalentClass ?eqClass .
                ?industry a ?eqClass .
                BIND(?eqClass AS ?sourceClass)
              }
              OPTIONAL { ?industry rdfs:label ?label }
            }
            ORDER BY ?sourceClass ?industry
            """;

        executeQuery(queryString, "IndustrySector");
    }

    private void queryResearchObject() {
        System.out.println("\n=== Запрос: ResearchObject ===");

        String queryString = """
            PREFIX my: <http://www.technical-sciences.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT DISTINCT ?object ?label ?sourceClass
            WHERE {
              {
                ?object a my:ResearchObject .
                BIND(my:ResearchObject AS ?sourceClass)
              }
              UNION
              {
                ?subClass rdfs:subClassOf* my:ResearchObject .
                ?object a ?subClass .
                BIND(?subClass AS ?sourceClass)
              }
              UNION
              {
                ?eqClass owl:equivalentClass my:ResearchObject .
                ?object a ?eqClass .
                BIND(?eqClass AS ?sourceClass)
              }
              UNION
              {
                my:ResearchObject owl:equivalentClass ?eqClass .
                ?object a ?eqClass .
                BIND(?eqClass AS ?sourceClass)
              }
              OPTIONAL { ?object rdfs:label ?label }
            }
            ORDER BY ?sourceClass ?object
            """;

        executeQuery(queryString, "ResearchObject");
    }

    private void queryTechnicalDiscipline() {
        System.out.println("\n=== Запрос: TechnicalDiscipline ===");
        
        String queryString = """
            PREFIX my: <http://www.technical-sciences.org/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT DISTINCT ?discipline ?label ?sourceClass
            WHERE {
              {
                ?discipline a my:TechnicalDiscipline .
                BIND(my:TechnicalDiscipline AS ?sourceClass)
              }
              UNION
              {
                ?subClass rdfs:subClassOf* my:TechnicalDiscipline .
                ?discipline a ?subClass .
                BIND(?subClass AS ?sourceClass)
              }
              UNION
              {
                ?eqClass owl:equivalentClass my:TechnicalDiscipline .
                ?discipline a ?eqClass .
                BIND(?eqClass AS ?sourceClass)
              }
              UNION
              {
                my:TechnicalDiscipline owl:equivalentClass ?eqClass .
                ?discipline a ?eqClass .
                BIND(?eqClass AS ?sourceClass)
              }
              OPTIONAL { ?discipline rdfs:label ?label }
            }
            ORDER BY ?sourceClass ?discipline
            """;

        executeQuery(queryString, "TechnicalDiscipline");
    }
    private void queryCustom() {
        System.out.println("\n=== Произвольный SPARQL запрос ===");
        System.out.println("Доступные префиксы:");
        System.out.println("  my: <" + MY_NS + ">");
        System.out.println("  rdfs: <http://www.w3.org/2000/01/rdf-schema#>");
        System.out.println("  owl: <http://www.w3.org/2002/07/owl#>");
        System.out.println("  rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>");
        System.out.println("\nВведите запрос (SELECT ...), пустая строка для завершения:");

        StringBuilder queryBuilder = new StringBuilder();
        String line;
        while (!(line = scanner.nextLine()).isEmpty()) {
            queryBuilder.append(line).append(" ");
        }

        String queryString = queryBuilder.toString().trim();
        if (!queryString.isEmpty()) {
            if (!queryString.contains("PREFIX")) {
                queryString =
                    "PREFIX my: <" + MY_NS + "> " +
                    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> " +
                    "PREFIX owl: <http://www.w3.org/2002/07/owl#> " +
                    queryString;
            }
            executeQuery(queryString, "Custom");
        }
    }

    /**
     * Универсальный метод выполнения запроса
     */
     private void executeQuery(String queryString, String queryName) {
         long startTime = System.currentTimeMillis();
 
         try {
             Query query = QueryFactory.create(queryString);
 
             try (QueryExecution qexec = QueryExecutionFactory.create(query, model)) {
                 
                 try {
                     qexec.setTimeout(30000);
                 } catch (UnsupportedOperationException e) {
                     // ignore
                 }
 
                 ResultSet results = qexec.execSelect();
 
                 List<String> varNames = results.getResultVars();
                 
                 int count = 0;
                 String prevSource = "";
                 final int MAX_RESULTS = 1000;
 
                 System.out.println("\n--- Результаты ---");
 
                 while (results.hasNext()) {
                     QuerySolution soln = results.nextSolution();
                     count++;
                     
                     if (count > MAX_RESULTS) {
                         System.out.println("\n... (показано первые " + MAX_RESULTS + " результатов)");
                         break;
                     }
 
                     // Находим основную переменную (не sourceClass и не label)
                     Resource mainResource = null;
                     for (String var : varNames) {
                         if (var.equals("sourceClass") || var.equals("label")) continue;
                         
                         RDFNode node = soln.get(var);
                         if (node != null && node.isResource()) {
                             mainResource = node.asResource();
                             break;
                         }
                     }
                     
                     Literal label = soln.getLiteral("label");
                     Resource sourceClass = varNames.contains("sourceClass") ? soln.getResource("sourceClass") : null;
 
                     String sourceUri = "unknown";
                     String shortSource = "unknown";
                     
                     if (sourceClass != null) {
                         sourceUri = sourceClass.getURI();
                         shortSource = shortenUri(sourceUri);
                     } else if (mainResource != null) {
                         Statement typeStmt = mainResource.getProperty(RDF.type);
                         if (typeStmt != null && typeStmt.getObject().isResource()) {
                             sourceUri = typeStmt.getResource().getURI();
                             shortSource = shortenUri(sourceUri);
                         }
                     }
 
                     if (!sourceUri.equals(prevSource)) {
                         System.out.println("\n[" + shortSource + "]");
                         prevSource = sourceUri;
                     }
 
                     String resUri = mainResource != null ? shortenUri(mainResource.getURI()) : "null";
                     
                     // Улучшенная обработка label
                     String labelStr;
                     if (label != null) {
                         labelStr = label.getString();
                     } else if (mainResource != null) {
                         // Fallback на локальное имя ресурса
                         String localName = mainResource.getLocalName();
                         labelStr = (localName != null && !localName.isEmpty()) ? localName : "N/A";
                     } else {
                         labelStr = "N/A";
                     }
 
                     System.out.printf("  %d. %s | %s%n", count, resUri, labelStr);
                 }
 
                 long endTime = System.currentTimeMillis();
 
                 System.out.println("\n--- Итого ---");
                 System.out.println("Найдено: " + count + " результатов");
                 System.out.println("Время выполнения: " + (endTime - startTime) + " мс");
 
                 if (count == 0) {
                     System.out.println("Совет: проверьте namespace в онтологии и запросе");
                     System.out.println("Ожидаемый NS: " + MY_NS);
                 }
             }
         } catch (QueryParseException e) {
             System.err.println("Ошибка синтаксиса SPARQL: " + e.getMessage());
         } catch (QueryCancelledException e) {
             System.err.println("⚠️ Запрос отменен по таймауту (30 сек)");
         } catch (Exception e) {
             System.err.println("Ошибка выполнения: " + e.getMessage());
             e.printStackTrace();
         }
     }

    private String shortenUri(String uri) {
        if (uri == null) return "null";
        return uri
            .replace(MY_NS, "my:")
            .replace("http://www.w3.org/2002/07/owl#", "owl:")
            .replace("http://www.w3.org/2000/01/rdf-schema#", "rdfs:")
            .replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdf:")
            .replace("http://dbpedia.org/ontology/", "dbo:")
            .replace("http://www.wikidata.org/entity/", "wd:");
    }
}