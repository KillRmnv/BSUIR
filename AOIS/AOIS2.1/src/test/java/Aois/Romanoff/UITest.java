package Aois.Romanoff;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
public class UITest {

    @Test
    void testGetInput() {
        Scanner scanner = mock(Scanner.class);
        when(scanner.nextLine()).thenReturn("A&B");

        UI ui = new UI();
        String result = ui.getInput(scanner);

        assertEquals("A&B", result);
    }
}
