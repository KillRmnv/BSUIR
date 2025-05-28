package by.romanov.ppois.Entities;

import lombok.Data;

import java.util.HashMap;

@Data
public class LawRegistry {
    private HashMap<Integer, Law> CRIMINAL_LAWS;
    private HashMap<Integer, Law> ADMIN_LAWS;

    public LawRegistry() {
        CRIMINAL_LAWS = new HashMap<>();
        ADMIN_LAWS = new HashMap<>();

    }

    public String printCriminalLaws() {
        StringBuilder laws = new StringBuilder();
        for (var law : CRIMINAL_LAWS.values()) {
            laws.append("Закон ");
            laws.append(law.getId());
            laws.append(" \n");
            laws.append(law.getDescription());
            laws.append("\n");
            laws.append(law.getPunishment());
            laws.append("\n");
        }
        return laws.toString();
    }

    public String printAdminLaws() {
        StringBuilder laws = new StringBuilder();

        for (var law : ADMIN_LAWS.values()) {
            laws.append("Закон ");
            laws.append(law.getId());
            laws.append(" \n");
            laws.append(law.getDescription());
            laws.append("\n");
            laws.append(law.getPunishment());
            laws.append("\n");
        }
        return laws.toString();
    }
}