package pbz.Romanov.repository;

import java.util.List;
import java.util.Map;

public interface DBMainMenuInterface {
    List<Map<String, Object>> findPrintingsByStateAndType(String state_var, String type_var) throws Exception;

    List<Map<String, Object>> printingsForYear() throws Exception;

    List<Map<String, Object>> unrecievedPrintingsForTwoMonths() throws Exception;

    List<Map<String, Object>> employeesByMonthAndDepartment(String department, String Date, String name) throws Exception;
}
