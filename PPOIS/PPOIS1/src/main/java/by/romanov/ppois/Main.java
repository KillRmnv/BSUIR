package by.romanov.ppois;

import by.romanov.ppois.Police.Police;
import by.romanov.ppois.Police.PoliceContext;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;


public class Main {
    public static void main(String[] args) throws Exception {
        Police police;
        PoliceContext policeContext = JacksonSerializer.load();

        police = new Police(policeContext);
        police.runAll(new by.romanov.ppois.Police.PoliceStates.InitialState());
    }
}