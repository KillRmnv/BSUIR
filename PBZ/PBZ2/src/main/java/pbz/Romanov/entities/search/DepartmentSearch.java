package pbz.Romanov.entities.search;

import lombok.Getter;
import lombok.Setter;
import pbz.Romanov.entities.Department;

@Getter
@Setter
public class DepartmentSearch extends Department {

    @Override
    public void setDepartmentId(Integer id) {
        this.departmentId = id;
    }

    @Override
    public void setDepartmentName(String name) {
        this.departmentName = (name != null) ? name.trim() : null;
    }
}
