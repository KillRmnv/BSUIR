package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Subscription;
import pbz.Romanov.entities.search.SubscriptionSearch;
import pbz.Romanov.services.ReferenceDataService;
import pbz.Romanov.services.SubscriptionService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Subscription")
public class SubscriptionCRUDController {

    @Inject
    private final SubscriptionService subscriptionService;

    public SubscriptionCRUDController(SubscriptionService subscriptionService, ReferenceDataService referenceDataService) {
        this.subscriptionService = subscriptionService;
        this.referenceDataService = referenceDataService;
    }
    @Inject
    private final ReferenceDataService referenceDataService;
    @Get("/")
    @View("SubscriptionCRUD")
    public Map<String, Object> subscriptionMenu() throws Exception {
        Map<String, Object> model = new HashMap<>();
        model.put("reference",referenceDataService.getReferenceTable("SubsPeriods"));
        return model;
    }

    @Post("/search/{page}")
    public List<Subscription> getSubscriptionsNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @Body SubscriptionSearch filter
    ) throws Exception {
        if(filter.getStartingDate()!=null &&filter.getStartingDate().isEmpty())
            filter.setStartingDate(null);
        if(filter.getEndingDate()!=null && filter.getEndingDate().isEmpty())
            filter.setEndingDate(null);
        filter.setId(-1);
        List<Subscription> allSubscriptions = subscriptionService.getSubscriptions(filter);
        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, allSubscriptions.size());
        if (fromIndex >= allSubscriptions.size()) return List.of();
        return allSubscriptions.subList(fromIndex, toIndex);
    }

    @Post("/create")
    public void createSubscription(@Body Subscription subscription) throws Exception {
        subscriptionService.insertSubscription(subscription);
    }

    @Put("/update")
    public void updateSubscription(@Body SubscriptionSearch subscription) throws Exception {
        // 1. Обработка строковых полей (остаётся как было)
        if(subscription.getStartingDate() == null || subscription.getStartingDate().isEmpty())
            subscription.setStartingDate(null);
        if(subscription.getEndingDate() == null || subscription.getEndingDate().isEmpty())
            subscription.setEndingDate(null);

        // 2. Обработка Integer полей: установить null, если < 1
        // Используем геттеры и сеттеры, как и требуется

        // Id
        if (subscription.getId() != null && subscription.getId() < 1) {
            subscription.setId(null); // Устанавливаем null
        }

        // Period
        if (subscription.getPeriod() != null && subscription.getPeriod() < 1) {
            subscription.setPeriod(null); // Устанавливаем null
        }

        // EmployeeId
        if (subscription.getEmployeeId() != null && subscription.getEmployeeId() < 1) {
            subscription.setEmployeeId(null); // Устанавливаем null
        }

        // Cost
        if (subscription.getCost() != null && subscription.getCost() < 1) {
            subscription.setCost(null); // Устанавливаем null
        }

        // После обработки, если Id всё ещё null, можно бросить исключение,
        // если Id является обязательным полем для обновления.
        // Если Id < 1, он уже был обнулен, поэтому проверка меняется:
        if (subscription.getId() == null) {
            throw new Exception("Id is required for update operation");
        }

        subscriptionService.updateSubscription(subscription);
    }

    @Post("/delete")
    public void deleteSubscription(@Body SubscriptionSearch filter) throws Exception {
        if(filter.getStartingDate().isEmpty())
            filter.setStartingDate(null);
        if(filter.getEndingDate().isEmpty())
            filter.setEndingDate(null);
        subscriptionService.deleteSubscription(filter);
    }
}
