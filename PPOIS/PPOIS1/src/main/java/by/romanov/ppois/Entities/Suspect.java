package by.romanov.ppois.Entities;

import lombok.Data;

import java.util.Random;

@Data
public class Suspect extends Human {
    private int intellegence;

    public Suspect() {
        generateRandomName();

        this.traits = new Traits(true);

        this.intellegence = generateBiasedIntellegence();
    }

    private int generateBiasedIntellegence() {
        Random random = new Random();
        int base = 70 + random.nextInt(91);
        int extra = 70 + random.nextInt(91);
        return Math.max(base, extra);
    }

    public Suspect(String name, String secondName, String thirdName, Traits traits) {
        super(name, secondName, thirdName, traits);
    }

    public Suspect(Suspect suspect) {
        this.intellegence = suspect.intellegence;
        this.name = suspect.name;
        this.secondName = suspect.secondName;
        this.thirdName = suspect.thirdName;
        this.traits = suspect.traits;
    }
    public String Info(){
        StringBuilder info = new StringBuilder();
        info.append(getFullName());
        info.append("\n");
        info.append("Вес:");
        info.append(traits.getWeight());
        info.append("\n");
        info.append("Рост:");
        info.append(traits.getHeight());
        info.append("\n");
        info.append("Возраст:");
        info.append(traits.getAge());
        info.append("\n");
        info.append("Цвет волос:");
        info.append(traits.getHairColor());
        info.append("\n");
        return info.toString();
    }
}
