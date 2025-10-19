package pbz.Romanov.entities;

import lombok.Data;

import java.util.List;

@Data
public class Employee {
    private int id = -1;
    private String firstName;
    private String secondName;
    private String thirdName;
    private String position;
    private String department;
    private List<Subscription> subs;

    public void setID(int id) {
        if (id > 0) {
            this.id = id;
        } else throw new IllegalArgumentException("ID must be greater than 0");
    }


    public Employee(int id, String name, String secondName, String thirdName, String position, String department, List<Subscription> subs) {
        this.id = id;
        this.firstName = name;
        this.secondName = secondName;
        this.thirdName = thirdName;
        this.position = position;
        this.department = department;
        this.subs = subs;
        for (Subscription sub : subs) {
            sub.setEmployeeId(id);
        }

    }

    public Employee(int id) {
        this.id = id;
    }
    public  Employee(){

    }
}
