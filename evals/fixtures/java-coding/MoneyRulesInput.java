import java.math.BigDecimal;

// Synthetic review input. The caller needs exact decimal amounts and numeric equality.
final class MoneyRulesInput {
    BigDecimal parseAmount(String amountText) {
        return new BigDecimal(Double.parseDouble(amountText));
    }

    boolean isOne(BigDecimal amount) {
        return amount.equals(new BigDecimal("1.00"));
    }
}
