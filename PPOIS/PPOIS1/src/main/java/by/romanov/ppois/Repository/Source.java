package by.romanov.ppois.Repository;

import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Ui.ConsoleUserInterface;



import java.io.IOException;

public interface Source {
    State loadState(State currentState, Context context, State state) throws IOException;

    void saveCurrentStateName(State currentState, Context context) throws IOException;

    void saveToFile(Object object) throws IOException;

    void deleteState(Object object);

    Object load( ConsoleUserInterface userInterface) throws Exception;

}
