package by.romanov.ppois.Entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)

public class Case {
    private List<String> contacts;
    private List<Suspect> suspects;
    private Law law;
    private Integer type;
    private Traits commonTraits;
    private boolean active;

    public Case() {
        contacts = new ArrayList<>();
        suspects = new ArrayList<>();
        law = new Law();
        commonTraits = new Traits();
        type=1;
        active=true;
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
        active=true;
    }

    public Case(HashMap<Integer, Law> laws) {
        Random randLaw = new Random();
        int rand = randLaw.nextInt(laws.size()-1);
        if(rand==0){
            rand++;
        }
        Law brokenLaw = laws.get(rand);
        contacts = generateRandomContacts();
        type = 1;
        this.law = brokenLaw;
        this.commonTraits = new Traits(true);
        this.suspects = new ArrayList<>();
        active=true;
    }
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Case aCase = (Case) o;
        return active == aCase.active &&
                Objects.equals(contacts, aCase.contacts) &&

                Objects.equals(law, aCase.law) &&
                Objects.equals(type, aCase.type) ;
    }

    @Override
    public int hashCode() {
        return Objects.hash(contacts, suspects, law, type, commonTraits, active);
    }
    private List<String> generateRandomContacts() {
        List<String> contacts = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            contacts.add(generateSimplePhone());
        }
        return contacts;
    }
    public String generateSimplePhone() {
        Random random = ThreadLocalRandom.current();
        StringBuilder phone = new StringBuilder("+");
        for (int i = 0; i < 9; i++) {
            phone.append(random.nextInt(10));
        }
        return phone.toString();
    }
}
