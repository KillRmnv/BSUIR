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
        type="ADMIN";
    }
    public Law(int id, String description, String punishment,String type) {
        this.id = id;
        this.description = description;
        this.punishment = punishment;
        this.type = type;
    }
    public void setType(String type){
        if(type.equals("ADMIN")||type.equals("CRIMINAL")){
            this.type=type;
        }else{
            throw new IllegalArgumentException("Invalid type");
        }
    }


}
