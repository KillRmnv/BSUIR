package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Delivery;
import pbz.Romanov.entities.search.DeliverySearch;
import pbz.Romanov.services.DeliveryService;
import pbz.Romanov.services.ReferenceDataService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Delivery")
public class DeliveryCRUDController {

    @Inject
    private final DeliveryService deliveryService;
    @Inject
    private  final ReferenceDataService referenceDataService;
    public DeliveryCRUDController(DeliveryService deliveryService, ReferenceDataService referenceDataService) {
        this.deliveryService = deliveryService;
        this.referenceDataService = referenceDataService;
    }

    @Get("/")
    @View("DeliverysCRUD")
    public Map<String, Object> deliverysCRUDMenu() throws Exception {
        Map<String, Object> model = new HashMap<>();
        model.put("references",referenceDataService.getReferenceTable("DeliveryType"));
        return model;
    }

    @Post("/search/{page}")
    public List<Delivery> getDeliveriesNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @Body DeliverySearch filter
    ) throws Exception {

        List<Delivery> allDeliveries = deliveryService.getDeliveries(filter);

        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, allDeliveries.size());
        if (fromIndex >= allDeliveries.size()) return List.of();
        return allDeliveries.subList(fromIndex, toIndex);
    }
    @Post("/create")
    public void createDelivery(@Body Delivery delivery) throws Exception {
        deliveryService.insertDelivery(delivery);
    }
    @Put("/update")
    public void updateDelivery(@Body DeliverySearch delivery) throws Exception {
        if (delivery.getAddress() == null || delivery.getAddress().isEmpty()) {
            delivery.setAddress(null);
        }
        if (delivery.getExpectedDate() == null || delivery.getExpectedDate().isEmpty()) {
            delivery.setExpectedDate(null);
        }

        // ID
        if (delivery.getId() != null && delivery.getId() < 1) {
            delivery.setId(null);
        }

        // Type
        if (delivery.getType() != null && delivery.getType() < 1) {
            delivery.setType(null);
        }

        // State (соответствует полю histId в классе Delivery)
        if (delivery.getHistId() != null && delivery.getHistId() < 1) {
            delivery.setState(null);
        }

        if (delivery.getId() == null) {
            throw new Exception("ID is required for update operation");
        }

        deliveryService.updateDelivery(delivery);
    }

    @Post("/delete")
    public void deleteDelivery(@Body DeliverySearch filter) throws Exception {
        deliveryService.deleteDelivery(filter);
    }
}
