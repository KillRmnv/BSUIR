package by.romanov.ppois.StateMachine;




import by.romanov.ppois.TransferData;
import by.romanov.ppois.Ui.ConsoleInput;
import by.romanov.ppois.Ui.ConsoleUserInterface;

public interface Context {

    ConsoleUserInterface getUserInterface();

    default void setInput(ConsoleInput input) {
    }

    default ConsoleInput getInput() {
        return null;
    }

    State getNextState();

    default TransferData getTransfer() {
        return null;
    }


    void setUserInterface(ConsoleUserInterface userInterface);
}