package by.romanov.ppois.Police;

import by.romanov.ppois.*;
import by.romanov.ppois.ControleCentre.ControlCentre;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartment;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.HRDepartment.HRDepartment;
import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartment;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartment;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.HashMap;

@Data
public class PoliceContext implements Context {
    @JsonIgnore
    private Input input;
    private Department choice;
    private ControlCentre controlCentre;
    private EnforcementDepartment enforcementDepartment;
    private HRDepartment hrDepartment;
    private InvestigationDepartment investigationDepartment;
    private PublicSafetyDepartment publicSafetyDepartment;
    public PoliceContext() throws Exception {
        SuspectSource suspectSource = new SuspectSource();
        for (int i = 0; i < 30; i++) {
            Traits randomTraits = new Traits(true);
            Suspect randomSuspect = new Suspect();
            randomSuspect.setTraits(randomTraits);
            suspectSource.addSuspect(randomSuspect);
        }

        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        for (int i = 0; i < 5; i++) {
            PoliceMan newPoliceMan = new PoliceMan(i);
            policeMans.put(i, newPoliceMan);
        }

        LawRegistry laws=new LawRegistry();
        controlCentre = new ControlCentre(new ControlCentreContext(suspectSource, laws));
        investigationDepartment = new InvestigationDepartment(new InvestigationDepartmentContext(suspectSource));
        enforcementDepartment = new EnforcementDepartment(new EnforcementDepartmentContext(policeMans));
        hrDepartment = new HRDepartment(new HRDepartmentContext(policeMans));
        input = new ConsoleInput();
        publicSafetyDepartment=new PublicSafetyDepartment(new PublicSafetyDepartmentContext(laws));
    }
    public PoliceContext(ControlCentreContext controlCentreContext,InvestigationDepartmentContext investigationDepartmentContext,EnforcementDepartmentContext enforcementDepartmentCont
    ,HRDepartmentContext hrDepartmentContext,PublicSafetyDepartmentContext publicSafetyDepartmentContext) throws Exception {
        controlCentre = new ControlCentre(controlCentreContext);
        investigationDepartment = new InvestigationDepartment(investigationDepartmentContext);
        enforcementDepartment = new EnforcementDepartment(enforcementDepartmentCont);
        hrDepartment = new HRDepartment(hrDepartmentContext);
        input = new ConsoleInput();
        publicSafetyDepartment=new PublicSafetyDepartment(publicSafetyDepartmentContext);
    }

    @Override
    public void setInput(Input input) {
        this.input = input;
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return new InitialState();
    }

    @Override
    public Input getInput() {
        return (Input) input;
    }

    public void setDepartment(Department department) {
        this.choice = department;
    }

}
