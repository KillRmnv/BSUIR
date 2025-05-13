package by.romanov.ppois.Service;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.Entities.Traits;
import by.romanov.ppois.Repository.CaseJsonRepository;
import by.romanov.ppois.Repository.Repository;
import by.romanov.ppois.Repository.SuspectSourceJsonRepository;

import lombok.Data;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
@Data
public class InvestigationService {
    protected final Repository<List<Case>, Case, Integer> caseRepository;
    protected final Repository<SuspectSource, Suspect,String> suspectRepository;
    public InvestigationService(){
        caseRepository=new CaseJsonRepository();
        suspectRepository=new SuspectSourceJsonRepository();
    }
    public InvestigationService(Repository<List<Case>, Case, Integer> caseRepository, Repository<SuspectSource, Suspect,String> suspectRepository) {
        this.caseRepository = caseRepository;
        this.suspectRepository = suspectRepository;
    }

    public Case chooseCase(int caseIndex) throws IOException {
        List<Case> cases = findActiveCases();
        if (!cases.isEmpty() && caseIndex >= 0 && caseIndex < cases.size()) {
            return cases.get(caseIndex);
        }
        return null;
    }

    public void interviewWitnesses(Case currentCase,List<Traits> witnessTraits) throws IOException {
        AtomicInteger maxWitnesses = new AtomicInteger(0);
        AtomicInteger maxUser = new AtomicInteger(0);
        Set<Suspect> witnessSuspects = suspectRepository.loadAll().findSuspectsBasedOnCommonTraits(witnessTraits, maxWitnesses);
        Set<Suspect> userSuspects = suspectRepository.loadAll().findSuspectsBasedOnCommonTraits(
                new ArrayList<>(Collections.singletonList(currentCase.getCommonTraits())), maxUser);
        if ((double) maxWitnesses.get() > (double) maxUser.get() * 1.5) {
            setSuspects(currentCase, SuspectSource.intersection(witnessSuspects, userSuspects), witnessSuspects.isEmpty(), witnessSuspects.iterator(), witnessSuspects, userSuspects);
        } else {
            setSuspects(currentCase, SuspectSource.intersection(witnessSuspects, userSuspects), userSuspects.isEmpty(), userSuspects.iterator(), witnessSuspects, witnessSuspects);
        }
        caseRepository.delete(currentCase);
        currentCase.setActive(false);
        caseRepository.add(currentCase);
    }

    protected void setSuspects(Case currentCase, Set<Suspect> intersection, boolean empty, Iterator<Suspect> iterator, Set<Suspect> witnessSuspects, Set<Suspect> userSuspects) {
        userSuspects = intersection;
        if (!userSuspects.isEmpty()) {
            currentCase.setSuspects(new ArrayList<>(Collections.singletonList(userSuspects.iterator().next())));
        } else if (!empty) {
            currentCase.setSuspects(new ArrayList<>(Collections.singletonList(iterator.next())));
        } else {
            currentCase.setSuspects(null);
        }
    }

    public List<Case> findActiveCases() throws IOException {
        List<Case> activeCases = new ArrayList<>();
        for (Case c : caseRepository.loadAll()) {
            if (c.isActive()) {
                activeCases.add(c);
            }
        }
        return activeCases;
    }
}