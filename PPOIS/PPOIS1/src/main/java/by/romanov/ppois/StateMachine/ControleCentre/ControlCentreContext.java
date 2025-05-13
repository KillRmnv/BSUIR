package by.romanov.ppois.StateMachine.ControleCentre;

import by.romanov.ppois.Entities.*;
import by.romanov.ppois.Repository.LawRegistryJsonRepository;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Repository.SuspectSourceJsonRepository;
import by.romanov.ppois.Service.ControlCentreService;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.TransferData;
import by.romanov.ppois.Ui.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

@Data
public class ControlCentreContext implements Context {
    @JsonIgnore
    ControlCentreService controlCentreService;
    @JsonIgnore
    private ConsoleUserInterface userInterface;
    @JsonIgnore
    private State nextStage;
    private Boolean isReceivingCall;
    private TransferData transfer;
    private Case currentCase;


    public ControlCentreContext(Repository<LawRegistry, Law,Law> lawRepository, Repository<SuspectSource, Suspect, String> suspectRepository, ConsoleUserInterface userInterface) {
        controlCentreService=new ControlCentreService(lawRepository,suspectRepository);
        transfer = new TransferData();
        isReceivingCall = false;
        this.userInterface = userInterface;

    }
    public ControlCentreContext(ConsoleUserInterface userInterface) {
        controlCentreService=new ControlCentreService();
        transfer = new TransferData();
        isReceivingCall = false;
        this.userInterface = userInterface;

    }

    public ControlCentreContext() {
        controlCentreService=new ControlCentreService();
        transfer = new TransferData();
        isReceivingCall = false;
        currentCase = new Case();
        userInterface = new ConsoleUserInterface(new ConsoleInput());

    }

@JsonIgnore
    @Override
    public ConsoleUserInterface getUserInterface() {
        return userInterface;
    }

    @JsonIgnore
    @Override
    public void setInput(ConsoleInput input) {
        userInterface.setConsoleInput(input);
    }

    @JsonIgnore
    @Override
    public ConsoleInput getInput() {
        return userInterface.getConsoleInput();
    }

    @JsonIgnore

    public State getNextState() {
        return nextStage;
    }


}
