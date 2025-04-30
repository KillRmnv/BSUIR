package by.romanov.ppois;

import lombok.Data;

@Data
public class TransferData {
    private Case caseData;
    private Suspect suspectData;
    private PoliceMan policeManData;
    private Traits traits;
    public TransferData(){
        caseData=new Case();
        suspectData=new Suspect();
        traits=new Traits();
        policeManData=new PoliceMan();
    }
}
