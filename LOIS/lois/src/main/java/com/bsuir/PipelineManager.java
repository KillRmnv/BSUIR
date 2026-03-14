package com.bsuir;

public class PipelineManager {

    private Pipeline pipeline;
    private ConsoleIO io = new ConsoleIO();
    public void init() {
    
        
        System.out.println("\nГенерация " + Config.amountOfPairs + " пар...");
        for (int i = 0; i < Config.amountOfPairs; i++) {
            Pair pair = io.generateRandomPair();
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
         io.displayState(0, pipeline.getStages());
        int tactCounter = 1;

        while (!pipeline.getQueue().isEmpty() || pipeline.hasActiveStages()) {
            if (tactCounter % Config.tactTime == 0) {
                pipeline.execute();
            } 
            
            io.displayState(tactCounter, pipeline.getStages());
            tactCounter++;
        }
        io.displayResults(pipeline.getResults());
    }
}
