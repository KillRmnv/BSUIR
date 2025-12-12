package pbz.Romanov.entities;

import lombok.Data;
import lombok.Getter;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Getter
public class HistoryRecord {
    protected Integer id;
    protected String date;
    protected Integer numOfPublication;
    protected Integer state;
    protected Integer sub;

    private boolean dateCheck(String date) {
        Pattern date_check = Pattern.compile("\\d{4}-((1[0-2])|(0?[1-9]))-((3[0-1])|([0-2]?\\d))$");
        Matcher matcher = date_check.matcher(date);
        if (matcher.matches()) {
            return true;
        } else throw new IllegalArgumentException("Invalid date format(YYYY-MM-DD)");
    }

    public HistoryRecord(Integer id,String date, Integer numOfPublication, Integer state,Integer sub) {
        setId(id);
        if (dateCheck(date))
            this.date = date;
        setNumOfPublication(numOfPublication);
        setState(state);
        setState(state);
        setSub(sub);
    }

    public void setDate(String date) {
        if (dateCheck(date))
            this.date = date;
    }
    public HistoryRecord() {}
    public  void setId(Integer id) {
        if(id>0){
            this.id = id;
        }else{
            throw new IllegalArgumentException("Invalid id");
        }
    }
    public void setSub(Integer sub) {
        if(sub>0){
            this.sub = sub;

        }else{
            throw new IllegalArgumentException("Invalid sub");
        }
    }
    public void setNumOfPublication(Integer numOfPublication) {
        if(numOfPublication>0){
            this.numOfPublication = numOfPublication;
        }else{
            throw new IllegalArgumentException("Invalid numOfPublication");
        }
    }
    public void setState(Integer state) {
        if(state>-1&&state<3){
            this.state = state;
        }else{
            throw new IllegalArgumentException("Invalid state");
        }
    }
}
