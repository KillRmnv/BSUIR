package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Printing;
import pbz.Romanov.entities.search.PrintingSearch;
import pbz.Romanov.services.PrintingService;
import pbz.Romanov.services.ReferenceDataService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Printing")
public class PrintingCRUDController {

    @Inject
    private final PrintingService printingService;
    @Inject
    private  final ReferenceDataService referenceDataService;
    public PrintingCRUDController(PrintingService printingService, ReferenceDataService referenceDataService) {
        this.printingService = printingService;
        this.referenceDataService = referenceDataService;
    }

    @Get("/")
    @View("PrintingCRUD")
    public Map<String, Object> printingCRUDMenu() throws Exception {
        Map<String, Object> model = new HashMap<>();
        model.put("references1",referenceDataService.getReferenceTable("Frequencies"));
        model.put("references2",referenceDataService.getReferenceTable("PublicationTypes"));
        return model;
    }

    @Post("/search/{page}")
    public List<Printing> getPrintingsNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @Body PrintingSearch filter
    ) throws Exception {
        List<Printing> fullList = printingService.getPrintings(filter);
        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, fullList.size());
        if (fromIndex >= fullList.size()) return List.of();
        return fullList.subList(fromIndex, toIndex);
    }

    @Post("/create")
    public void createPrinting(@Body Printing printing) throws Exception {
        printingService.insertPrinting(printing);
    }

    @Put("/update")
    public void updatePrinting(@Body PrintingSearch printing) throws Exception {


        if (printing.getName() != null && printing.getName().isEmpty()) {
            printing.setName(null);
        }


        // Type
        if (printing.getType() != null && printing.getType() < 1) {
            printing.setType(null);
        }

        // Index
        if (printing.getIndex() != null && printing.getIndex() < 1) {
            throw new IllegalArgumentException("Index must be greater than 0");
        }

        // Period
        if (printing.getPeriod() != null && printing.getPeriod() < 1) {
            printing.setPeriod(null); // Устанавливаем null
        }

        printingService.updatePrinting(printing);
    }

    @Post("/delete")
    public void deletePrinting(@Body PrintingSearch filter) throws Exception {
        printingService.deletePrinting(filter);
    }
}
