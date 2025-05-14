package by.romanov.ppois.StateMachine.ControleCentre;

import by.romanov.ppois.Entities.Law;
import by.romanov.ppois.Entities.LawRegistry;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Ui.ConsoleInput;
import by.romanov.ppois.Ui.ConsoleUserInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ControlCentereInput {
    ConsoleInput input;

    ControlCentereInput() {
        input = new ConsoleInput();
    }

    public ControlCentereInput(ConsoleInput input) {
        this.input = input;
    }

    public Law chooseLaw(int choiceInt, LawRegistry laws, ConsoleUserInterface userInterface)     {
        switch (choiceInt) {
            case 1:
                userInterface.show(laws.printCriminalLaws());
                return laws.getCRIMINAL_LAWS().get(input.getChoice("Введите номер закона", 1, 10)-1);

            case 2:
                userInterface.show(laws.printAdminLaws());
                return laws.getADMIN_LAWS().get(input.getChoice("Введите номер закона", 1, 10)-1);
        }
        return null;
    }

    public int describeHairColor()     {
        return input.getChoice("""
                Цвет волос:
                0.Не помню
                1.Чёрный
                2.Каштановый
                3.Рыжий
                4.Русый
                5.Седой
                6.Блондин
                7.Ненатуральный
                """, 0, 7);
    }

    public int age() {
        List<Integer> numbers = input.getNumberRange("""
                Примерный возраст:
                """, 0, 99);
        return numbers.get(0) * 100 + numbers.get(1);
    }

    public int weight() {
        List<Integer> numbers = input.getNumberRange("""
                Примерный вес:
                """, 0, 300);

        return numbers.get(0) * 1000 + numbers.get(1);
    }

    public int height() {
        List<Integer> numbers = input.getNumberRange("""
                Примерный рост:
                """, 0, 250);
        return numbers.get(0) * 1000 + numbers.get(1);
    }

    public int describeSuspect()     {
        return input.getChoice("""
                Вы видели подозреваемого?
                1.Да
                2.Нет
                """, 1, 2);
    }

    public List<String> witnessContactData()     {
        int amnt = witnesses();
        List<String> contacts = new ArrayList<>();
        for (int i = 0; i < amnt; i++) {
            String contact = input.getRegex("Введите email или номер телефона(9 цифр):",
                    "^(\\+\\d{9}|[^@\\s]+@[^@\\s]+)$");
            System.out.println("Свидетель добавлен: " + contact);
            contacts.add(contact);
        }
        return contacts;
    }

    public int witnesses()     {
        return input.getChoice("""
                Количество свидетелей:
                """, 0, 99);

    }

    public int receiveCall()     {
        return input.getChoice("""
                Выберите причину обращения:
                1. Уголовное преступление
                2. Административное преступление
                """, 1, 2);
    }

    public int chooseOptions()     {
        return input.getChoice("""
                1. Написать заявление
                2. Действия с списоком подозреваемых 
                """, 1, 2);
    }
    public int chooseSourceAction()     {
        return input.getChoice("""
                1. Просмотреть список подозреваемых
                2. Удалить из списка подозреваемых
                3. Добавить в список подозреваемых
                """, 1, 3);
    }
    public void show(Map<String, Suspect> suspectMap, ConsoleUserInterface userInterface){
        int index=0;
        for(var suspect : suspectMap.values()) {
            userInterface.show(String.valueOf(index));
            index++;
            userInterface.show(suspect.Info());
        }
    }
    public int exactHeight()     {
        return input.getChoice("""
                Pост:
                """, 0, 250);
    }
    public int exactWeight()     {
        return input.getChoice("""
                Bес:
                """, 0, 300);
    }
    public int exactAge()     {
       return input.getChoice("""
                Возраст:
                """, 0, 99);
    }
    public String fullName(){
        return input.getLine("Имя Фамилия Отчество:");
    }

}