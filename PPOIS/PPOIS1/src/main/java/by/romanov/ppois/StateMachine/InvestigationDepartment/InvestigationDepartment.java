package by.romanov.ppois.StateMachine.InvestigationDepartment;
import by.romanov.ppois.Repository.Source;
import by.romanov.ppois.StateMachine.StateMachine;
import lombok.Data;

@Data
public class InvestigationDepartment extends StateMachine {
    public InvestigationDepartment(InvestigationDepartmentContext context, Source source) {
        super(context,source);
    }
}
