package by.romanov.ppois.ControleCentre;

import by.romanov.ppois.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ControlCentereInput {
    Input input;

    ControlCentereInput() {
        input = new ConsoleInput();
    }

    public ControlCentereInput(Input input) {
        this.input = input;
    }

    public Law chooseLaw(int choiceInt, LawRegistry laws) {
        switch (choiceInt) {
            case 1:
                input.show(laws.printCriminalLaws());
                return laws.getCRIMINAL_LAWS().get(input.getChoice("Введите номер закона", 0, 9));

            case 2:
                input.show(laws.printAdminLaws());
                return laws.getADMIN_LAWS().get(input.getChoice("Введите номер закона", 0, 9));
        }
        return null;
    }

    public int describeHairColor() {
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

    public int describeSuspect() {
        return input.getChoice("""
                Вы видели подозреваемого?
                1.Да
                2.Нет
                """, 1, 2);
    }

    public List<String> witnessContactData() {
        int amnt = witnesses();
        List<String> contacts = new ArrayList<>();
        for (int i = 0; i < amnt; i++) {
            String contact = input.getRegex("Введите email или номер телефона:",
                    "^(\\+\\d{9}|[^@\\s]+@[^@\\s]+)$");
            contacts.add(contact);
        }
        return contacts;
    }

    public int witnesses() {
        return input.getChoice("""
                Количество свидетелей:
                """, 0, 99);

    }

    public int receiveCall() {
        return input.getChoice("""
                Выберите причину обращения:
                1. Уголовное преступление
                2. Административное преступление
                """, 1, 2);
    }

    public int chooseOptions() {
        return input.getChoice("""
                1. Написать заявление
                2. Действия с списоком подозреваемых 
                """, 1, 2);
    }
    public int chooseDbAction(){
        return input.getChoice("""
                1. Просмотреть список подозреваемых
                2. Удалить из списка подозреваемых
                3. Добавить в список подозреваемых
                """, 1, 3);
    }
    public void show(Map<String, Suspect> suspectMap){
        int index=0;
        for(var suspect : suspectMap.values()) {
            input.showNum(index);
            index++;
            input.show(suspect.Info());
        }
    }
    public int exactHeight() {
        return input.getChoice("""
                Pост:
                """, 0, 250);
    }
    public int exactWeight() {
        return input.getChoice("""
                Bес:
                """, 0, 300);
    }
    public int exactAge() {
       return input.getChoice("""
                Возраст:
                """, 0, 99);
    }
    public String fullName(){
        return input.getString("Имя Фамилия Отчество:");
    }
    public void noSuchSuspect(){
        input.show("Такого подозреваемого нет");
    }
}