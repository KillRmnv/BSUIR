package ppois.Romanov;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import lombok.Setter;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;

public class SearchController implements Initializable,Controller {
    @FXML
    private ChoiceBox pageAmountChoice;
    @FXML
    private Button prevPageButton;
    @FXML
    private Button nextPageButton;
    @FXML
    private Label pageLabel;
    @FXML
    private TextField accountNumberField;
    @Setter
    private CustomerProcessingSystem customerProcessingSystem;
    @FXML
    private TextField nameField;
    @FXML
    private TextField addressField;
    @FXML
    private TextField mobilePhoneField;
    @FXML
    private TextField townPhoneField;
    @FXML
    private Button searchButton;
    @FXML
    private TableView<Customer> tableView;
    @FXML
    private TableColumn<Customer, Integer> accountNumberColumn;
    @FXML
    private TableColumn<Customer, String> fioColumn;
    @FXML
    private TableColumn<Customer, String> addressColumn;
    @FXML
    private TableColumn<Customer, String> phonesColumn;
    @FXML
    private TableColumn<Customer, String> mobilePhoneColumn;
    @FXML
    private TableColumn<Customer, String> townPhoneColumn;
    private List<Customer> searchResults;
    private int pageNumber = 0;

    public void searchCustomer() throws Exception {
        tableView.setItems(FXCollections.observableArrayList());
        CustomerSearchCriteria templateCustomer = getCustomerSearchCriteria();

        searchResults = customerProcessingSystem.loadCustomers(templateCustomer);

       updateTableView();
    }
    private void updateTableView() {
        if (searchResults.isEmpty()) {
            return;
        }

        if (searchResults.size() <  (Integer)pageAmountChoice.getValue()) {
            tableView.setItems(FXCollections.observableArrayList(searchResults.subList(0, searchResults.size())));
            ViewObjectsBuilder.hideButton(nextPageButton);
        } else {
            tableView.setItems(FXCollections.observableArrayList(searchResults.subList(0,
                    (Integer)pageAmountChoice.getValue())));
            ViewObjectsBuilder.showButton(nextPageButton);
        }

        pageNumber = 0;
        ViewObjectsBuilder.hideButton(prevPageButton);
        pageLabel.setText("Page:" + pageNumber);
    }
    private CustomerSearchCriteria getCustomerSearchCriteria() {
        CustomerSearchCriteria templateCustomer = new CustomerSearchCriteria();
        templateCustomer.setName(nameField.getText());
        templateCustomer.setAddress(addressField.getText());
        templateCustomer.setMobilePhone(mobilePhoneField.getText());
        templateCustomer.setTownPhone(townPhoneField.getText());

        if (!accountNumberField.getText().isEmpty()) {
            templateCustomer.setAccountNumber(accountNumberField.getText());
        } else {
            templateCustomer.setAccountNumber("");
        }
        return templateCustomer;
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        ViewObjectsBuilder.createColumns(fioColumn, accountNumberColumn, addressColumn, mobilePhoneColumn, townPhoneColumn);
        searchResults = new ArrayList<>();
        ObservableList<Integer> pages = FXCollections.observableArrayList(10,15,20);
        pageAmountChoice.setItems(pages);
        pageAmountChoice.setValue(15);
        ViewObjectsBuilder.hideButton(prevPageButton);
        ViewObjectsBuilder.hideButton(nextPageButton);
        pageLabel.setText("Page:" + pageNumber);

    }

    public void prevPage() {
        pageNumber--;
        pageLabel.setText("Page:" + pageNumber);
        tableView.setItems(FXCollections.observableArrayList(searchResults.subList(pageNumber
                * (Integer)pageAmountChoice.getValue(), (pageNumber + 1)
                *  (Integer)pageAmountChoice.getValue())));
        if (pageNumber == 0) {
            ViewObjectsBuilder.hideButton(prevPageButton);
        }
        ViewObjectsBuilder.showButton(nextPageButton);
    }

    public void nextPage() {
        pageNumber++;
        List<Customer> toShow;
        if((pageNumber + 1) *  (Integer)pageAmountChoice.getValue()<searchResults.size()) {
            toShow = searchResults.subList(pageNumber *  (Integer)pageAmountChoice.getValue(),
                    (pageNumber + 1) *  (Integer)pageAmountChoice.getValue());
        }else{
            toShow = searchResults.subList(pageNumber *  (Integer)pageAmountChoice.getValue(),
                    searchResults.size());
        }
        ViewObjectsBuilder.nextPage(pageNumber, pageLabel, nextPageButton, prevPageButton, tableView, toShow);
    }

    public void changeAmntOfCustomersOnPage() {
       updateTableView();
    }
}