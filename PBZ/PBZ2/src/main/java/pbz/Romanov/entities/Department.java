package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Getter
public class Department {
    protected Integer departmentId;
    protected String departmentName;

    public void setDepartmentId(Integer id) {
        if (id < 1)
            throw new IllegalArgumentException("Department ID must be greater than 0");
        this.departmentId = id;
    }

    public void setDepartmentName(String name) {
        if (name == null || name.isBlank())
            throw new IllegalArgumentException("Department name cannot be empty");
        this.departmentName = name.trim();
    }
}
