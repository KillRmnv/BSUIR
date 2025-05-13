package by.romanov.ppois.StateMachine.PublicSafetyDepartment;

import by.romanov.ppois.Repository.Source;
import by.romanov.ppois.StateMachine.StateMachine;
import lombok.Data;

@Data
public class PublicSafetyDepartment extends StateMachine {
    public PublicSafetyDepartment() {}
    public PublicSafetyDepartment(PublicSafetyDepartmentContext context, Source source) {
        super(context,source);
    }
}
