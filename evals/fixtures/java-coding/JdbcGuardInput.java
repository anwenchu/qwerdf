import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/** Synthetic review input. The caller supplies one active transaction. */
final class JdbcGuardInput {
    private static final String LOCK = "SELECT version FROM synthetic_guard "
            + "WHERE tenant_id = ? AND owner_id = ? FOR UPDATE";
    private static final String UPDATE = "UPDATE synthetic_guard SET version = version + 1 "
            + "WHERE tenant_id = ? AND owner_id = ? AND version = ?";

    boolean increment(Connection connection, long tenantId, long ownerId) throws SQLException {
        long version;
        try (PreparedStatement statement = connection.prepareStatement(LOCK)) {
            statement.setLong(1, tenantId);
            statement.setLong(2, ownerId);
            try (ResultSet rows = statement.executeQuery()) {
                if (!rows.next()) {
                    return false;
                }
                version = rows.getLong("version");
            }
        }
        try (PreparedStatement statement = connection.prepareStatement(UPDATE)) {
            statement.setLong(1, tenantId);
            statement.setLong(2, ownerId);
            statement.setLong(3, version);
            return statement.executeUpdate() == 1;
        }
    }
}
