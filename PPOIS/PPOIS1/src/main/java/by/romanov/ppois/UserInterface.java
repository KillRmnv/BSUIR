package by.romanov.ppois;

import java.util.List;

public interface UserInterface {
       void showPage(String currentPage);
       String getPage();
       void setPage(String page);
       Input getInput();
       void setInput(Input input);
       void show(List<String> messages);
       void showNum(int num);
       void showNumericRange(String prompt, int min, int max);
       void show(String message);
}
