package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@NoArgsConstructor

@Data
public class Delivery {
    protected Integer id;
    protected Integer type;
    protected String address;
    protected Integer histId;
    protected String expectedDate;

    public Delivery(Integer deliveryId) {
        setId(deliveryId);
    }
    public Delivery(Integer id, Integer type, String address, Integer histId, String expectedDate) {
        setId(id);
        setType(type);
        setAddress(address);
        setState(histId);
        setExpectedDate(expectedDate);
    }

    public void setId(Integer id) {
        if (id < 1) {
            throw new IllegalArgumentException("Id must be greater than 0");
        }
        this.id = id;
    }

    public void setType(Integer type) {
        if (type < 1) {
            throw new IllegalArgumentException("Type must be greater than 0");
        }
        this.type = type;
    }

    public void setAddress(String address) {
        if (address == null || address.trim().isEmpty()) {
            throw new IllegalArgumentException("Address cannot be empty");
        }
        if (address.length() > 128) {
            throw new IllegalArgumentException("Address length must not exceed 128 characters");
        }
        this.address = address.trim();
    }

    public void setState(Integer state) {
        if (state < 0) {
            throw new IllegalArgumentException("State must be non-negative");
        }
        this.histId = state;
    }



    public void setExpectedDate(String expectedDate) {
        if (expectedDate == null || expectedDate.trim().isEmpty()) {
            throw new IllegalArgumentException("Expected date cannot be empty");
        }
        if (!dateCheck(expectedDate)) {
            throw new IllegalArgumentException("Invalid date format (expected YYYY-MM-DD)");
        }
        this.expectedDate = expectedDate;
    }

    private boolean dateCheck(String date) {
        Pattern datePattern = Pattern.compile("^\\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01])$");
        Matcher matcher = datePattern.matcher(date);
        return matcher.matches();
    }
}
