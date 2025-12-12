package pbz.Romanov.repository;

import java.util.List;
import java.util.Map;

public interface DBMainMenuInterface {
    List<Map<String, Object>> findPrintingsByStateAndType(String state_var, String type_var) throws Exception;

    List<Map<String, Object>> printingsForYear(int year) throws Exception;

    List<Map<String, Object>> unrecievedPrintingsForTwoMonths() throws Exception;

    List<Map<String, Object>> employeesByMonthAndDepartment(int department, String Date, int name) throws Exception;
}
