package ppois.romanov.data;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.xml.sax.SAXException;
import ppois.romanov.entities.Customer;
import ppois.romanov.CustomerSearchCriteria;

import javax.xml.parsers.*;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;
import java.io.IOException;
import java.sql.SQLException;
import java.util.*;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class XMLSource implements Source {
    private File file;
    Map<Integer, Customer> customers;

    public XMLSource(File file) {
        this.file = file;
        customers = new HashMap<Integer, Customer>();
    }

    @Override
    public List<Customer> load(int start, int limit) throws IOException, SAXException, ParserConfigurationException {
        if (customers.isEmpty()) {
            load(null);
        }
        limit--;
        List<Integer> keys = new ArrayList<>(customers.keySet());
        Collections.sort(keys);
        List<Customer> toLoad = new ArrayList<>();
        for (int startKey = start; startKey <= limit&&startKey< keys.size(); startKey++) {
            toLoad.add(customers.get(keys.get(startKey)));
        }
        return toLoad;
    }

    @Override
    public List<Customer> load(CustomerSearchCriteria condition) throws ParserConfigurationException, IOException, SAXException,NoSuchElementException {
        if (condition == null) {
            customers.clear();
            parseCustomersFromXml(file);
            return new ArrayList<>(customers.values());
        } else {
            Set<Integer> possibleKeys = filterByAccountNumber(condition.getAccountNumber());

            try {
                applyFilters(condition, possibleKeys);
            } catch (NoSuchElementException e) {
                return null;
            }

            return buildResult(possibleKeys);
        }
    }

    private void parseCustomersFromXml(File file) throws ParserConfigurationException, IOException, SAXException {
        if (!file.exists() || file.length() == 0) return;

        SAXParserFactory factory = SAXParserFactory.newInstance();
        SAXParser parser = factory.newSAXParser();
        SAXCustomerHandler handler = new SAXCustomerHandler(customers);
        parser.parse(file, handler);
    }

    private Set<Integer> filterByAccountNumber(String accountNumber)  {
        Set<Integer> keys = new HashSet<>();
        if (!accountNumber.isEmpty()) {
            for (var key : customers.keySet()) {
                String strB = String.valueOf(key);
                if (strB.contains(accountNumber)) {
                    keys.add(key);
                }
            }
        }
        return keys;
    }

    private void applyFilters(CustomerSearchCriteria condition, Set<Integer> possibleKeys) {
        filterCustomersByPattern(
                condition.getName() != null ? condition.getName() : null,
                c -> c.getName(),
                customers,
                possibleKeys
        );

        filterCustomersByPattern(
                condition.getAddress(),
                Customer::getAddress,
                customers,
                possibleKeys
        );
        Set<Integer> possibleKeysWithMobilePhones = new HashSet<>(possibleKeys);
        Set<Integer> possibleKeysWithTownPhones = new HashSet<>(possibleKeys);
        possibleKeys.clear();
        filterCustomersByPattern(
                condition.getMobilePhone(),
                Customer::getMobilePhone,
                customers,
                possibleKeysWithMobilePhones
        );

        filterCustomersByPattern(
                condition.getTownPhone(),
                Customer::getTownPhone,
                customers,
                possibleKeysWithTownPhones
        );
        possibleKeys.addAll(possibleKeysWithMobilePhones);
        possibleKeys.addAll(possibleKeysWithTownPhones);
    }

    private List<Customer> buildResult(Set<Integer> possibleKeys) {
        List<Customer> result = new ArrayList<>();
        for (var key : possibleKeys) {
            result.add(customers.get(key));
        }
        return result;
    }

    private void filterCustomersByPattern(
            String value,
            Function<Customer, String> fieldExtractor,
            Map<Integer, Customer> customers,
            Set<Integer> possibleKeys
    ) {
        if (value == null || value.isEmpty()) return;

        Pattern pattern = Pattern.compile(value);

        if (possibleKeys.isEmpty()) {
            for (var customer : customers.values()) {
                Matcher matcher = pattern.matcher(fieldExtractor.apply(customer));
                if (matcher.find()) {
                    possibleKeys.add(Integer.parseInt(customer.getAccountNumber()));
                }
            }
            if (possibleKeys.isEmpty()) {
                throw new NoSuchElementException("No matching customers found.");
            }
        } else {
            List<Integer> toErase = new ArrayList<>();
            for (var key : possibleKeys) {
                Matcher matcher = pattern.matcher(fieldExtractor.apply(customers.get(key)));
                if (!matcher.find()) {
                    toErase.add(key);
                }
            }
            for (var key : toErase) {
                possibleKeys.remove(key);
            }
        }
    }

    @Override
    public void save(List<Customer> records) {
        try {
            DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder docBuilder = docFactory.newDocumentBuilder();

            Document doc = docBuilder.newDocument();
            Element rootElement = doc.createElement("Customers");
            doc.appendChild(rootElement);

            for (Customer customer : records) {
                Element customerElement = doc.createElement("Customer");
                customerElement.setAttribute("FullName", customer.getName());

                Element account = doc.createElement("Account");
                account.setTextContent(String.valueOf(customer.getAccountNumber()));
                customerElement.appendChild(account);

                Element address = doc.createElement("Address");
                address.setTextContent(customer.getAddress());
                customerElement.appendChild(address);

                Element mobile = doc.createElement("MobilePhone");
                mobile.setTextContent(customer.getMobilePhone());
                customerElement.appendChild(mobile);

                Element town = doc.createElement("TownPhone");
                town.setTextContent(customer.getTownPhone());
                customerElement.appendChild(town);

                rootElement.appendChild(customerElement);
            }

            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");

            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult(file);

            transformer.transform(source, result);

        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Ошибка при сохранении XML: " + e.getMessage());
        }
    }

    @Override
    public boolean add(Customer record) {
        if (customers.containsKey(record.getAccountNumber())) {
            return false;
        }
        customers.put(Integer.parseInt(record.getAccountNumber()), record);
        save(new ArrayList<>(customers.values()));
        //save(new ArrayList<>(List.of(record)));
        return true;
    }

    @Override
    public int delete(CustomerSearchCriteria condition) throws ParserConfigurationException, IOException, SAXException {
        List<Customer> toRemove = load(condition);
        if(toRemove==null){
            return 0;
        }
        for (Customer customer : toRemove) {
            customers.remove(customer.getAccountNumber());
        }
        save(new ArrayList<>(customers.values()));
        return toRemove.size();
    }

    @Override
    public int size() throws SQLException {
        return customers.size();
    }
}