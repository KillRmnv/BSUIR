package ppois.Romanov;

import javafx.collections.FXCollections;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Modality;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ViewObjectsBuilder {
    public static void createColumns(TableColumn<Customer, String> fioColumn,
                                      TableColumn<Customer, Integer> accountNumberColumn,
                                      TableColumn<Customer, String> addressColumn,
                                      TableColumn<Customer, String> mobilePhoneColumn,
                                      TableColumn<Customer, String> townPhoneColumn){
        fioColumn.setCellValueFactory(new PropertyValueFactory<>("name"));
        accountNumberColumn.setCellValueFactory(new PropertyValueFactory<>("accountNumber"));
        addressColumn.setCellValueFactory(new PropertyValueFactory<>("address"));
        mobilePhoneColumn.setCellValueFactory(new PropertyValueFactory<>("mobilePhone"));
        townPhoneColumn.setCellValueFactory(new PropertyValueFactory<>("townPhone"));
    }
    public static void setItemsTable(List<Customer> toShow,
                  int pageNumber,
                  TableView<Customer> tableView,
                  Button nextPageButton,
                  Button prevPageButton){
        if ( CustomerProcessingSystemConstants.amountOfCustomersOnPage == toShow.size())
            tableView.setItems(FXCollections.observableArrayList(toShow));
        else {
            tableView.setItems(FXCollections.observableArrayList(toShow));
            hideButton(nextPageButton);
        }
        showButton(prevPageButton);
    }
    public static void hideButton(Button PageButton){
        PageButton.setDisable(true);
        PageButton.setVisible(false);
    }
    public static void showButton(Button PageButton){
        PageButton.setDisable(false);
        PageButton.setVisible(true);
    }
    public static void buildDialogWindow(FXMLLoader loader,CustomerProcessingSystem customerProcessingSystem,String windowName) throws IOException {
        Parent root = loader.load();
        Controller Controller = loader.getController();
        Controller.setCustomerProcessingSystem(customerProcessingSystem);
        Stage stage = new Stage();
        stage.setTitle(windowName);
        stage.setScene(new Scene(root));
        stage.initModality(Modality.APPLICATION_MODAL);
        stage.showAndWait();
    }
    public static void showViewObject(Node object){
        object.setVisible(true);
        object.setManaged(true);
    }
    public static void hideViewObject(Node object){
        object.setVisible(false);
        object.setManaged(false);
    }public static void  buildTree(CustomerProcessingSystem customerProcessingSystem, TreeView<String> treeView){
        TreeItem<String> root = new TreeItem<>("Customers");
        List<TreeItem<String>> customersTree = new ArrayList<>();
        try {
            for (var cust : customerProcessingSystem.loadCustomers(null)) {
                TreeItem<String> customer = new TreeItem<>(cust.getName());
                TreeItem<String> accountNumber = new TreeItem<>(String.valueOf(cust.getAccountNumber()));
                TreeItem<String> address = new TreeItem<>(cust.getAddress());
                TreeItem<String> phones = new TreeItem<>("Phones");
                TreeItem<String> mobilePhone = new TreeItem<>(cust.getMobilePhone());
                TreeItem<String> townPhone = new TreeItem<>(cust.getTownPhone());
                phones.getChildren().addAll(townPhone, mobilePhone);
                customer.getChildren().addAll(accountNumber, address, phones);
                customersTree.add(customer);
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        root.getChildren().addAll(customersTree);
        treeView.setRoot(root);

    }
    public static  void  nextPage(int pageNumber,Label pageLabel,Button nextPageButton,Button prevPageButton,TableView<Customer> tableView,List<Customer> searchResults){
        pageLabel.setText("Page:" + pageNumber);
        ViewObjectsBuilder.setItemsTable(searchResults, pageNumber, tableView, nextPageButton, prevPageButton);
    }
}