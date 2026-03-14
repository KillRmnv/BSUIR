package com.bsuir;

import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

public class Pipeline {

    private Queue<Pair> queue;
    private List<Stage> stages;
    private List<Pair> results;

    public List<Pair> getResults() {
        return results;
    }

    public void setResults(List<Pair> results) {
        this.results = results;
    }

    public Queue<Pair> getQueue() {
        return queue;
    }

    public void setQueue(Queue<Pair> queue) {
        this.queue = queue;
    }

    public List<Stage> getStages() {
        return stages;
    }

    public void setStages(List<Stage> stages) {
        this.stages = stages;
    }

    public Pipeline(List<Stage> stages) {
        this.stages = stages;
        this.queue = new ConcurrentLinkedQueue<>();
        this.results = new ArrayList<>();
    }

    public Pipeline(int size) {
        stages = new ArrayList<Stage>(size);
        this.queue = new ConcurrentLinkedQueue<>();
        for (int i = 0; i < size - 1; i++) {
            Stage firstStage = new Stage();
            stages.add(firstStage);
        }
        Stage lastStage = new Stage(true);
        stages.add(lastStage);
        this.results = new ArrayList<>();
    }

    public void execute() throws InterruptedException {
        for (int i = stages.size() - 1; i > 0; i--) {
            Stage prevStage = stages.get(i - 1);
            Stage currStage = stages.get(i);

            if (!prevStage.isComplete()) {
                currStage.setPairs(prevStage.getPairs());
                if (currStage.isLast()) {
                    results.addAll(prevStage.getPairs());
                }
                prevStage.eject();
            } else if (currStage.isLast() && queue.isEmpty()&& !currStage.isComplete()) {
                currStage.eject();
            }
        }

        Stage firstStage = stages.get(0);
        if (firstStage.isComplete() && !queue.isEmpty()) {
            List<Pair> batch = new ArrayList<>();

            for (int i = 0; i < Config.parallelism && !queue.isEmpty(); i++) {
                batch.add(queue.poll());
            }
            firstStage.setPairs(batch);
        }

        for (Stage stage : stages) {
            stage.execute();
        }
    }

    public boolean hasActiveStages() {
        for (Stage stage : stages) {
            if (!stage.isComplete()) {
                return true;
            }
        }
        return false;
    }
}
