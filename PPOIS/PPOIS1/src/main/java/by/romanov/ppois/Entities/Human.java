package by.romanov.ppois.Entities;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.Random;

@Data
public class Human {
    protected String name;
    protected String secondName;
    protected String thirdName;
    protected Traits traits;
    public Human() {
        name="Human";
        secondName="Human";
        thirdName="Human";
        traits=new Traits();
    }
    public Human(String name, String secondName,String thirdName, Traits age) {
        this.name = name;
        this.secondName = secondName;
        this.thirdName=thirdName;
        this.traits = age;
    }
    @JsonIgnore
    public String getFullName(){
        StringBuilder suspectFullName=new StringBuilder();
        suspectFullName.append(name);
        suspectFullName.append(" ");
        suspectFullName.append(secondName);
        suspectFullName.append(" ");
        suspectFullName.append(thirdName);
        return suspectFullName.toString().trim();
    }
    protected static final String[] FIRST_NAMES = {
            "Иван", "Пётр", "Сергей", "Алексей", "Дмитрий", "Михаил", "Егор",
            "Андрей", "Виктор", "Юрий", "Артур", "Никита", "Фёдор", "Роман", "Тимофей", "Максим"
    };

    protected static final String[] LAST_NAMES = {
            "Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Соколов", "Попов",
            "Волков", "Семенов", "Фролов", "Морозов", "Орлов", "Зайцев", "Белый", "Гаврилов", "Карпов"
    };

    protected static final String[] PATRONYMICS = {
            "Иванович", "Петрович", "Сергеевич", "Алексеевич", "Дмитриевич", "Михайлович", "Егорович",
            "Андреевич", "Юрьевич", "Артурович", "Максимович", "Фёдорович", "Романович", "Никитич"
    };


    protected void generateRandomName() {
        Random random = new Random();
        this.name = FIRST_NAMES[random.nextInt(FIRST_NAMES.length)];
        this.secondName = LAST_NAMES[random.nextInt(LAST_NAMES.length)];
        this.thirdName = PATRONYMICS[random.nextInt(PATRONYMICS.length)];
    }

}
