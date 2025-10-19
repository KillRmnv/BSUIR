package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Delivery;
import pbz.Romanov.services.DeliveryService;


import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Delivery")
public class DeliveryCRUDController {
    @Inject
    private final DeliveryService deliveryService;


    public DeliveryCRUDController(DeliveryService deliveryService) {
        this.deliveryService = deliveryService;
    }


    @Get("/")
    @View("DeliverysCRUD")
    public Map<String, Object> deliverysCRUDMenu() {
        return new HashMap<>();
    }

    @Get("/{page}")
    public List<Delivery> getDeliveriesNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @QueryValue(value = "id", defaultValue = "-1") int id,
            @QueryValue(value = "type", defaultValue = "") String type,
            @QueryValue(value = "date", defaultValue = "") String date
    ) throws Exception {

        Delivery filter = new Delivery();
        if (id != -1) filter.setId(id);
        filter.setType(type);
        if (!date.equals("")) filter.setDate(date);

        List<Delivery> allDeliveries = deliveryService.getDeliveries(filter);

        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, allDeliveries.size());
        if (fromIndex >= allDeliveries.size()) return List.of();
        return allDeliveries.subList(fromIndex, toIndex);
    }


    @Get("/create")
    public void createDelivery(
    @QueryValue(value = "type", defaultValue = "") String type,
    @QueryValue(value = "date", defaultValue = "") String date) throws Exception {
        Delivery filter = new Delivery();

        filter.setType(type);
        if (!date.equals("")) filter.setDate(date);
        deliveryService.insertDelivery(filter);
    }

    @Get("/update")
    public void updateDelivery( @QueryValue(value = "id", defaultValue = "-1") int id,
                                @QueryValue(value = "type", defaultValue = "") String type,
                                @QueryValue(value = "date", defaultValue = "") String date) throws Exception {
        Delivery filter = new Delivery();
        if (id != -1) filter.setId(id);
        filter.setType(type);
        if (!date.equals("")) filter.setDate(date);
        deliveryService.updateDelivery(filter);
    }

    @Get("/delete")
    public void deleteDelivery(@QueryValue(value = "id", defaultValue = "-1") int id,
                               @QueryValue(value = "type", defaultValue = "") String type,
                               @QueryValue(value = "date", defaultValue = "") String date) throws Exception {
        Delivery filter = new Delivery();
        if (id != -1) filter.setId(id);
        filter.setType(type);
        if (!date.equals("")) filter.setDate(date);
        deliveryService.deleteDelivery(filter);
    }
}
