package by.romanov.ppois.EnforcementDepartment;
import by.romanov.ppois.StateMachine;
import lombok.Data;

@Data
public class EnforcementDepartment extends StateMachine {

    public EnforcementDepartment(EnforcementDepartmentContext context) {
        super(context);
    }
}
