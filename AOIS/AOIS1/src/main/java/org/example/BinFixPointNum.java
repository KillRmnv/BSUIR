package org.example;

import java.util.ArrayList;

public class BinFixPointNum {
    private ArrayList<Integer> num= new ArrayList<>();
    ArrayList<Integer> Getter(){
        return num;
    }
    void Setter(ArrayList<Integer> anthrBin){
        num.clear();
        num.addAll(anthrBin);
    }
}