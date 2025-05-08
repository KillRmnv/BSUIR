package by.romanov.ppois;


public interface Context {
    Source getSource();
    void setSource(Source source);
    void setUserInterface(UserInterface userInterface);
    UserInterface getUserInterface();
    default void setInput(Input input) {
    }
    default Input getInput() {
        return null;
    }
    State getNextState();
    default TransferData getTransfer(){
        return null;
    }
}
