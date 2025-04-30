package by.romanov.ppois.InvestigationDepartment;
import by.romanov.ppois.StateMachine;
import lombok.Data;

@Data
public class InvestigationDepartment extends StateMachine {
    public InvestigationDepartment(InvestigationDepartmentContext context) {
        super(context);
    }
}
