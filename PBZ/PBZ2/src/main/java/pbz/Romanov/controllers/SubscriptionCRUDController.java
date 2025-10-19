package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Delivery;
import pbz.Romanov.entities.Printing;
import pbz.Romanov.entities.Subscription;
import pbz.Romanov.services.SubscriptionService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Subscription")
public class SubscriptionCRUDController {
    @Inject
    private final SubscriptionService subscriptionService;


    public SubscriptionCRUDController(SubscriptionService subscriptionService) {
        this.subscriptionService = subscriptionService;
    }

    @Get("/")
    @View("SubscriptionCRUD")
    public Map<String, Object> subscriptionMenu() {
        return new HashMap<>();
    }

    @Get("/{page}")
    public List<Subscription> getSubscriptionsNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @QueryValue(value = "startingDate", defaultValue = "") String startingDate,
            @QueryValue(value = "endingDate", defaultValue = "") String endingDate,
            @QueryValue(value = "amountOfMonths", defaultValue = "-1") int amountOfMonths,
            @QueryValue(value = "deliveryId", defaultValue = "-1") int deliveryId,
            @QueryValue(value = "printingIndex", defaultValue = "-1") int printingIndex,
            @QueryValue(value = "employeeId", defaultValue = "-1") int employeeId,
            @QueryValue(value = "cost", defaultValue = "-1") int cost
    ) throws Exception {

        Subscription filter = new Subscription();
        if (!startingDate.equals(""))
            filter.setStartingDate(startingDate);
        if (!endingDate.equals(""))
            filter.setEndingDate(endingDate);
        filter.setAmountOfMonths(amountOfMonths);
        filter.setDelivery(new Delivery(deliveryId));
        Printing printing = new Printing();
        if (printingIndex != -1) {
            printing.setIndex(printingIndex);
        }
        filter.setPrinting(printing);
        filter.setEmployeeId(employeeId);
        filter.setCost(cost);

        List<Subscription> allSubscriptions = subscriptionService.getSubscriptions(filter);

        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, allSubscriptions.size());
        if (fromIndex >= allSubscriptions.size()) return List.of();
        return allSubscriptions.subList(fromIndex, toIndex);
    }


    @Get("/create")
    public void createSubscription(@QueryValue(value = "startingDate", defaultValue = "") String startingDate,
            @QueryValue(value = "endingDate", defaultValue = "") String endingDate,
            @QueryValue(value = "amountOfMonths", defaultValue = "-1") int amountOfMonths,
            @QueryValue(value = "deliveryId", defaultValue = "-1") int deliveryId,
            @QueryValue(value = "printingIndex", defaultValue = "-1") int printingIndex,
            @QueryValue(value = "employeeId", defaultValue = "-1") int employeeId,
            @QueryValue(value = "cost", defaultValue = "-1") int cost) throws Exception {
        Subscription filter = new Subscription();
        if (!startingDate.equals(""))
            filter.setStartingDate(startingDate);
        if (!endingDate.equals(""))
            filter.setEndingDate(endingDate);
        filter.setAmountOfMonths(amountOfMonths);
        filter.setDelivery(new Delivery(deliveryId));
        Printing printing = new Printing();
        if (printingIndex != -1) {
            printing.setIndex(printingIndex);
        }
        filter.setPrinting(printing);
        filter.setEmployeeId(employeeId);
        filter.setCost(cost);
        subscriptionService.insertSubscription(filter);
    }

    @Get("/update")
    public void updateSubscription(@QueryValue(value = "startingDate", defaultValue = "") String startingDate,
            @QueryValue(value = "endingDate", defaultValue = "") String endingDate,
            @QueryValue(value = "amountOfMonths", defaultValue = "-1") int amountOfMonths,
            @QueryValue(value = "deliveryId", defaultValue = "-1") int deliveryId,
            @QueryValue(value = "printingIndex", defaultValue = "-1") int printingIndex,
            @QueryValue(value = "employeeId", defaultValue = "-1") int employeeId,
            @QueryValue(value = "cost", defaultValue = "-1") int cost) throws Exception {
        Subscription filter = new Subscription();
        if (!startingDate.equals(""))
            filter.setStartingDate(startingDate);
        if (!endingDate.equals(""))
            filter.setEndingDate(endingDate);
        filter.setAmountOfMonths(amountOfMonths);
        filter.setDelivery(new Delivery(deliveryId));
        Printing printing = new Printing();
        if (printingIndex != -1) {
            printing.setIndex(printingIndex);
        }
        filter.setPrinting(printing);
        filter.setEmployeeId(employeeId);
        filter.setCost(cost);
        subscriptionService.updateSubscription(filter);
    }

    @Get("/delete")
    public void deleteSubscription(@QueryValue(value = "startingDate", defaultValue = "") String startingDate,
            @QueryValue(value = "endingDate", defaultValue = "") String endingDate,
            @QueryValue(value = "amountOfMonths", defaultValue = "-1") int amountOfMonths,
            @QueryValue(value = "deliveryId", defaultValue = "-1") int deliveryId,
            @QueryValue(value = "printingIndex", defaultValue = "-1") int printingIndex,
            @QueryValue(value = "employeeId", defaultValue = "-1") int employeeId,
            @QueryValue(value = "cost", defaultValue = "-1") int cost) throws Exception {
        Subscription filter = new Subscription();
        if (!startingDate.equals(""))
            filter.setStartingDate(startingDate);
        if (!endingDate.equals(""))
            filter.setEndingDate(endingDate);
        filter.setAmountOfMonths(amountOfMonths);
        filter.setDelivery(new Delivery(deliveryId));
        Printing printing = new Printing();
        if (printingIndex != -1) {
            printing.setIndex(printingIndex);
        }
        filter.setPrinting(printing);
        filter.setEmployeeId(employeeId);
        filter.setCost(cost);
        subscriptionService.deleteSubscription(filter);
    }
}
