package pbz.Romanov.entities;

import lombok.Data;

import java.util.List;

@Data
public class Employee {
    protected Integer id;
    protected String firstName;
    protected String secondName;
    protected String thirdName;
    protected String position;
    protected Integer department;

    public void setID(Integer id) {
        if (id > 0) {
            this.id = id;
        } else throw new IllegalArgumentException("ID must be greater than 0");
    }
    public void setDepartment(Integer department) {
        if (department > 0) {
            this.department = department;

        }else throw new IllegalArgumentException("Department must be greater than 0");
    }
    public Employee(Integer id, String name, String secondName, String thirdName, String position, Integer department) {
        setID(id);
        this.firstName = name;
        this.secondName = secondName;
        this.thirdName = thirdName;
        this.position = position;
        this.department = department;
    }

    public Employee(Integer id) {
        setID(id);
    }
    public  Employee(){

    }
}
