package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Employee;
import pbz.Romanov.entities.HistoryRecord;
import pbz.Romanov.services.HistoryService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/History")
public class HistoryCRUDController {
    @Inject
    private final HistoryService historyService;

    public HistoryCRUDController(HistoryService historyService) {
        this.historyService = historyService;
    }

    @Get("/")
    @View("HistoryCRUD")
    public Map<String, Object> historyMenu() {
        return new HashMap<>();
    }

    @Get("/{page}")
    public List<HistoryRecord> getHistoryNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @QueryValue(value = "date", defaultValue = "") String date,
            @QueryValue(value = "printing", defaultValue = "-1") int printing,
            @QueryValue(value = "employeeId", defaultValue = "-1") int employeeId,
            @QueryValue(value = "numOfPublication", defaultValue = "-1") int numOfPublication,
            @QueryValue(value = "received", defaultValue = "-1") int received,
            @QueryValue(value = "writeOut", defaultValue = "-1") int writeOut
    ) throws Exception {

        HistoryRecord filter = new HistoryRecord();
        if (!date.equals(""))
            filter.setDate(date);
        filter.setPrinting(printing);
        filter.setEmployee(new Employee(employeeId));
        filter.setNumOfPublication(numOfPublication);
        filter.setReceived(received);
        filter.setWriteOut(writeOut);

        List<HistoryRecord> allRecords = historyService.getHistoryRecords(filter);

        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, allRecords.size());
        if (fromIndex >= allRecords.size()) return List.of();
        return allRecords.subList(fromIndex, toIndex);
    }

    @Get("/create")
    public void createHistory(@QueryValue(value = "date", defaultValue = "") String date,
            @QueryValue(value = "printing", defaultValue = "-1") int printing,
            @QueryValue(value = "employeeId", defaultValue = "-1") int employeeId,
            @QueryValue(value = "numOfPublication", defaultValue = "-1") int numOfPublication,
            @QueryValue(value = "received", defaultValue = "-1") int received,
            @QueryValue(value = "writeOut", defaultValue = "-1") int writeOut) throws Exception {
        HistoryRecord filter = new HistoryRecord();
        if (!date.equals(""))
            filter.setDate(date);
        filter.setPrinting(printing);
        filter.setEmployee(new Employee(employeeId));
        filter.setNumOfPublication(numOfPublication);
        filter.setReceived(received);
        filter.setWriteOut(writeOut);
        historyService.insertHistoryRecord(filter);
    }

    @Get("/update")
    public void updateHistory(@QueryValue(value = "date", defaultValue = "") String date,
            @QueryValue(value = "printing", defaultValue = "-1") int printing,
            @QueryValue(value = "employeeId", defaultValue = "-1") int employeeId,
            @QueryValue(value = "numOfPublication", defaultValue = "-1") int numOfPublication,
            @QueryValue(value = "received", defaultValue = "-1") int received,
            @QueryValue(value = "writeOut", defaultValue = "-1") int writeOut) throws Exception {
        HistoryRecord filter = new HistoryRecord();
        if (!date.equals(""))
            filter.setDate(date);
        filter.setPrinting(printing);
        filter.setEmployee(new Employee(employeeId));
        filter.setNumOfPublication(numOfPublication);
        filter.setReceived(received);
        filter.setWriteOut(writeOut);
        historyService.updateHistoryRecord(filter);
    }

    @Get("/delete")
    public void deleteHistory(@QueryValue(value = "date", defaultValue = "") String date,
            @QueryValue(value = "printing", defaultValue = "-1") int printing,
            @QueryValue(value = "employeeId", defaultValue = "-1") int employeeId,
            @QueryValue(value = "numOfPublication", defaultValue = "-1") int numOfPublication,
            @QueryValue(value = "received", defaultValue = "-1") int received,
            @QueryValue(value = "writeOut", defaultValue = "-1") int writeOut) throws Exception {
        HistoryRecord filter = new HistoryRecord();
        if (!date.equals(""))
            filter.setDate(date);
        filter.setPrinting(printing);
        filter.setEmployee(new Employee(employeeId));
        filter.setNumOfPublication(numOfPublication);
        filter.setReceived(received);
        filter.setWriteOut(writeOut);
        historyService.deleteHistoryRecord(filter);
    }
}
