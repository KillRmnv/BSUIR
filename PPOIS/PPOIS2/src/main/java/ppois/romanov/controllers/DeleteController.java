package ppois.romanov.controllers;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import lombok.Setter;
import ppois.romanov.CustomerProcessingSystem;
import ppois.romanov.CustomerSearchCriteria;

import java.net.URL;
import java.util.ResourceBundle;

public class DeleteController implements Initializable, Controller {
    @FXML
    private Button deleteButton;
    @FXML
    private Label deleteResult;
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
    @Setter
    private CustomerProcessingSystem customerProcessingSystem;

    public void deleteCustomer() throws Exception {
        CustomerSearchCriteria customerToAdd = new CustomerSearchCriteria();
        boolean empty = true;
        customerToAdd.setName(nameField.getText());
        if (nameField.getText().length() > 2)
            empty = false;
        customerToAdd.setAddress(addressField.getText());
        if (addressField.getText().length() > 2)
            empty = false;
        customerToAdd.setMobilePhone(mobilePhoneField.getText());
        if (mobilePhoneField.getText().length() > 2)
            empty = false;
        customerToAdd.setTownPhone(townPhoneField.getText());
        if (townPhoneField.getText().length() > 2)
            empty = false;
        customerToAdd.setAccountNumber(accountNumberField.getText());
        if (accountNumberField.getText().length() > 2)
            empty = false;
        if(!empty) {
            int amnt = customerProcessingSystem.removeCustomer(customerToAdd);
            if (amnt > 0) {
                deleteResult.setText("Количество удаленных клиентов:" + amnt);
            } else {
                deleteResult.setText("Клиенты по критериям не найдены");
            }
        }else{
                deleteResult.setText("Хотя бы одно поле должно содержать не менее 3 символов");
        }
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

    }
}
