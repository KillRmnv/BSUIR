package by.romanov.ppois.Repository;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.StateMachine.Police.PoliceContext;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Ui.ConsoleUserInterface;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import java.io.File;
import java.io.IOException;

public class JacksonSerializer implements Source {
    private static final ObjectMapper objectMapper = new ObjectMapper()
            .registerModule(new JavaTimeModule());

    public void saveToFile(Object object) throws IOException {
        if (object != null) {
            objectMapper.writeValue(
                    new File("./src/main/resources/" + object.getClass().getName() + ".json"),
                    object
            );
        }
    }

    @Override
    public void saveCurrentStateName(State currentState, Context context) throws IOException {
        if (currentState != null) {
            String fileName = getStateFileName(context);
            objectMapper.writeValue(new File("./src/main/resources/" + fileName), currentState.getClass().getName());
        }
    }

    public static String getStateFileName(Object context) {
        return context.getClass().getSimpleName() + "_state.json";
    }

    public State loadStateFromFile(Context context) throws IOException {
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

    @Override
    public Object load( ConsoleUserInterface userInterface) throws Exception {

        EnforcementDepartmentContext enforcementContext = loadOrCreateEnforcementContext(userInterface );
        HRDepartmentContext hrContext = loadOrCreateHRContext(userInterface );
        InvestigationDepartmentContext investigationContext = loadOrCreateInvestigationContext(userInterface );
        PublicSafetyDepartmentContext publicSafetyContext = loadOrCreatePublicSafetyContext(userInterface );
        ControlCentreContext controlCentreContext = loadOrCreateControlCentreContext(userInterface );

        PoliceContext policeContext = new PoliceContext(controlCentreContext, investigationContext,
                enforcementContext, hrContext, publicSafetyContext,userInterface);
        
        return policeContext;
    }


    private static EnforcementDepartmentContext loadOrCreateEnforcementContext(ConsoleUserInterface userInterface    ) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.Service.EnforcementDepartment.EnforcementDepartmentContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, EnforcementDepartmentContext.class);
        } else {
            EnforcementDepartmentContext context = new EnforcementDepartmentContext(userInterface );
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    private static HRDepartmentContext loadOrCreateHRContext(ConsoleUserInterface userInterface    ) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.Service.HRDepartment.HRDepartmentContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, HRDepartmentContext.class);
        } else {
            HRDepartmentContext context = new HRDepartmentContext(userInterface );
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    private static InvestigationDepartmentContext loadOrCreateInvestigationContext(ConsoleUserInterface userInterface    ) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.Service.InvestigationDepartment.InvestigationDepartmentContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, InvestigationDepartmentContext.class);
        } else {
            InvestigationDepartmentContext context = new InvestigationDepartmentContext(userInterface );
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    private static PublicSafetyDepartmentContext loadOrCreatePublicSafetyContext(ConsoleUserInterface userInterface    ) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.Service.PublicSafetyDepartment.PublicSafetyDepartmentContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, PublicSafetyDepartmentContext.class);
        } else {
            PublicSafetyDepartmentContext context = new PublicSafetyDepartmentContext(userInterface );
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    private static ControlCentreContext loadOrCreateControlCentreContext(ConsoleUserInterface userInterface    ) throws IOException {
        String path = "./src/main/resources/by.romanov.ppois.Service.ControleCentre.ControlCentreContext.json";
        File file = new File(path);
        if (file.exists()) {
            return loadFromFile(path, ControlCentreContext.class);
        } else {
            ControlCentreContext context = new ControlCentreContext( userInterface);
            objectMapper.writeValue(file, context);
            return context;
        }
    }

    @Override
    public void deleteState(Object object) {
        File file = new File("./src/main/resources/" + getStateFileName(object));
        if (file.exists())
            file.delete();
    }

    public State loadState(State currentState, Context context, State state) throws IOException {
        currentState = loadStateFromFile(context);
        if (currentState == null) {
            currentState = state;
        } else {
            deleteState(context);

        }
        return currentState;
    }
}