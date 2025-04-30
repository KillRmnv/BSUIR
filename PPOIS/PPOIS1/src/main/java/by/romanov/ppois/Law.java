package by.romanov.ppois;
import lombok.Data;

@Data
public class Law {
    private int id;
    private String description;
    private String punishment;
    public Law(){
        description="";
        punishment="";
    }
    public Law(int id, String description, String punishment) {
        this.id = id;
        this.description = description;
        this.punishment = punishment;
    }
    public int getId() {
        return id;
    }
    public String getDescription() {
        return description;
    }
    public String getPunishment() {
        return punishment;
    }
}
