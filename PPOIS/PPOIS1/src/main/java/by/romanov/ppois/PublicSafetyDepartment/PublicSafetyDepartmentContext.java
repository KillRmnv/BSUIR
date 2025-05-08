package by.romanov.ppois.PublicSafetyDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.HashMap;

@Data
public class PublicSafetyDepartmentContext implements Context {
    private TransferData transfer;
    private String page;
    @JsonIgnore
    private Source source;
    @JsonIgnore
    private UserInterface userInterface;
    private HashMap<Integer, Law> criminalLaws;
    @JsonIgnore
    private State next;
    public PublicSafetyDepartmentContext() {
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }
    public PublicSafetyDepartmentContext(LawRegistry laws){
        criminalLaws=laws.getCRIMINAL_LAWS();
        transfer=new TransferData();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        page="";
        source=new JacksonSerializer();
    }
    public PublicSafetyDepartmentContext(Input input) {
        transfer=new TransferData();
        criminalLaws=new LawRegistry().getCRIMINAL_LAWS();
        userInterface=new ConsoleUserInterface(input);
        page="";
        source=new JacksonSerializer();
    }
    @JsonIgnore
    @Override
    public void setInput(Input input) {
        userInterface.setInput(input);
    }
    @JsonIgnore
    @Override
    public Input getInput() {
        return  userInterface.getInput();
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return next;
    }
}
