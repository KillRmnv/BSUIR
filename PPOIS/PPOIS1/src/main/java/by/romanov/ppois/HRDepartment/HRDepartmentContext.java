package by.romanov.ppois.HRDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.HashMap;

@Data
public class HRDepartmentContext implements Context {
    private HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
    @JsonIgnore
    private Input input;
    private int budget;
    private TransferData transfer;
    public HRDepartmentContext() {
        budget=10000;
        input=new ConsoleInput();
        transfer=new TransferData();
    }
    public HRDepartmentContext(Input input) {
        this.input=input;
        budget=10000;
        transfer=new TransferData();
    }

    public HRDepartmentContext(HashMap<Integer, PoliceMan> policeMans) {
        this.policeMans = policeMans;
        budget=10000;
        input=new ConsoleInput();
        transfer=new TransferData();
    }

    @Override
    public void setInput(Input input) {
       this.input= input;
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

    @Override
    public Input getInput() {
        return (Input)input;
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return new InitialState();
    }
}
