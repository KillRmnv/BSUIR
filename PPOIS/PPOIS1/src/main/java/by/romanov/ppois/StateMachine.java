package by.romanov.ppois;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;


@Data
public class StateMachine {
    @JsonIgnore
    protected State currentState;
    protected Context context;

    public StateMachine() {
    }

    public StateMachine(Context context) {
        this.context = context;
    }

    public final void runAll(State state) throws Exception {
        currentState = context.getSource().loadState(currentState, context, state);
        while (currentState != null) {
            context.getSource().saveCurrentStateName(currentState, context);
            context.getUserInterface().showPage(context.getUserInterface().getPage());
            currentState.run(context);
            currentState = currentState.next(context);
            context.getSource().saveContextToFile(context);
        }
        context.getSource().deleteContext(context);
    }
}