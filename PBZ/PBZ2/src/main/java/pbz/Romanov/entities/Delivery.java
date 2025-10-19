package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
@NoArgsConstructor
@AllArgsConstructor
@Data
public class Delivery {
    private int id=-1;
    private String type;
    private String date=null;

    public Delivery(int deliveryId) {
        this.id = deliveryId;
    }

    public void setDate(String date) {
        Pattern date_check = Pattern.compile("\\d{4}-((1[0-2])|(0?[1-9]))-((3[0-1])|([0-2]?\\d))$");
        Matcher matcher = date_check.matcher(date);
        if (matcher.matches()) {
            this.date = date;
        } else throw new IllegalArgumentException("Invalid date format(YYYY-MM-DD)");
    }


}
