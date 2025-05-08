package by.romanov.ppois.PublicSafetyDepartment;

import by.romanov.ppois.StateMachine;
import lombok.Data;

@Data
public class PublicSafetyDepartment extends StateMachine {
    public PublicSafetyDepartment() {}
    public PublicSafetyDepartment(PublicSafetyDepartmentContext context) {
        super(context);
    }
}
