package ppois.romanov.entities;

import lombok.Data;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Data
public class FullName {
    private String firstName;
    private String secondName;
    private String lastName;

    public FullName() {
        firstName = "";
        secondName = "";
        lastName = "";
    }

    public FullName(String name) {
        firstName = "";
        secondName = "";
        lastName = "";
        setFullName(name);
    }

    public FullName(String firstName, String secondName, String lastName) {
        this.firstName = firstName;
        this.secondName = secondName;
        this.lastName = lastName;
    }

    public String getFullName() {
        return firstName + " " + secondName + " " + lastName;
    }

    public void setFullName(String fullName) {
        Pattern wordPattern = Pattern.compile("[\\p{L}0-9]+");
        Matcher matcher = wordPattern.matcher(fullName);

        while (matcher.find()) {
            if (firstName.isEmpty())
                firstName = matcher.group();
            else
            if (secondName.isEmpty())
                secondName = matcher.group();
            else
            if (lastName.isEmpty()) {
                lastName = matcher.group();
                return;
            }
            fullName = fullName.replaceFirst(matcher.group(), "");
        }
    }
}
