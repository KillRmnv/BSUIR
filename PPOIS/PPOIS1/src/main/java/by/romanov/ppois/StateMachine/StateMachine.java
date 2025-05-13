package by.romanov.ppois.StateMachine;

import by.romanov.ppois.Repository.Source;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.io.IOException;
import java.util.concurrent.CompletableFuture;


@Data
public class StateMachine {
    @JsonIgnore
    protected State currentState;
    protected Context context;
    @JsonIgnore
    protected Source source;

    public StateMachine() {
    }

    public StateMachine(Context context,Source source) {
        this.context = context;
        this.source = source;
    }

    public final void runAll(State state) throws Exception {
        currentState = source.loadState(currentState, context, state);
        while (currentState != null) {
            CompletableFuture.runAsync(() -> {
                try {
                    source.saveCurrentStateName(currentState, context);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
            currentState.run(context);
            currentState = currentState.next(context);
            CompletableFuture.runAsync(() -> {
                try {
                    source.saveToFile(context);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
        }
        CompletableFuture.runAsync(() -> {
            source.deleteState(context);
        });
    }
}