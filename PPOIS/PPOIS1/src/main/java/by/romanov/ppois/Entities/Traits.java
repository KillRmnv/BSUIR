package by.romanov.ppois.Entities;

import lombok.Data;

import java.util.Random;

@Data
public class Traits {
    private String hairColor;
    private int height;
    private int age;
    private int weight;
    private static final String[] HAIR_COLORS = {
            "Чёрный", "Каштановый", "Рыжий", "Русый", "Седой", "Блондин", "Ненатуральный"
    };

    public Traits() {}

    public Traits(Boolean rand) {
        Random random = new Random();
        int randNum = random.nextInt(95);
        if(rand) {
            this.age = randNum * 100 + randNum + random.nextInt(5);
            randNum = 130 + random.nextInt(80);
            this.height = randNum * 1000 + randNum + random.nextInt(10);
            randNum = 30 + random.nextInt(130);
            this.weight = randNum * 1000 + randNum + random.nextInt(20);

        }else{
            this.age = randNum   ;
            randNum = 130 + random.nextInt(80);
            this.height = randNum  ;
            randNum = 30 + random.nextInt(130);
            this.weight = randNum;
        }
        this.hairColor = HAIR_COLORS[random.nextInt(HAIR_COLORS.length)];
    }

    public Traits(Traits traits) {
        this.hairColor = traits.hairColor;
        this.height = traits.height;
        this.age = traits.age;
        this.weight = traits.weight;
    }
}