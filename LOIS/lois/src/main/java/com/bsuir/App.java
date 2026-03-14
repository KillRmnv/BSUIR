package com.bsuir;


public class App {
    public static void main(String[] args) throws InterruptedException {
        ConsoleIO consoleIO = new ConsoleIO();
        consoleIO.inputPipelineParams();
        Pipeline pipeline = new Pipeline(Config.amountOfBits);
        PipelineManager pipelineManager = new PipelineManager(pipeline);
        pipelineManager.init();
        pipelineManager.start();
    }
}