package ppois.Romanov;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import lombok.Setter;

import java.net.URL;
import java.util.ResourceBundle;

public class DeleteController implements Initializable,Controller {
    public Button deleteButton;
    public Label deleteResult;
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

    public void deleteCustomer( ) throws Exception {
        CustomerSearchCriteria customerToAdd = new CustomerSearchCriteria();
        customerToAdd.setName(nameField.getText());
        customerToAdd.setAddress(addressField.getText());
        customerToAdd.setMobilePhone(mobilePhoneField.getText());
        customerToAdd.setTownPhone(townPhoneField.getText());
        customerToAdd.setAccountNumber(accountNumberField.getText());

        int amnt = customerProcessingSystem.removeCustomer(customerToAdd);

        if (amnt > 0) {
            deleteResult.setText("Amount of deleted successfully:" + amnt);
        } else {
            deleteResult.setText("Customer not found");
        }
    }

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

    }
}
