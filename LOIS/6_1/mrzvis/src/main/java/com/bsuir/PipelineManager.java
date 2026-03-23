/*
Лабораторная работа №1
Выполнил студент группы 321701
Романов К.В.
Вариант 6
Улучшенный PipelineManager с отслеживанием завершенных пар
*/

package com.bsuir;

import java.util.ArrayList;
import java.util.List;

public class PipelineManager {

    private Pipeline pipeline;
    private ConsoleIO io = new ConsoleIO();
    private List<Pair> completedPairs = new ArrayList<>();

    public void init() {
        System.out.println("\nГенерация " + Config.amountOfPairs + " пар...");
        for (int i = 0; i < Config.amountOfPairs; i++) {
            System.out.print("  Пара " + i + ": ");
            Pair pair = io.generateRandomPair();
            pair.setPairNumber(i);
            pipeline.getQueue().add(pair);
        }
    }

    public Pipeline getPipeline() {
        return pipeline;
    }

    public PipelineManager(Pipeline pipeline) {
        this.pipeline = pipeline;
    }

    public void addPair(Pair pair) {
        pipeline.getQueue().add(pair);
    }

    public void setPipeline(Pipeline pipeline) {
        this.pipeline = pipeline;
    }

    public void start() throws InterruptedException {
        int tactCounter = 0;
        io.displayState(tactCounter, pipeline.getStages(), completedPairs);
        
        tactCounter = 1;

        while (!pipeline.getQueue().isEmpty() || pipeline.hasActiveStages()) {
            if (tactCounter % Config.tactTime == 0) {
                int previousResultsSize = completedPairs.size();
                pipeline.execute();
                
                List<Pair> newResults = pipeline.getResults();
                for (int i = previousResultsSize; i < newResults.size(); i++) {
                    Pair completedPair = newResults.get(i);
                    completedPair.setCompletionTact(tactCounter + 1);
                    if (!completedPairs.contains(completedPair)) {
                        completedPairs.add(completedPair);
                    }
                }
            }

            io.displayState(tactCounter, pipeline.getStages(), completedPairs);
            tactCounter++;
        }
        
        io.displayFinalResults(pipeline.getResults());
    }
}