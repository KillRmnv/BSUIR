package by.romanov.ppois;

import lombok.Getter;

@Getter
public enum Department{
   POLICE(0), CONTROL_CENTRE(1),INVESTIGATION_DEPARTMENT(2),
    ENFORCEMENT_DEPARTMENT(3),HR_DEPARTMENT(4),PUBLIC_SAFETY_DEPARTMENT(5),EXIT(-1);
    private int code;
    Department(int choice) {
        this.code = choice;
    }
    public void setChoice(int choice) {
        this.code = choice;
    }
    public static Department fromCode(int code) {
        for (Department dep : values()) {
            if (dep.code == code) {
                return dep;
            }
        }
        throw new IllegalArgumentException("Invalid department code: " + code);
    }
}
