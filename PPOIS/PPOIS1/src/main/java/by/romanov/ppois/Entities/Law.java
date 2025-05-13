package by.romanov.ppois.Entities;
import lombok.Data;
import lombok.Getter;

@Data
public class Law {
    private int id;
    private String description;
    private String punishment;
    private String type;
    public Law(){
        description="";
        punishment="";
    }
    public Law(int id, String description, String punishment) {
        this.id = id;
        this.description = description;
        this.punishment = punishment;
    }

}
