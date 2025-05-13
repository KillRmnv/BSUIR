package by.romanov.ppois.StateMachine.Police;

import by.romanov.ppois.*;
import by.romanov.ppois.Repository.JacksonSerializer;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentre;
import by.romanov.ppois.StateMachine.ControleCentre.ControlCentreContext;
import by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartment;
import by.romanov.ppois.StateMachine.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartment;
import by.romanov.ppois.StateMachine.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartment;
import by.romanov.ppois.StateMachine.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartment;
import by.romanov.ppois.StateMachine.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Ui.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;


@Data
public class PoliceContext implements Context {
    @JsonIgnore
    private ConsoleUserInterface userInterface;
    private Department choice;
    private ControlCentre controlCentre;
    private EnforcementDepartment enforcementDepartment;
    private HRDepartment hrDepartment;
    private InvestigationDepartment investigationDepartment;
    private PublicSafetyDepartment publicSafetyDepartment;

    public PoliceContext() throws Exception {
        controlCentre = new ControlCentre(new ControlCentreContext(),new JacksonSerializer());
        investigationDepartment = new InvestigationDepartment(new InvestigationDepartmentContext(),new JacksonSerializer());
        enforcementDepartment = new EnforcementDepartment(new EnforcementDepartmentContext(),new JacksonSerializer());
        hrDepartment = new HRDepartment(new HRDepartmentContext(),new JacksonSerializer());
        publicSafetyDepartment=new PublicSafetyDepartment(new PublicSafetyDepartmentContext(),new JacksonSerializer());
        userInterface=new ConsoleUserInterface();
    }
    public PoliceContext(ConsoleUserInterface userInterface) {
        controlCentre = new ControlCentre(new ControlCentreContext(),new JacksonSerializer());
        investigationDepartment = new InvestigationDepartment(new InvestigationDepartmentContext(),new JacksonSerializer());
        enforcementDepartment = new EnforcementDepartment(new EnforcementDepartmentContext(),new JacksonSerializer());
        hrDepartment = new HRDepartment(new HRDepartmentContext(),new JacksonSerializer());
        publicSafetyDepartment=new PublicSafetyDepartment(new PublicSafetyDepartmentContext(),new JacksonSerializer());
        this.userInterface=userInterface;
    }
    public PoliceContext(ControlCentreContext controlCentreContext,InvestigationDepartmentContext investigationDepartmentContext,
                         EnforcementDepartmentContext enforcementDepartmentCont
    ,HRDepartmentContext hrDepartmentContext,PublicSafetyDepartmentContext publicSafetyDepartmentContext,ConsoleUserInterface userInterface) throws Exception {
        controlCentre = new ControlCentre(controlCentreContext,new JacksonSerializer());
        investigationDepartment = new InvestigationDepartment(investigationDepartmentContext,new JacksonSerializer());
        enforcementDepartment = new EnforcementDepartment(enforcementDepartmentCont,new JacksonSerializer());
        hrDepartment = new HRDepartment(hrDepartmentContext,new JacksonSerializer());
        publicSafetyDepartment=new PublicSafetyDepartment(publicSafetyDepartmentContext,new JacksonSerializer());
        this.userInterface=userInterface;
    }
    @JsonIgnore
    @Override
    public void setInput(ConsoleInput input) {
        userInterface.setConsoleInput(input);
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return new InitialState();
    }
    @JsonIgnore
    @Override
    public ConsoleInput getInput() {
        return (ConsoleInput) userInterface.getConsoleInput();
    }

    public void setDepartment(Department department) {
        this.choice = department;
    }

}