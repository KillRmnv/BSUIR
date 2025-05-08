package by.romanov.ppois.Entities;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Data
public class PoliceMan extends Human {
    @Getter @Setter
    int id;
    int experience;
    int salary;
    public PoliceMan(){}
    public PoliceMan(String name, String secondName, String thirdName, Traits traits,
                     int id, int experience, int salary) {
        super(name, secondName, thirdName, traits);
        this.id = id;
        this.experience = experience;
        this.salary = salary;
    }

    public PoliceMan(int id) {
        generateRandomName();
        this.id = id;
        this.experience = generateRandomExperience();
        this.salary = calculateSalary();
    }

    private int generateRandomExperience() {
        Random random = new Random();
        double lambda = 0.05;
        double expValue = -Math.log(1 - random.nextDouble()) / lambda;
        return (int)Math.min(100, expValue);
    }

    private int calculateSalary() {
        int baseSalary = 500;
        int experienceBonus = experience * 30;
        Random random = new Random();
        double randomFactor = 0.8 + random.nextDouble() * 0.4;

        return (int)((baseSalary + experienceBonus) * randomFactor);
    }

    public void gainExperience(int years) {
        this.experience += years;
        this.salary = calculateSalary();
    }
   public List<String> Info(){
        List<String> policeManInfo = new ArrayList<>();
        policeManInfo.add(getFullName());
        policeManInfo.add("Опыт:"+experience);
        policeManInfo.add("Зарплата:"+salary);
        return policeManInfo;
   }

}