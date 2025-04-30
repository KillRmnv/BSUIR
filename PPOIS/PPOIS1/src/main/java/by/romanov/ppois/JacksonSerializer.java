package by.romanov.ppois;

import by.romanov.ppois.ControleCentre.ControlCentre;
import by.romanov.ppois.ControleCentre.ControlCentreContext;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartment;
import by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext;
import by.romanov.ppois.HRDepartment.HRDepartment;
import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartment;
import by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext;
import by.romanov.ppois.Police.PoliceContext;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartment;
import by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;

public class JacksonSerializer {
    private static final ObjectMapper objectMapper = new ObjectMapper()
            .registerModule(new JavaTimeModule());

    public static String serialize(Object object) throws IOException {
        return objectMapper.writeValueAsString(object);
    }

    public static <T> T deserialize(String json, Class<T> valueType) throws IOException {
        return objectMapper.readValue(json, valueType);
    }

    public static void saveToFile(Object object, String filename) throws IOException {
        objectMapper.writeValue(new File(filename), object);
    }

    public static <T> T loadFromFile(String filename, Class<T> valueType) throws IOException {
        return objectMapper.readValue(new File(filename), valueType);
    }

    public static PoliceContext load() throws Exception {
        EnforcementDepartmentContext enforcementContext;
        HRDepartmentContext hrContext;
        InvestigationDepartmentContext investigationContext;
        PublicSafetyDepartmentContext publicSafetyContext;
        ControlCentreContext controlCentreContext;
        SuspectSource suspectSource = new SuspectSource();
        for (int i = 0; i < 30; i++) {
            Traits randomTraits = new Traits(true);
            Suspect randomSuspect = new Suspect();
            randomSuspect.setTraits(randomTraits);
            suspectSource.addSuspect(randomSuspect);
        }

        HashMap<Integer, PoliceMan> policeMans = new HashMap<>();
        for (int i = 0; i < 5; i++) {
            PoliceMan newPoliceMan = new PoliceMan(i);
            policeMans.put(i, newPoliceMan);
        }
        LawRegistry laws=new LawRegistry();
        File file = new File("./src/main/resources/by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext.json");
        if (file.exists()) {
            enforcementContext = loadFromFile(
                    "./src/main/resources/by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext.json",
                    EnforcementDepartmentContext.class);

        }else{
            enforcementContext=new EnforcementDepartmentContext(policeMans);
            objectMapper.writeValue(
                    new File("./src/main/resources/by.romanov.ppois.EnforcementDepartment.EnforcementDepartmentContext.json"),
                    enforcementContext
            );
        }
        file = new File("./src/main/resources/by.romanov.ppois.HRDepartment.HRDepartmentContext.json");
        if (file.exists()) {
            hrContext = loadFromFile(
                    "./src/main/resources/by.romanov.ppois.HRDepartment.HRDepartmentContext.json",
                    HRDepartmentContext.class);
        }else{
            hrContext=new HRDepartmentContext(policeMans);
            objectMapper.writeValue(
                    new File("./src/main/resources/by.romanov.ppois.HRDepartment.HRDepartmentContext.json"),
                    hrContext
            );
        }


        file = new File("./src/main/resources/by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext.json");
        if (file.exists()) {
            investigationContext = loadFromFile(
                    "./src/main/resources/by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext.json",
                    InvestigationDepartmentContext.class);
        }else{
            investigationContext=new InvestigationDepartmentContext(suspectSource);
            objectMapper.writeValue(
                    new File("./src/main/resources/by.romanov.ppois.InvestigationDepartment.InvestigationDepartmentContext.json"),
                    investigationContext
            );
        }


        file = new File("./src/main/resources/by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext.json");
        if (file.exists()) {
            publicSafetyContext = loadFromFile(
                    "./src/main/resources/by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext.json",
                    PublicSafetyDepartmentContext.class);
        }else{
            publicSafetyContext=new PublicSafetyDepartmentContext(laws);
            objectMapper.writeValue(
                    new File("./src/main/resources/by.romanov.ppois.PublicSafetyDepartment.PublicSafetyDepartmentContext.json"),
                    publicSafetyContext
            );
        }


        file = new File("./src/main/resources/by.romanov.ppois.ControleCentre.ControlCentreContext.json");
        if (file.exists()) {
            controlCentreContext = loadFromFile(
                    "./src/main/resources/by.romanov.ppois.ControleCentre.ControlCentreContext.json",
                    ControlCentreContext.class);
        }else{
            controlCentreContext=new ControlCentreContext(suspectSource,laws);
            objectMapper.writeValue(
                    new File("./src/main/resources/by.romanov.ppois.ControleCentre.ControlCentreContext.json"),
                    controlCentreContext
            );
        }
        return new PoliceContext(controlCentreContext, investigationContext,
                enforcementContext, hrContext, publicSafetyContext);
    }
}