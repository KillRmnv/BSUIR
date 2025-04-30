package by.romanov.ppois.HRDepartment.HRDepartmentsStates;

import by.romanov.ppois.Context;
import by.romanov.ppois.HRDepartment.HRDepartmentContext;
import by.romanov.ppois.HRDepartment.HRDepartmentInput;
import by.romanov.ppois.PoliceMan;
import by.romanov.ppois.State;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class HirePoliceManState implements State {
    @Override
    public void run(Context context) {
        HRDepartmentContext hrContext = (HRDepartmentContext) context;
        HRDepartmentInput input=new HRDepartmentInput( hrContext.getInput());
        List<PoliceMan> newPoliceMans = new ArrayList<>();
        Random random = new Random();
        int choice=0;
        input.showBudget(hrContext.getBudget());
        do {
            for (int index = 0; index < 10; index++) {
                int randomId = random.nextInt();
                while (hrContext.getPoliceMans().containsKey(randomId)) {
                    randomId = random.nextInt();
                }
                PoliceMan newOne = new PoliceMan(randomId);
                newPoliceMans.add(newOne);
                input.showPoliceManInfo(newOne.Info(),index);
            }
            input.showLastTwoHireOptions();
            choice = input.getPoliceManHireChoice();
            if (choice == 11) {
                break;
            }else if (choice !=10) {
               try {
                   hrContext.addPoliceMan(newPoliceMans.get(choice));
               }catch (Exception e){
                   System.out.println(e.getMessage());
                   choice=10;
               }
            }
            newPoliceMans.clear();
        }
        while (choice==10) ;
    }

    @Override
    public State next(Context context) {
        return null;
    }
}
