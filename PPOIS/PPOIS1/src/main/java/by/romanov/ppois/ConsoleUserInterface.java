package by.romanov.ppois;

import com.fasterxml.jackson.annotation.JsonIgnore;

import java.util.List;

public class ConsoleUserInterface implements UserInterface {
    @JsonIgnore
    Input input;
    public ConsoleUserInterface() {}
    public ConsoleUserInterface(Input input) {
        this.input=input;
    }
    @Override
    public void showPage(String currentPage) {
    }

    @Override
    public String getPage() {
        return "";
    }

    @Override
    public void setPage(String page) {

    }

    @Override
    public Input getInput() {
        return input;
    }

    @Override
    public void setInput(Input input) {
        this.input = input;
    }
    @Override
    public void show(String message) {
        System.out.println(message);
    }
    @Override
    public void showNumericRange(String prompt, int min, int max) {
        System.out.println(prompt);
        System.out.print(min + "-" + max);
        System.out.println();
    }

    @Override
    public void show(List<String> messages) {
        for (int index = 0; index < messages.size(); index++) {
            System.out.println(messages.get(index));
        }
    }
    @Override
    public void showNum(int num){
        System.out.print(num+".");
    }
}
