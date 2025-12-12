package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class PublicationType {
    protected Integer typeId;
    protected String typeName;

    public void setTypeId(int id) {
        if (id < 1)
            throw new IllegalArgumentException("Type ID must be positive");
        this.typeId = id;
    }

    public void setTypeName(String name) {
        if (name == null || name.isBlank())
            throw new IllegalArgumentException("Publication type name cannot be empty");
        this.typeName = name.trim();
    }
}
