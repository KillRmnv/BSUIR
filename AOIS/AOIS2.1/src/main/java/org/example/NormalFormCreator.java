package org.example;
import java.util.ArrayList;
import java.util.HashMap;

import java.util.Iterator;
import java.util.LinkedHashMap;

public class NormalFormCreator {
    public HashMap<String,Object> SDNF(ArrayList<ArrayList<Integer>> truthTable, LinkedHashMap<String,Character> statements){
        String result=new String();
        ArrayList<Integer> NumericalForm=new ArrayList<>();
        Iterator<String> keyIterator ;
        for(var line=0;line<truthTable.size();line++){
            if(truthTable.get(line).getLast()==1){
                NumericalForm.add(line);
                keyIterator = statements.keySet().iterator();
                result+="(";
                for(int i=0;keyIterator.hasNext();i++){
                    String  key = keyIterator.next();
                    if(truthTable.get(line).get(i)==1){
                        result+=key+"&";
                    }else {
                        result+="!"+key+"&";
                    }
                }
                result= result.substring(0,result.length()-1);
                result+=")";
                result+="|";
            }
        }
        result= result.substring(0,result.length()-1);
        HashMap<String,Object> resultMap=new HashMap<>();
        resultMap.put("NumericalForm",NumericalForm);
        resultMap.put("result",result);
        return resultMap;
    }
    public HashMap<String,Object> SKNF(ArrayList<ArrayList<Integer>> truthTable, LinkedHashMap<String,Character> statements){
        String result=new String();
        ArrayList<Integer> NumericalForm=new ArrayList<>();
        Iterator<String> keyIterator ;
        for(var line=0;line<truthTable.size();line++){
            if(truthTable.get(line).getLast()==0){
                NumericalForm.add(line);
                keyIterator = statements.keySet().iterator();
                result+="(";
                for(int i=0;keyIterator.hasNext();i++){
                    String key = keyIterator.next();
                    if(truthTable.get(line).get(i)==0){
                        result+=key+"|";
                    }else {
                        result+="!"+key+"|";
                    }
                }
                result=result.substring(0,result.length()-1);
                result+=")";
                result+="&";
            }
        }
        result= result.substring(0,result.length()-1);
        HashMap<String,Object> resultMap=new HashMap<>();
        resultMap.put("NumericalForm",NumericalForm);
        resultMap.put("result",result);
        return resultMap;
    }
    public ArrayList<Integer> IndexForm(TruthTable truthTable){
        ArrayList<Integer> NumericalForm=new ArrayList<>();
        for(var line:truthTable.getCombinations()){
            NumericalForm.add(line.getLast());
        }
        return NumericalForm;
    }
}