package by.romanov.ppois.StateMachine.Police;


import by.romanov.ppois.Ui.ConsoleInput;

public class PoliceInput  {
    private ConsoleInput input;
    public int chooseDepartment()  {
      return  input.getChoice( """
                        Выберите отдел:
                        1. Центр управления
                        2. Отдел расследований
                        3. Отдел исполнения
                        4. Отдел кадров
                        5. Отдел по общественной безопасности
                        """,1,5);
    }

    public PoliceInput(ConsoleInput input) {
        this.input = input;
    }
}
