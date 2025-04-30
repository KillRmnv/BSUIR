package by.romanov.ppois;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)

public class Case {
    private List<String> contacts;
    private List<Suspect> suspects;
    private Law law;
    private Integer type;
    private Traits commonTraits;

    public Case() {
        contacts = new ArrayList<>();
        suspects = new ArrayList<>();
        law = new Law();
        commonTraits = new Traits();
        type=1;
    }

    public boolean empty() {
        if (contacts.isEmpty() && suspects.isEmpty() && law.getPunishment().isEmpty() && law.getDescription().isEmpty()) {
            return true;
        }
        return false;
    }

    public Case(Law law, List<String> contacts) {
        this.law = law;
        this.contacts = contacts;
        suspects = new ArrayList<>();
    }

    public Case(HashMap<Integer, Law> laws) {
        Random randLaw = new Random();
        Integer rand = randLaw.nextInt(laws.size());
        Law brokenLaw = laws.get(rand);
        contacts = generateRandomContacts();
        type = 1;
        this.law = brokenLaw;
        this.commonTraits = new Traits(true);
        this.suspects = new ArrayList<>();
    }

    private List<String> generateRandomContacts() {
        List<String> contacts = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            contacts.add(generateSimplePhone());
        }
        return contacts;
    }

    private String generateSimplePhone() {
        Random random = ThreadLocalRandom.current();
        StringBuilder phone = new StringBuilder("+");
        for (int i = 0; i < 9; i++) {
            phone.append(random.nextInt(10));
        }
        return phone.toString();
    }
}
