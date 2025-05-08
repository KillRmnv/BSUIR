package by.romanov.ppois.webapp;

import by.romanov.ppois.Input;
import by.romanov.ppois.UserInterface;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.annotation.QueryValue;
import io.micronaut.views.View;

import java.util.List;
import java.util.Map;


@Controller
public class StateMachineController implements UserInterface {

    private Input input;
    private String currentPage;
    private List<String> messages;

    public StateMachineController() {
        this.input = new WebInput();
        currentPage = "police/initial";
    }

    @Get("/{currentPage}")
    @View("{currentPage}")
    @Override
    public void showPage(@PathVariable String currentPage) {
        this.currentPage = currentPage;
    }

    @Override
    public String getPage() {
        return currentPage;
    }

    @Get("/{currentPage}")
    @View("{currentPage}")
    public void handle(@PathVariable String currentPage,
                       @QueryValue Map<String, String> params) {
        this.currentPage = currentPage;
        input.setPage(currentPage);
        ((WebInput) input).setParams(params);
    }

    @Override
    public Input getInput() {
        return input;
    }

    @Override
    public void setInput(Input input) throws IllegalArgumentException {
        if (input instanceof WebInput)
            this.input = input;
        else
            throw new IllegalArgumentException("Input must be an instance of WebInput");
    }

    @Override
    public void show(List<String> list) {
        messages.addAll(list);
    }

    @Override
    public void showNum(int i) {
        messages.add(i + ".");
    }

    @Override
    public void showNumericRange(String prompt, int min, int max) {
        messages.add(prompt + ": " + min + "-" + max);
    }

    @Override
    public void show(String s) {
        messages.add(s);
    }

    @Get("/messages/json")
    public Map<String, Object> getMessages() {
        return Map.of("messages", this.messages);
    }
}