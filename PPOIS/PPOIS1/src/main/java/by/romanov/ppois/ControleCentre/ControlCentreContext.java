package by.romanov.ppois.ControleCentre;

import by.romanov.ppois.*;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.LawRegistry;
import by.romanov.ppois.Entities.SuspectSource;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

@Data
public class ControlCentreContext implements Context {
    private LawRegistry lawRegistry;
    private SuspectSource suspectSource;
    @JsonIgnore
    private UserInterface userInterface;
    @JsonIgnore
    private State nextStage;
    private Boolean isReceivingCall;
    private TransferData transfer;
    private Case currentCase;
    @JsonIgnore
    private Source source;

    public ControlCentreContext(SuspectSource suspectSource, LawRegistry lawRegistry) {
        this.suspectSource = suspectSource;
        this.lawRegistry = lawRegistry;
        transfer=new TransferData();
        isReceivingCall=false;
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }

    public ControlCentreContext() {
        this.suspectSource = new SuspectSource();
        this.lawRegistry = new LawRegistry();
        transfer=new TransferData();
        isReceivingCall=false;
        currentCase=new Case();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }

    public ControlCentreContext(Input input) {
        this.suspectSource = new SuspectSource();
        this.lawRegistry = new LawRegistry();
        transfer=new TransferData();
        isReceivingCall=false;
        userInterface=new ConsoleUserInterface(input);
        source=new JacksonSerializer();
    }

    @Override
    public void setUserInterface(UserInterface userInterface) {
        this.userInterface = userInterface;
    }

    @Override
    public UserInterface getUserInterface() {
        return userInterface;
    }
    @JsonIgnore
    @Override
    public void setInput(Input input) {
        userInterface.setInput(input);
    }
    @JsonIgnore
    @Override
    public Input getInput() {
        return userInterface.getInput();
    }
    @JsonIgnore

    public State getNextState() {
        return nextStage;
    }
}
