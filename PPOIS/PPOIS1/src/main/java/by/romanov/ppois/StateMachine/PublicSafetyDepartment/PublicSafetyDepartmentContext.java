package by.romanov.ppois.StateMachine.PublicSafetyDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Repository.LawRegistryJsonRepository;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Service.PublicSafetyService;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Ui.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.io.IOException;

@Data
public class PublicSafetyDepartmentContext implements Context {
    private TransferData transfer;
    @JsonIgnore
    private ConsoleUserInterface userInterface;
    @JsonIgnore
    private PublicSafetyService publicSafetyService;
    @JsonIgnore
    private State next;


    public PublicSafetyDepartmentContext(){
        transfer=new TransferData();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        publicSafetyService=new PublicSafetyService();
    }
    public PublicSafetyDepartmentContext(ConsoleUserInterface userInterface) {
        transfer=new TransferData();
        this.userInterface=userInterface;

        publicSafetyService=new PublicSafetyService();
    }
    @JsonIgnore
    @Override
    public void setInput(ConsoleInput input) {
        userInterface.setConsoleInput(input);
    }
    @JsonIgnore
    @Override
    public ConsoleInput getInput() {
        return  userInterface.getConsoleInput();
    }
    @JsonIgnore
    public LawRegistry getLawRegistry() throws IOException {
       return publicSafetyService.getLawRegistry().loadAll();
    }
    @Override
    @JsonIgnore

    public State getNextState() {
        return next;
    }

}
