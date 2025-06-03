package ppois.romanov.controllers;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import lombok.Setter;
import ppois.romanov.entities.Customer;
import ppois.romanov.CustomerProcessingSystem;

import java.net.URL;
import java.util.ResourceBundle;

public class AddingController implements Initializable, Controller {
    @FXML
    private Label addingResult;
    @Setter
    private CustomerProcessingSystem customerProcessingSystem;
    @FXML
    private TextField accountNumberField;
    @FXML
    private TextField nameField;
    @FXML
    private TextField addressField;
    @FXML
    private TextField mobilePhoneField;
    @FXML
    private TextField townPhoneField;
    @FXML
    private Button addButton;

    public void addCustomer( ) throws Exception {
        Customer customerToAdd = new Customer();
        try {
            customerToAdd.setAccountNumber(Integer.parseInt(accountNumberField.getText()));
        }
        catch(IllegalArgumentException ignored) {
            addingResult.setText(ignored.getMessage());
            return;
        }
        if(nameField.getText().isEmpty()) {
            addingResult.setText("Имя не должно быть пустым");
            return;
        }
        customerToAdd.setName(nameField.getText());
        if(addressField.getText().isEmpty()) {
            addingResult.setText("Адрес не должен быть пустым");
            return;
        }
        customerToAdd.setAddress(addressField.getText());
        try {
            customerToAdd.setMobilePhone(mobilePhoneField.getText());
        }catch(IllegalArgumentException ignored) {
            addingResult.setText(ignored.getMessage());
            return;
        }
        try {
            customerToAdd.setTownPhone(townPhoneField.getText());
        } catch(IllegalArgumentException ignored) {
            addingResult.setText(ignored.getMessage());
            return;
        }
        if (customerProcessingSystem.addCustomer(customerToAdd)) {
            addingResult.setText("Successfully added");
        } else {
            addingResult.setText("Failed to add");
        }
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

    }
}
