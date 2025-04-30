package by.romanov.ppois.PublicSafetyDepartment;

import by.romanov.ppois.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.HashMap;

@Data
public class PublicSafetyDepartmentContext implements Context {
    private TransferData transfer;
    @JsonIgnore
    private Input input;
    private HashMap<Integer, Law> criminalLaws;
    @JsonIgnore
    private State next;
    public PublicSafetyDepartmentContext() {
        input=new ConsoleInput();
    }
    public PublicSafetyDepartmentContext(LawRegistry laws){
        criminalLaws=laws.getCRIMINAL_LAWS();
        input=new ConsoleInput();
        transfer=new TransferData();
    }
    public PublicSafetyDepartmentContext(Input input) {
        this.input=input;
        transfer=new TransferData();
        criminalLaws=new LawRegistry().getCRIMINAL_LAWS();
    }
    @Override
    public void setInput(Input input) {
        this.input =  input;
    }

    @Override
    public Input getInput() {
        return (Input) input;
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return next;
    }
}
