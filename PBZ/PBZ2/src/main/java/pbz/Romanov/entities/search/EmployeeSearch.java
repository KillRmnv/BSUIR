package pbz.Romanov.entities.search;

import lombok.Getter;
import lombok.Setter;
import pbz.Romanov.entities.Employee;

@Getter
@Setter
public class EmployeeSearch extends Employee {

    @Override
    public void setID(Integer id) {
        this.id = id;
    }

    @Override
    public void setDepartment(Integer department) {
        this.department = department;
    }
}
