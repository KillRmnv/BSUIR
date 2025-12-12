package pbz.Romanov.entities;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@NoArgsConstructor
@Data
public class Subscription {
    protected Integer id;
    protected String startingDate = null;
    protected String endingDate = null;
    protected Integer period;
    protected Printing printing;
    protected Integer employeeId;
    protected Integer cost;

    private static final Pattern DATE_PATTERN = Pattern.compile(
            "\\d{4}-((1[0-2])|(0?[1-9]))-((3[0-1])|([0-2]?\\d))$"
    );

    private boolean isValidDate(String date) {
        if (date == null) return true;
        Matcher matcher = DATE_PATTERN.matcher(date);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("Invalid date format: '" + date + "'. Expected: YYYY-MM-DD");
        }
        return true;
    }



    public void setId(Integer id) {
        if (id < 0) {
            throw new IllegalArgumentException("Subscription ID cannot be negative: " + id);
        }
        this.id = id;
    }

    public void setStartingDate(String startingDate) {
        isValidDate(startingDate);
        this.startingDate = startingDate;
    }

    public void setEndingDate(String endingDate) {
        isValidDate(endingDate);
        this.endingDate = endingDate;
    }

    public void setPeriod(Integer period) {
        if (period <= 0) {
            throw new IllegalArgumentException("Period must be positive: " + period);
        }
        this.period = period;
    }

    public void setPrinting(Printing printing) {
        if (printing == null) {
            throw new IllegalArgumentException("Printing cannot be null");
        }
        if (printing.getIndex() <= 0) {
            throw new IllegalArgumentException("Printing index must be positive: " + printing.getIndex());
        }
        this.printing = printing;
    }

    public void setEmployeeId(Integer employeeId) {
        if (employeeId <= 0) {
            throw new IllegalArgumentException("Employee ID must be positive: " + employeeId);
        }
        this.employeeId = employeeId;
    }

    public void setCost(Integer cost) {
        if (cost <= 0) {
            throw new IllegalArgumentException("Cost must be positive: " + cost);
        }
        this.cost = cost;
    }

    public Subscription(Integer id, Integer index, Integer employeeId, String startingDate, String endingDate, Integer period, Integer cost) {
        setId(id);
        setEmployeeId(employeeId);
        setStartingDate(startingDate);
        setEndingDate(endingDate);
        setPeriod(period);
        setCost(cost);
        this.printing = new Printing();
        this.printing.setIndex(index);
    }

}