package by.romanov.ppois.PublicSafetyDepartment;

import by.romanov.ppois.Law;
import by.romanov.ppois.State;
import by.romanov.ppois.StateMachine;
import lombok.Data;

import java.util.HashMap;
import java.util.Map;

@Data
public class PublicSafetyDepartment extends StateMachine {
    public PublicSafetyDepartment() {}
    public PublicSafetyDepartment(PublicSafetyDepartmentContext context) {
        super(context);
    }
}
