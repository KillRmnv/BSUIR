package by.romanov.ppois.StateMachine.HRDepartment;
import by.romanov.ppois.Repository.Source;
import by.romanov.ppois.StateMachine.StateMachine;
import lombok.Data;

@Data
public class HRDepartment extends StateMachine {
    public HRDepartment(HRDepartmentContext context, Source source) {
        super(context,source);
    }
}
