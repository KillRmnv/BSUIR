package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.repository.DBMainMenuInterface;

import java.util.List;
import java.util.Map;

@Singleton
public class MainMenuService {
    @Inject
    @Named("PostgreSQLRepository")
    private DBMainMenuInterface dbInterface;


    public MainMenuService(DBMainMenuInterface dbInterface) {
        this.dbInterface = dbInterface;
    }

    public List<Map<String, Object>> findPrintingsByStateAndType(String state_var, String type_var,int page, int amountOnPage) throws Exception {
        var buff=dbInterface.findPrintingsByStateAndType(state_var, type_var);
        if((page - 1) * amountOnPage + amountOnPage<= buff.size()){
            return dbInterface.findPrintingsByStateAndType(state_var, type_var).subList((page - 1) * amountOnPage, (page - 1) * amountOnPage + amountOnPage);
        }else{
            return dbInterface.findPrintingsByStateAndType(state_var, type_var).subList((page - 1) * amountOnPage, buff.size());
        }

    }

    public List<Map<String, Object>> printingsForYear(int page, int amountOnPage,int year) throws Exception {
        var buff=dbInterface.printingsForYear(year);
        if((page - 1) * amountOnPage + amountOnPage<= buff.size()){
            return dbInterface.printingsForYear(year).subList((page - 1) * amountOnPage, (page - 1) * amountOnPage + amountOnPage);
        }else{
            return dbInterface.printingsForYear(year).subList((page - 1) * amountOnPage, buff.size());
        }

    }

    public List<Map<String, Object>> unrecievedPrintingsForTwoMonths(int page, int amountOnPage) throws Exception {
        var buff=dbInterface.unrecievedPrintingsForTwoMonths();
        if((page - 1) * amountOnPage + amountOnPage<= buff.size()){
            return dbInterface.unrecievedPrintingsForTwoMonths().subList((page - 1) * amountOnPage, (page - 1) * amountOnPage + amountOnPage);
        }else{
            return dbInterface.unrecievedPrintingsForTwoMonths().subList((page - 1) * amountOnPage, buff.size());
        }

    }

    public List<Map<String, Object>> employeesByMonthAndDepartment(int department, String Date, int name,int page, int amountOnPage) throws Exception {
        if(Date.isEmpty()){
            throw new Exception("Empty or invalid parameters");
        }
        var buff=dbInterface.employeesByMonthAndDepartment(department, Date, name);
        if((page - 1) * amountOnPage + amountOnPage<= buff.size()){
            return dbInterface.employeesByMonthAndDepartment(department, Date, name).subList((page - 1) * amountOnPage, (page - 1) * amountOnPage + amountOnPage);
        }else{
            return dbInterface.employeesByMonthAndDepartment(department, Date, name).subList((page - 1) * amountOnPage, buff.size());
        }
    }


}
