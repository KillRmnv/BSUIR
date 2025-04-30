package by.romanov.ppois.Police;

import by.romanov.ppois.State;
import by.romanov.ppois.StateMachine;
import lombok.Data;

@Data
public class Police extends StateMachine {
    public Police() {}
    public Police( PoliceContext context) {
        super(context);
    }

}
