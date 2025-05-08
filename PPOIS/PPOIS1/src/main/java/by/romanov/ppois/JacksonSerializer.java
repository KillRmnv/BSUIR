package by.romanov.ppois;

import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.Entities.*;
import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.Police.PoliceContext;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class JacksonSerializer implements Source {
    private static final ObjectMapper objectMapper = new ObjectMapper()
            .registerModule(new JavaTimeModule());

    public  void saveContextToFile(Context context) throws IOException {
        if (context != null) {
            objectMapper.writeValue(
                    new File("./src/main/resources/" + context.getClass().getName() + ".json"),
                    context
            );
        }
    }

    public  void saveCurrentStateName(State currentState, Context context) throws IOException {
        if (currentState != null) {
            String fileName = getStateFileName(context);
            objectMapper.writeValue(new File("./src/main/resources/" + fileName), currentState.getClass().getName());
        }
    }

    public static String getStateFileName(Context context) {
        return context.getClass().getSimpleName() + "_state.json";
    }

    public  State loadStateFromFile(Context context) throws IOException {
        String fileName = getStateFileName(context);
        File file = new File("./src/main/resources/" + fileName);

        if (file.exists()) {
            try {
                String className = objectMapper.readValue(file, String.class);
                Class<?> clazz = Class.forName(className);
                return (State) clazz.getDeclaredConstructor().newInstance();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    public static <T> T loadFromFile(String filename, Class<T> valueType) throws IOException {
        return objectMapper.readValue(new File(filename), valueType);
    }

    public static PoliceContext load() throws Exception {
        SuspectSource suspectSource = generateSuspectSource();
        HashMap<Integer, PoliceMan> policeMans = generatePoliceMans();
        LawRegistry laws = new LawRegistry();

        EnforcementDepartmentContext enforcementContext = loadOrCreateEnforcementContext(policeMans);
        HRDepartmentContext hrContext = loadOrCreateHRContext(policeMans);
        InvestigationDepartmentContext investigationContext = loadOrCreateInvestigationContext(suspectSource);
        PublicSafetyDepartmentContext publicSafetyContext = loadOrCreatePublicSafetyContext(laws);
        ControlCentreContext controlCentreContext = loadOrCreateControlCentreContext(suspectSource, laws);

        return new PoliceContext(controlCentreContext, investigationContext,
                enforcementContext, hrContext, publicSafetyContext);
    }

    private static SuspectSource generateSuspectSource() {
        SuspectSource suspectSource = new SuspectSource();
        for (int i = 0; i < 30; i++) {
            Traits randomTraits = new Traits(false);
            Suspect randomSuspect = new Suspect();
            randomSuspect.setTraits(randomTraits);
            suspectSource.addSuspect(randomSuspect);
        }
        return suspectSource;
    }

    private static HashMap<Integer, PoliceMan> generatePoliceMans() {
        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        for (int i = 0; i < 5; i++) {
            PoliceMan newPoliceMan = new PoliceMan(i);
            policeMans.put(i, newPoliceMan);
        }
        return policeMans;
    }

    private static EnforcementDepartmentContext loadOrCreateEnforcementContext(Map<Integer, PoliceMan> policeMans) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, EnforcementDepartmentContext.class);
        } else {
            EnforcementDepartmentContext context = new EnforcementDepartmentContext((HashMap<Integer, PoliceMan>) policeMans);
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    private static HRDepartmentContext loadOrCreateHRContext(Map<Integer, PoliceMan> policeMans) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.HRDepartment.HRDepartmentContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, HRDepartmentContext.class);
        } else {
            HRDepartmentContext context = new HRDepartmentContext((HashMap<Integer, PoliceMan>) policeMans);
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    private static InvestigationDepartmentContext loadOrCreateInvestigationContext(SuspectSource source) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, InvestigationDepartmentContext.class);
        } else {
            InvestigationDepartmentContext context = new InvestigationDepartmentContext(source);
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    private static PublicSafetyDepartmentContext loadOrCreatePublicSafetyContext(LawRegistry laws) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, PublicSafetyDepartmentContext.class);
        } else {
            PublicSafetyDepartmentContext context = new PublicSafetyDepartmentContext(laws);
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    private static ControlCentreContext loadOrCreateControlCentreContext(SuspectSource source, LawRegistry laws) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.ControleCentre.ControlCentreContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, ControlCentreContext.class);
        } else {
            ControlCentreContext context = new ControlCentreContext(source, laws);
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    public  void deleteContext(Context context) {
        File file = new File("./src/main/resources/" + getStateFileName(context));
        if (file.exists())
            file.delete();
    }
    public  State loadState(State currentState, Context context, State state) throws IOException {
        currentState = loadStateFromFile(context);
        if (currentState == null) {
            currentState = state;
        } else {
            deleteContext(context);

        }
        return currentState;
    }
}