package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Circulation;
import pbz.Romanov.entities.search.CirculationSearch;
import pbz.Romanov.services.CirculationService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Circulation")
public class CirculationCRUDController {

    @Inject
    private final CirculationService circulationService;

    public CirculationCRUDController(CirculationService circulationService) {
        this.circulationService = circulationService;
    }

    @Get("/")
    @View("CirculationCRUD")
    public Map<String, Object> circulationCRUDMenu() {
        return new HashMap<>();
    }

    @Post("/search/{page}")
    public List<Circulation> getCirculationsNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @Body CirculationSearch filter
    ) throws Exception {
        List<Circulation> fullList = circulationService.getCirculations(filter);
        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, fullList.size());
        if (fromIndex >= fullList.size()) return List.of();
        return fullList.subList(fromIndex, toIndex);
    }

    @Post("/create")
    public void createCirculation(@Body Circulation circulation) throws Exception {
        circulationService.insertCirculation(circulation);
    }

    @Put("/update")
    public void updateCirculation(@Body CirculationSearch circulation) throws Exception {
        if (circulation.getAmount() != null && circulation.getAmount() < 1) {
            circulation.setAmount(null);
        }

        if (circulation.getAllocatedAmount() != null && circulation.getAllocatedAmount() < 1) {
            circulation.setAllocatedAmount(null);
        }

        if (circulation.getNumOfPub() != null && circulation.getNumOfPub() < 1) {
            circulation.setNumOfPub(null);
        }

        circulationService.updateCirculation(circulation);
    }

    @Post("/delete")
    public void deleteCirculation(@Body CirculationSearch filter) throws Exception {
        circulationService.deleteCirculation(filter);
    }
}
