package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Set;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class SubscriptionFrequency {
    protected static final Set<String> ALLOWED = Set.of("год", "полгода");

    protected Integer freqId;
    protected String freqName;

    public void setFreqName(String name) {
        if (name == null || !ALLOWED.contains(name.trim()))
            throw new IllegalArgumentException("Invalid subscription frequency: " + name);
        this.freqName = name.trim();
    }
}
