package by.romanov.ppois;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Data;

import java.io.File;
import java.io.IOException;

@Data
public class StateMachine {
    @JsonIgnore
    protected State currentState;

    protected Context context;
    protected String currentStateClassName;

    private static final ObjectMapper objectMapper = new ObjectMapper();

    public StateMachine() {
    }

    public StateMachine(Context context) {
        this.context = context;
    }

    public final void runAll(State state) throws Exception {
        currentState = loadStateFromFile();
        boolean loaded=false;
        if (currentState == null) {
            currentState = state;
        } else {
            File file = new File("./src/main/resources/"+getStateFileName());
            file.delete();
            loaded = true;
        }
        currentStateClassName = state.getClass().getName();
        State next=null;
        while (currentState != null) {
            currentState.run(context);
            currentState = currentState.next(context);

            if (currentState != null) {
                currentStateClassName = currentState.getClass().getName();
            }

            saveContextToFile();
            saveCurrentStateName();
        }
        File file = new File("./src/main/resources/"+getStateFileName());
        if (file.exists())
            file.delete();

    }

    public void saveContextToFile() throws IOException {
        if (context != null) {
            objectMapper.writeValue(
                    new File("./src/main/resources/"+context.getClass().getName() + ".json"),
                    context
            );
        }

    }
    public static void saveContextToFile(Context context) throws IOException {
        if (context != null) {
            objectMapper.writeValue(
                    new File("./src/main/resources/"+context.getClass().getName() + ".json"),
                    context
            );
        }
    }
    public void saveCurrentStateName() throws IOException {
        if (currentState != null) {
            String fileName = getStateFileName();
            objectMapper.writeValue(new File("./src/main/resources/"+fileName), currentState.getClass().getName());
        }
    }

    public String getStateFileName() {
        return context.getClass().getSimpleName() + "_state.json";
    }

    public State loadStateFromFile() {
        String fileName = getStateFileName();
        File file = new File("./src/main/resources/"+fileName);

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

}
