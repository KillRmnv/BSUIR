package ppois.romanov.controllers;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import lombok.Setter;
import ppois.romanov.entities.Customer;
import ppois.romanov.CustomerProcessingSystem;
import ppois.romanov.CustomerSearchCriteria;
import ppois.romanov.ViewObjectsBuilder;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;

public class SearchController implements Initializable, Controller {
    @FXML
    private  Label pageNumberLabel;
    @FXML
    private  Button lastPageButton;
    @FXML
    private  Button firstPageButton;
    @FXML
    private ChoiceBox pageAmountChoice;
    @FXML
    private Button prevPageButton;
    @FXML
    private Button nextPageButton;

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
        ViewObjectsBuilder.showButton(lastPageButton);
        if (searchResults.size() <  (Integer)pageAmountChoice.getValue()) {
            tableView.setItems(FXCollections.observableArrayList(searchResults.subList(0, searchResults.size())));
            ViewObjectsBuilder.hideButton(nextPageButton);
            ViewObjectsBuilder.hideButton(lastPageButton);
        } else {
            tableView.setItems(FXCollections.observableArrayList(searchResults.subList(0,
                    (Integer)pageAmountChoice.getValue())));
            ViewObjectsBuilder.showButton(nextPageButton);
        }

        pageNumber = 0;
        pageNumberLabel.setText("Стр:"+String.valueOf(pageNumber));
        ViewObjectsBuilder.hideButton(prevPageButton);
        pageNumberLabel.setText("Стр:" + pageNumber);
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
        ViewObjectsBuilder.hideButton(lastPageButton);
        ViewObjectsBuilder.hideButton(firstPageButton);


        pageNumberLabel.setText("Стр:" + pageNumber);

    }

    public void prevPage() {
        pageNumber--;
        pageNumberLabel.setText("Стр:" + pageNumber);
        tableView.setItems(FXCollections.observableArrayList(searchResults.subList(pageNumber
                * (Integer)pageAmountChoice.getValue(), (pageNumber + 1)
                *  (Integer)pageAmountChoice.getValue())));
        if (pageNumber == 0) {
            ViewObjectsBuilder.hideButton(prevPageButton);
            ViewObjectsBuilder.hideButton(firstPageButton);
        }
        ViewObjectsBuilder.showButton(nextPageButton);
        ViewObjectsBuilder.showButton(lastPageButton);
        pageNumberLabel.setText("Стр:"+String.valueOf(pageNumber));
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
            ViewObjectsBuilder.hideButton(lastPageButton);
            ViewObjectsBuilder.hideButton(nextPageButton);
        }
        ViewObjectsBuilder.nextPage(pageNumber, pageNumberLabel, nextPageButton, prevPageButton, tableView, toShow);
        ViewObjectsBuilder.showButton(firstPageButton);
        pageNumberLabel.setText("Стр:"+String.valueOf(pageNumber));
    }

    public void changeAmntOfCustomersOnPage() {

       updateTableView();
    }

    public void lastPage() throws Exception {
        int size = searchResults.size();
       pageNumber= ViewObjectsBuilder.lastPage(size,pageNumber,pageAmountChoice,nextPageButton,prevPageButton);
        loadPage();
        ViewObjectsBuilder.showButton(firstPageButton);
        ViewObjectsBuilder.hideButton(lastPageButton);
        ViewObjectsBuilder.hideButton(nextPageButton);
        ViewObjectsBuilder.showButton(prevPageButton);
        pageNumberLabel.setText("Стр:"+String.valueOf(pageNumber));
    }

    private void loadPage() {
        tableView.setItems(FXCollections.observableArrayList());
        pageNumberLabel.setText("Стр:" + pageNumber);
        List<Customer> toShow=null;
        if((pageNumber + 1) *  (Integer)pageAmountChoice.getValue()<=searchResults.size()) {
            toShow = searchResults.subList(pageNumber * (Integer) pageAmountChoice.getValue(),
                    (pageNumber + 1) * (Integer) pageAmountChoice.getValue());
        }else{
            toShow = searchResults.subList(pageNumber * (Integer) pageAmountChoice.getValue(),
                    searchResults.size()-1);
        }
        ViewObjectsBuilder.setItemsTable(toShow,  tableView, nextPageButton, prevPageButton);
        pageNumberLabel.setText("Стр:"+String.valueOf(pageNumber));
    }

    public void firstPage() throws Exception {
        pageNumber=0;
        int size = searchResults.size();
        ViewObjectsBuilder.firstPage(size,pageAmountChoice,nextPageButton,prevPageButton);
        loadPage();
        ViewObjectsBuilder.showButton(lastPageButton);
        ViewObjectsBuilder.hideButton(firstPageButton);
        ViewObjectsBuilder.hideButton(prevPageButton);

        pageNumberLabel.setText("Стр:"+String.valueOf(pageNumber));
    }
}