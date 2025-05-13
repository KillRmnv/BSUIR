package by.romanov.ppois.StateMachine.EnforcementDepartment;
import by.romanov.ppois.Repository.Source;
import by.romanov.ppois.StateMachine.StateMachine;
import lombok.Data;

@Data
public class EnforcementDepartment extends StateMachine {

    public EnforcementDepartment(EnforcementDepartmentContext context, Source source) {
        super(context,source);
    }
}
