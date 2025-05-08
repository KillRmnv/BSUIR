package by.romanov.ppois;

import java.lang.reflect.InvocationTargetException;

public interface State {
    void run(Context context) throws Exception;
    State next(Context context) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException;

}