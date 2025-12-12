package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Set;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class Frequency {
    private static final Set<String> ALLOWED = Set.of(
            "ежедневно", "еженедельно", "ежемесячно", "ежеквартально", "раз в полгода"
    );

    protected Integer freqId;
    protected String freqName;

    public void setFreqId(int id) {
        if (id < 1)
            throw new IllegalArgumentException("Frequency ID must be > 0");
        this.freqId = id;
    }

    public void setFreqName(String name) {
        if (name == null || !ALLOWED.contains(name.trim()))
            throw new IllegalArgumentException("Invalid frequency name: " + name);
        this.freqName = name.trim();
    }
}
