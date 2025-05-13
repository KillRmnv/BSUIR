package by.romanov.ppois;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.Traits;
import lombok.Data;

@Data
public class TransferData {
    private Case caseData;
    private Suspect suspectData;
    private PoliceMan policeManData;
    private Traits traits;
    private int choice;
    public TransferData(){
        caseData=new Case();
        suspectData=new Suspect();
        traits=new Traits();
        policeManData=new PoliceMan();
    }
}
