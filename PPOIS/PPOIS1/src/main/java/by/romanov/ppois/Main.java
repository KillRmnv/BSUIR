package by.romanov.ppois;

import by.romanov.ppois.Repository.JacksonSerializer;
import by.romanov.ppois.Repository.Source;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.StateMachine;
import by.romanov.ppois.Ui.ConsoleUserInterface;

public class Main {
    public static void main(String[] args) throws Exception {
        StateMachine police;
        Source source=new JacksonSerializer();
        Context policeContext = (Context) source.load(new ConsoleUserInterface());
        police = new StateMachine(policeContext,source);
        police.runAll(new InitialState());
    }
}