from string import Template

java_template = Template("""
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Solution {
$solution
}

public class TestSolution {
$tests
}
""")