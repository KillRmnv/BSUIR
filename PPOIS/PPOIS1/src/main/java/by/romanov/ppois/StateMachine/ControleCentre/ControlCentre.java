package by.romanov.ppois.StateMachine.ControleCentre;
import by.romanov.ppois.Repository.Source;
import by.romanov.ppois.StateMachine.StateMachine;
import lombok.Data;

@Data
public class ControlCentre extends StateMachine {

    public ControlCentre(ControlCentreContext context, Source source) {
        super(context,source);
    }
}
