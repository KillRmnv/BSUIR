package by.romanov.ppois.StateMachine;

public interface State {
    void run(Context context) throws Exception;

    State next(Context context) throws Exception;

}