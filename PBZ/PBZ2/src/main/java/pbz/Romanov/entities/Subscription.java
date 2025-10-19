package pbz.Romanov.entities;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
@NoArgsConstructor
@Data
public class Subscription {
    private String startingDate=null;
    private String endingDate=null;
    private int amountOfMonths;
    private Delivery delivery;
    private Printing printing;
    private int employeeId;
    private int cost;

    private boolean dateCheck(String date) {
        Pattern date_check = Pattern.compile("\\d{4}-((1[0-2])|(0?[1-9]))-((3[0-1])|([0-2]?\\d))$");
        Matcher matcher = date_check.matcher(date);
        if (matcher.matches()) {
            return true;
        } else throw new IllegalArgumentException("Invalid date format(YYYY-MM-DD)");
    }

    public void setStartingDate(String date) {
        if (dateCheck(date)) {
            this.startingDate = date;
        }
    }

    public void setEndingDate(String date) {
        if (dateCheck(date)) {
            this.endingDate = date;
        }
    }

    public Subscription(int index, int employeeId, String startingDate, String endingDate, int delivery, int period, int cost) {
        this.employeeId = employeeId;
        this.startingDate = startingDate;
        this.endingDate = endingDate;
        this.delivery = new Delivery(delivery);
        this.cost = cost;
        this.amountOfMonths = period;
        this.printing = new Printing(index);
        this.printing.setIndex(index);
    }

}
