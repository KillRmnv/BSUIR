package by.romanov.ppois.StateMachine.HRDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Repository.PoliceMansJsonRepository;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Service.HRService;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Ui.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.io.IOException;
import java.util.HashMap;

@Data
public class HRDepartmentContext implements Context {
    @JsonIgnore
    private ConsoleUserInterface userInterface;
    @JsonIgnore
    private HRService hrService;
    private int budget;
    private TransferData transfer;

    public HRDepartmentContext() {
        budget=10000;
        transfer=new TransferData();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        hrService=new HRService();
    }
    public HRDepartmentContext(ConsoleUserInterface userInterface) {
        budget=10000;
        transfer=new TransferData();
        this.userInterface=userInterface;
        hrService=new HRService();

    }

    public HRDepartmentContext(Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> repository,ConsoleUserInterface userInterface) {
        budget=10000;
        transfer=new TransferData();
        this.userInterface=userInterface;
        hrService=new HRService(repository);
    }
    @JsonIgnore
    @Override
    public void setInput(ConsoleInput input) {
        userInterface.setConsoleInput(input);
    }
    public void delPoliceMan(int index) throws IOException {

       PoliceMan policeMan= hrService.getAvailablePoliceMans().get(index);
        int salary = policeMan.getSalary();
        hrService.getPoliceManRepository().delete(policeMan);
        budget += salary;
    }
    public void addPoliceMan(PoliceMan policeMan) throws Exception{
        if(budget<policeMan.getSalary()){
            throw new Exception("Недостаточно средств");
        }
        hrService.getPoliceManRepository().add(policeMan);
        budget-=policeMan.getSalary();
    }
    @JsonIgnore
    @Override
    public ConsoleInput getInput() {
        return userInterface.getConsoleInput();
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return new InitialState();
    }

}
