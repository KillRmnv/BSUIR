package by.romanov.ppois;


public interface Context {

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
