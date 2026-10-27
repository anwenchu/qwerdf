import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;

// Synthetic review input. Equality deliberately includes scale; no Service interface is needed.
final class AcceptedPatterns {
    boolean sameRepresentation(BigDecimal first, BigDecimal second) {
        return first.equals(second);
    }

    List<String> renamedLabel() {
        List<String> labels = Arrays.asList("pending", "done");
        labels.set(0, "waiting");
        return labels;
    }
}
