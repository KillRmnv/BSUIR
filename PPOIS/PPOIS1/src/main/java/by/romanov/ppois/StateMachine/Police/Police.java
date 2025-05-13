package by.romanov.ppois.StateMachine.Police;

import by.romanov.ppois.Repository.Source;
import by.romanov.ppois.StateMachine.StateMachine;
import lombok.Data;

@Data
public class Police extends StateMachine {
    public Police() {}
    public Police(PoliceContext context, Source source) {
        super(context,source);
    }

}
