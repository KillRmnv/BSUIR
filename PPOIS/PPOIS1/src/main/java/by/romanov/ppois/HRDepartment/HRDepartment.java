package by.romanov.ppois.HRDepartment;
import by.romanov.ppois.StateMachine;
import lombok.Data;

@Data
public class HRDepartment extends StateMachine {
    public HRDepartment(HRDepartmentContext context) {
        super(context);
    }
}
