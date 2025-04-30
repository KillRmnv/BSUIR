package by.romanov.ppois.Police;


import by.romanov.ppois.Input;

public class PoliceInput  {
    private Input input;
    public int chooseDepartment() {
      return  input.getChoice( """
                        Выберите отдел:
                        1. Центр управления
                        2. Отдел расследований
                        3. Отдел исполнения
                        4. Отдел кадров
                        5. Отдел по общественной безопасности
                        """,1,5);
    }

    public PoliceInput(Input input) {
        this.input = input;
    }
}
