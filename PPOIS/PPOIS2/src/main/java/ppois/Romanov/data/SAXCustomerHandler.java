package ppois.Romanov.data;

import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;
import ppois.Romanov.entities.Customer;
import ppois.Romanov.entities.FullName;

import java.util.Map;

public class SAXCustomerHandler extends DefaultHandler {
    private final Map<Integer, Customer> customers;
    private StringBuilder content;
    private String name;
    private String address;
    private String mobilePhone;
    private String townPhone;
    private int account;

    public SAXCustomerHandler(Map<Integer, Customer> customers) {
        this.customers = customers;
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) {
        content = new StringBuilder();
        if (qName.equalsIgnoreCase("Customer")) {
            name = attributes.getValue("FullName");
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) {
        content.append(ch, start, length);
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        switch (qName) {
            case "Account":
                account = Integer.parseInt(content.toString().trim());
                break;
            case "Address":
                address = content.toString().trim();
                break;
            case "MobilePhone":
                mobilePhone = content.toString().trim();
                break;
            case "TownPhone":
                townPhone = content.toString().trim();
                break;
            case "Customer":
                Customer customer = new Customer(new FullName(name), account, mobilePhone, townPhone);
                customer.setAddress(address);
                customers.put(account, customer);
                break;
        }
    }
}

