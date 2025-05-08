package by.romanov.ppois.HRDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.HashMap;

@Data
public class HRDepartmentContext implements Context {
    private HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
    @JsonIgnore
    private UserInterface userInterface;
    private int budget;
    private TransferData transfer;
    @JsonIgnore
    private Source source;
    public HRDepartmentContext() {
        budget=10000;
        transfer=new TransferData();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }
    public HRDepartmentContext(Input input) {
        budget=10000;
        transfer=new TransferData();
        userInterface=new ConsoleUserInterface(input);
        source=new JacksonSerializer();
    }

    public HRDepartmentContext(HashMap<Integer, PoliceMan> policeMans) {
        this.policeMans = policeMans;
        budget=10000;
        transfer=new TransferData();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }
    @JsonIgnore
    @Override
    public void setInput(Input input) {
        userInterface.setInput(input);
    }
    public void delPoliceMan(int index){
        if(policeMans.containsKey(index)) {
            int salary = policeMans.get(index).getSalary();
            policeMans.remove(index);
            budget += salary;
        }
    }
    public void addPoliceMan(PoliceMan policeMan) throws Exception{
        if(budget<policeMan.getSalary()){
            throw new Exception("Недостаточно средств");
        }
        policeMans.put(policeMans.size(), policeMan);
        budget-=policeMan.getSalary();
    }
    @JsonIgnore
    @Override
    public Input getInput() {
        return userInterface.getInput();
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return new InitialState();
    }
}
