package by.romanov.ppois.ControleCentre;

import by.romanov.ppois.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

@Data
public class ControlCentreContext implements Context {
    private LawRegistry lawRegistry;
    private SuspectSource suspectSource;
    @JsonIgnore
    private Input input;
    @JsonIgnore
    private State nextStage;
    private Boolean isReceivingCall;
    private TransferData transfer;
    private Case currentCase;

    public ControlCentreContext(SuspectSource suspectSource, LawRegistry lawRegistry) {
        this.suspectSource = suspectSource;
        this.input = new ConsoleInput();
        this.lawRegistry = lawRegistry;
        transfer=new TransferData();
        isReceivingCall=false;
    }

    public ControlCentreContext() {
        this.suspectSource = new SuspectSource();
        this.input = new ConsoleInput();
        this.lawRegistry = new LawRegistry();
        transfer=new TransferData();
        isReceivingCall=false;
        currentCase=new Case();
    }

    public ControlCentreContext(Input input) {
        this.suspectSource = new SuspectSource();
        this.input = input;
        this.lawRegistry = new LawRegistry();
        transfer=new TransferData();
        isReceivingCall=false;
    }

    @Override
    public void setInput(Input input) {
        this.input = input;
    }

    @Override
    public Input getInput() {
        return input;
    }
    @JsonIgnore

    public State getNextState() {
        return nextStage;
    }
}
