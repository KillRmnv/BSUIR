package pbz.Romanov.entities;

import lombok.Data;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Data
public class HistoryRecord {
    private String date=null;
    private Integer printing=-1;
    private Employee employee;
    private int numOfPublication=-1;
    private int received=-1;
    private int writeOut=-1;

    private boolean dateCheck(String date) {
        Pattern date_check = Pattern.compile("\\d{4}-((1[0-2])|(0?[1-9]))-((3[0-1])|([0-2]?\\d))$");
        Matcher matcher = date_check.matcher(date);
        if (matcher.matches()) {
            return true;
        } else throw new IllegalArgumentException("Invalid date format(YYYY-MM-DD)");
    }

    public HistoryRecord(String date, int employeeId, Integer printing, int numOfPublication, int received, int writeOut) {
        if (dateCheck(date))
            this.date = date;
        this.employee = new Employee(employeeId);
        this.printing = printing;
        this.numOfPublication = numOfPublication;
        this.received = received;
        this.writeOut = writeOut;
    }

    public void setDate(String date) {
        if (dateCheck(date))
            this.date = date;
    }
    public HistoryRecord() {}

}
