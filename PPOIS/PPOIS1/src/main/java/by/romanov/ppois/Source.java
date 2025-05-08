package by.romanov.ppois;

import java.io.IOException;

public interface Source {
     State loadState(State currentState, Context context, State state) throws IOException;
     void saveCurrentStateName(State currentState, Context context)throws IOException;
     void saveContextToFile(Context context) throws IOException;
     void deleteContext(Context context);
}
