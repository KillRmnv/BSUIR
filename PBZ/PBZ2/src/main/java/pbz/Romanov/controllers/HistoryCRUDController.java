package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.HistoryRecord;
import pbz.Romanov.entities.search.HistoryRecordSearch;
import pbz.Romanov.services.HistoryService;
import pbz.Romanov.services.ReferenceDataService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/History")
public class HistoryCRUDController {

    @Inject
    private final HistoryService historyService;
    @Inject
    private final ReferenceDataService referenceDataService;
    public HistoryCRUDController(HistoryService historyService, ReferenceDataService referenceDataService) {
        this.historyService = historyService;
        this.referenceDataService = referenceDataService;
    }

    @Get("/")
    @View("HistoryCRUD")
    public Map<String, Object> historyMenu() throws Exception {
        Map<String, Object> model = new HashMap<>();
        model.put("reference",referenceDataService.getReferenceTable("HistoryStates"));
        return model;
    }

    @Post("/search/{page}")
    public List<HistoryRecord> getHistoryNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @Body HistoryRecordSearch filter
    ) throws Exception {
        List<HistoryRecord> allRecords = historyService.getHistoryRecords(filter);
        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, allRecords.size());
        if (fromIndex >= allRecords.size()) return List.of();
        return allRecords.subList(fromIndex, toIndex);
    }

    @Post("/create")
    public void createHistory(@Body HistoryRecord historyRecord) throws Exception {
        historyService.insertHistoryRecord(historyRecord);
    }

    @Put("/update")
    public void updateHistory(@Body HistoryRecordSearch historyRecord) throws Exception {

        if (historyRecord.getDate() == null || historyRecord.getDate().isEmpty()) {
            historyRecord.setDate(null);
        }

        if (historyRecord.getId() != null && historyRecord.getId() < 1) {
            historyRecord.setId(null);
        }

        if (historyRecord.getNumOfPublication() != null && historyRecord.getNumOfPublication() < 1) {
            historyRecord.setNumOfPublication(null);
        }

        if (historyRecord.getState() != null && historyRecord.getState() < 1) {
            historyRecord.setState(null);
        }

        if (historyRecord.getSub() != null && historyRecord.getSub() < 1) {
            historyRecord.setSub(null);
        }

        if (historyRecord.getId() == null) {
            throw new Exception("Id is required for update operation");
        }

        historyService.updateHistoryRecord(historyRecord);
    }

    @Post("/delete")
    public void deleteHistory(@Body HistoryRecordSearch filter) throws Exception {
        historyService.deleteHistoryRecord(filter);
    }
}
