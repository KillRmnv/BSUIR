package ppois.Romanov;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.control.*;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.sql.SQLException;
import java.util.List;
import java.util.ResourceBundle;

public class MainController implements Initializable, Controller {
    @FXML
    private ChoiceBox pageAmountChoice;
    @FXML
    private Button migrateButton;
    @FXML
    private Button nextPageButton;
    @FXML
    private Label pageLabel;
    @FXML
    private Button prevPageButton;

    private CustomerProcessingSystem customerProcessingSystem;
    @FXML
    private TableColumn<Customer, String> fioColumn;
    @FXML
    private TableColumn<Customer, Integer> accountNumberColumn;
    @FXML
    private TableColumn<Customer, String> addressColumn;
    @FXML
    private TableColumn<Customer, String> phonesColumn;
    @FXML
    private TableColumn<Customer, String> mobilePhoneColumn;
    @FXML
    private TableColumn<Customer, String> townPhoneColumn;
    @FXML
    private Button addButton;
    @FXML
    private Button deleteButton;
    @FXML
    private Button searchButton;
    @FXML
    private Button treeViewButton;
    @FXML
    private Button tableViewButton;
    @FXML
    private Button xmlButton;
    @FXML
    private Button sqlButton;
    @FXML
    private TableView<Customer> tableView;
    @FXML
    private TreeView<String> treeView;
    private int pageNumber = 0;


    public void showTableView() throws Exception {
        ViewObjectsBuilder.showViewObject(tableView);
        ViewObjectsBuilder.hideViewObject(treeView);

        pageLabel.setVisible(true);
        pageNumber = 0;
        ViewObjectsBuilder.createColumns(fioColumn, accountNumberColumn, addressColumn, mobilePhoneColumn, townPhoneColumn);
        var customers = customerProcessingSystem.loadCustomers(0,
                (Integer) pageAmountChoice.getValue());
        tableView.setItems(FXCollections.observableArrayList(customers));
        pageLabel.setText("Page:" + pageNumber);
        ViewObjectsBuilder.hideButton(prevPageButton);
        if (customers.size() < (Integer) pageAmountChoice.getValue())
            ViewObjectsBuilder.hideButton(nextPageButton);
        else
            ViewObjectsBuilder.showButton(nextPageButton);
    }

    public void showTreeView() {
        ViewObjectsBuilder.hideViewObject(tableView);
        ViewObjectsBuilder.showViewObject(treeView);
        pageLabel.setVisible(false);
        ViewObjectsBuilder.hideButton(prevPageButton);
        ViewObjectsBuilder.hideButton(nextPageButton);
        ViewObjectsBuilder.buildTree(customerProcessingSystem, treeView);
    }

    public void searchCustomer() throws IOException {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("/searchWindow.fxml"));
        ViewObjectsBuilder.buildDialogWindow(loader, customerProcessingSystem, "Search");
    }

    public void deleteCustomer() throws Exception {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("/deleteWindow.fxml"));
        ViewObjectsBuilder.buildDialogWindow(loader, customerProcessingSystem, "Delete");
        if (treeView.isVisible()) {
            showTreeView();
        } else
            loadPage();
    }

    public void addCustomer() throws Exception {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("/addingWindow.fxml"));
        ViewObjectsBuilder.buildDialogWindow(loader, customerProcessingSystem, "Adding");
        if (treeView.isVisible()) {
            showTreeView();
        } else
            loadPage();
    }

    public void loadXmlData() throws Exception {
        customerProcessingSystem.close();
        customerProcessingSystem = new CustomerProcessingSystem(new XMLSource(new File("src/main/resources/xml/customers.xml")));
        if (treeView.isVisible()) {
            showTreeView();
        } else {
            showTableView();
        }
    }

    public void loadSqlData() throws Exception {
        customerProcessingSystem = new CustomerProcessingSystem(new SQLiteSource("src/main/resources/db/customers.db"));
        if (treeView.isVisible()) {
            showTreeView();
        } else {
            showTableView();
        }
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        try {
            customerProcessingSystem = new CustomerProcessingSystem(new SQLiteSource("src/main/resources/db/customers.db"));
        } catch (ClassNotFoundException | SQLException e) {
            throw new RuntimeException(e);
        }
        ObservableList<Integer> pages = FXCollections.observableArrayList(10, 15, 20);
        pageAmountChoice.setItems(pages);
        pageAmountChoice.setValue(15);
        showTreeView();
    }

    public void prevPage() throws Exception {
        pageNumber--;
        pageLabel.setText("Page:" + pageNumber);
        List<Customer> toShow = customerProcessingSystem.loadCustomers(pageNumber *
                (Integer) pageAmountChoice.getValue(), (pageNumber + 1)
                * (Integer) pageAmountChoice.getValue());
        tableView.setItems(FXCollections.observableArrayList(toShow));
        if (pageNumber == 0) {
            ViewObjectsBuilder.hideButton(prevPageButton);
        }
        ViewObjectsBuilder.showButton(nextPageButton);
    }

    public void loadPage() throws Exception {
        tableView.setItems(FXCollections.observableArrayList());
        pageLabel.setText("Page:" + pageNumber);
        List<Customer> toShow = customerProcessingSystem.loadCustomers(pageNumber *
                        (Integer) pageAmountChoice.getValue(),
                (pageNumber + 1) * (Integer) pageAmountChoice.getValue());
        ViewObjectsBuilder.setItemsTable(toShow, (Integer) pageAmountChoice.getValue(), tableView, nextPageButton, prevPageButton);
    }

    public void nextPage() throws Exception {
        pageNumber++;
        List<Customer> toShow = customerProcessingSystem.loadCustomers(pageNumber *
                        (Integer) pageAmountChoice.getValue(),
                (pageNumber + 1) * (Integer) pageAmountChoice.getValue());
        ViewObjectsBuilder.nextPage(pageNumber, pageLabel, nextPageButton, prevPageButton, tableView, toShow);
        toShow = customerProcessingSystem.loadCustomers((pageNumber + 1) *
                        (Integer) pageAmountChoice.getValue(),
                (pageNumber + 1) * (Integer) pageAmountChoice.getValue() + 1);
        if (toShow.isEmpty()) {
            ViewObjectsBuilder.hideButton(nextPageButton);
        }
    }

    @Override
    public void setCustomerProcessingSystem(CustomerProcessingSystem customerProcessingSystem) {
        this.customerProcessingSystem = customerProcessingSystem;
    }

    public void migrateData() throws Exception {
        customerProcessingSystem.migrate();
    }

    public void changeAmntOfCustomersOnPage() throws Exception {
        if (tableView.isVisible())
            showTableView();
    }
}