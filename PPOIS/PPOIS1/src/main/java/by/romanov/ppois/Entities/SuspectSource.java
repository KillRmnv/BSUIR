package by.romanov.ppois.Entities;

import lombok.Data;

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

@Data
public class SuspectSource {

    private Map<String, Suspect> suspects;
    private Map<String, Map<Integer, Set<String>>> suspectTraits;

    public SuspectSource() {
        suspects = new HashMap<>();
        suspectTraits = new HashMap<>();
    }

    public void addSuspect(Suspect suspect) {
        String fullName = suspect.getFullName();
        suspects.put(fullName, suspect);
        Traits traits = suspect.getTraits();
        Map<Integer, Set<String>> suspectsByTraits = suspectTraits.getOrDefault("Hair", new HashMap<>());
        Set<String> names = suspectsByTraits.getOrDefault(traitNumHair(traits.getHairColor()),new HashSet<>());
        names.add(fullName);
        suspectsByTraits.put(traitNumHair(traits.getHairColor()), names);
        suspectTraits.put("Hair", suspectsByTraits);
        suspectsByTraits = suspectTraits.getOrDefault("Age", new HashMap<>());
        names = suspectsByTraits.getOrDefault(traits.getAge() / 10,new HashSet<>());
        names.add(fullName);
        suspectsByTraits.put(traits.getAge() / 10, names);
        suspectTraits.put("Age", suspectsByTraits);
        suspectsByTraits = suspectTraits.getOrDefault("Weight", new HashMap<>());
        names = suspectsByTraits.getOrDefault(traits.getWeight() / 10,new HashSet<>());
        names.add(fullName);
        suspectsByTraits.put(traits.getWeight() / 10, names);
        suspectTraits.put("Weight", suspectsByTraits);
        suspectsByTraits = suspectTraits.getOrDefault("Height", new HashMap<>());
        names = suspectsByTraits.getOrDefault((int) (traits.getHeight() * 10),new HashSet<>());
        names.add(fullName);
        suspectsByTraits.put((int) (traits.getHeight() * 10), names);
        suspectTraits.put("Height", suspectsByTraits);

    }

    public static int traitNumHair(String traitName) {
        return switch (traitName) {
            case "Чёрный" -> 1;
            case "Каштановый" -> 2;
            case "Рыжий" -> 3;
            case "Русый" -> 4;
            case "Седой" -> 5;
            case "Блондин" -> 6;
            case "Ненатуральный" -> 7;
            default -> 0;
        };
    }

    public static String traitStringHair(int num) {
        switch (num) {
            case 1:
                return "Чёрный";
            case 2:
                return "Каштановый";
            case 3:
                return "Рыжий";
            case 4:
                return "Русый";
            case 5:
                return "Седой";
            case 6:
                return "Блондин";
            case 7:
                return "Ненатуральный";
            default:
                return "Неизвестно";
        }
    }

    public boolean deleteSuspect(String suspectName) {
        if (suspects.get(suspectName) == null) {
            return false;
        }
        Traits traits = new Traits(suspects.get(suspectName).getTraits());
        suspects.remove(suspectName);
        Map<Integer, Set<String>> suspectsByTraits = suspectTraits.get("Hair");
        Set<String> names = suspectsByTraits.get(traitNumHair(traits.getHairColor()));
        names.remove(suspectName);
        suspectsByTraits = suspectTraits.get("Age");
        names = suspectsByTraits.get(traits.getAge() / 10);
        names.remove(suspectName);
        suspectsByTraits.put(traits.getAge() / 10, names);
        suspectTraits.put("Age", suspectsByTraits);
        suspectsByTraits = suspectTraits.get("Weight");
        names = suspectsByTraits.get(traits.getWeight() / 10);
        names.remove(suspectName);
        suspectsByTraits.put(traits.getWeight() / 10, names);
        suspectTraits.put("Weight", suspectsByTraits);
        suspectsByTraits = suspectTraits.get("Height");
        names = suspectsByTraits.get((int) (traits.getHeight() * 10));
        names.remove(suspectName);
        suspectsByTraits.put((int) (traits.getHeight() * 10), names);
        suspectTraits.put("Height", suspectsByTraits);
        return true;
    }

    public static Set<Suspect> intersection(Set<Suspect> set1, Set<Suspect> set2) {
        Set<Suspect> result = new HashSet<>(set1);
        result.retainAll(set2);
        return result;
    }
    private void adjastSuspectByTraits( Map<String,Integer> suspectByTraits,Set<String> suspect1,AtomicInteger max,Set<String> suspectMax){
        if(suspect1==null){
            return;
        }
        for(var sus: suspect1) {
            int amnt=  suspectByTraits.getOrDefault( suspects.get(sus).getFullName(),0);
            amnt++;
            if(amnt>max.get()){
                max.set(amnt);
                suspectMax.clear();
                suspectMax.add(suspects.get(sus).getFullName());
            }else if(amnt==max.get()){
                suspectMax.add(suspects.get(sus).getFullName());
            }
            suspectByTraits.put(sus,amnt);
        }
    }
    public Set<Suspect> findSuspectsBasedOnCommonTraits(List<Traits> traits, AtomicInteger maxTraits) {
        Map<String,Integer> suspectByTraits = new HashMap<>();
        Set<String> suspectMax = new HashSet<>();
        AtomicInteger max=new AtomicInteger(0);
        for (var trait : traits) {
            Set<String> suspect1 = suspectTraits.get("Hair").get(traitNumHair(trait.getHairColor()));
            adjastSuspectByTraits(suspectByTraits,suspect1,max,suspectMax);
            int lowerLimit=trait.getAge() / 100;
            int upperLimit=trait.getAge() % 100;
            for(int beg=lowerLimit; beg<=upperLimit; beg+=10) {
                suspect1 = suspectTraits.get("Age").get(beg);
                adjastSuspectByTraits(suspectByTraits,suspect1,max,suspectMax);
            }
            lowerLimit=trait.getWeight() / 1000;
            upperLimit=trait.getWeight() % 1000;
            for(int beg=lowerLimit; beg<=upperLimit; beg+=10) {
                suspect1 = suspectTraits.get("Weight").get(beg);
                adjastSuspectByTraits(suspectByTraits,suspect1,max,suspectMax);
            }
            lowerLimit=trait.getHeight() / 1000;
            upperLimit=trait.getWeight() % 1000;
            for(int beg=lowerLimit; beg<=upperLimit; beg+=10) {
                suspect1 = suspectTraits.get("Height").get(beg);
                adjastSuspectByTraits(suspectByTraits, suspect1,max,suspectMax);
            }
        }
        Set<Suspect> result = new HashSet<>();
        for(var sus:suspectMax){
            result.add(suspects.get(sus));
        }
        maxTraits.set(max.get());
        return result;
    }
}