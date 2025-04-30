package by.romanov.ppois.ControleCentre;
import by.romanov.ppois.StateMachine;
import lombok.Data;

@Data
public class ControlCentre extends StateMachine {

    public ControlCentre(ControlCentreContext context) {
        super(context);
    }
}
