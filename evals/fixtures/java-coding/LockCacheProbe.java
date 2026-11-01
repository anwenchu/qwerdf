import java.io.StringReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import org.apache.ibatis.builder.xml.XMLMapperBuilder;
import org.apache.ibatis.datasource.unpooled.UnpooledDataSource;
import org.apache.ibatis.mapping.Environment;
import org.apache.ibatis.session.Configuration;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.apache.ibatis.transaction.jdbc.JdbcTransactionFactory;

/** Isolated MyBatis/H2 cache probe, not production data access or a Spring integration test. */
public final class LockCacheProbe {
    private static SqlSessionFactory factory(String url, boolean cached, boolean locking) {
        Configuration configuration = new Configuration(new Environment("probe",
                new JdbcTransactionFactory(), new UnpooledDataSource("org.h2.Driver", url, "sa", "")));
        String xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
                + "<!DOCTYPE mapper PUBLIC \"-//mybatis.org//DTD Mapper 3.0//EN\" "
                + "\"https://mybatis.org/dtd/mybatis-3-mapper.dtd\">"
                + "<mapper namespace=\"probe\"><cache/>"
                + "<select id=\"read\" parameterType=\"int\" resultType=\"int\" useCache=\""
                + cached + "\">SELECT amount FROM guard_probe WHERE id = #{id}"
                + (locking ? " FOR UPDATE" : "") + "</select></mapper>";
        new XMLMapperBuilder(new StringReader(xml), configuration, "probe.xml",
                configuration.getSqlFragments()).parse();
        return new SqlSessionFactoryBuilder().build(configuration);
    }

    private static boolean update(Connection connection) throws SQLException {
        try (Statement statement = connection.createStatement()) {
            statement.executeUpdate("UPDATE guard_probe SET amount = amount + 1 WHERE id = 1");
            return true;
        } catch (SQLException failure) {
            if (failure.getErrorCode() != 50200) {
                throw failure;
            }
            return false; // H2 lock timeout: only the expected conflict counts as blocked.
        }
    }

    private static void run(boolean cached, boolean locking) throws Exception {
        String url = "jdbc:h2:mem:cache_probe_" + cached + "_" + locking
                + ";DB_CLOSE_DELAY=-1;LOCK_TIMEOUT=150";
        try (Connection seed = DriverManager.getConnection(url, "sa", "");
                Statement statement = seed.createStatement()) {
            statement.execute("CREATE TABLE guard_probe(id INT PRIMARY KEY, amount INT NOT NULL)");
            statement.execute("INSERT INTO guard_probe VALUES(1,100)");
        }
        SqlSessionFactory factory = factory(url, cached, locking);
        try (SqlSession warm = factory.openSession(false)) {
            if (((Integer) warm.selectOne("probe.read", 1)) != 100) {
                throw new AssertionError("Unexpected seed value");
            }
            warm.commit(true);
        }
        try (SqlSession holder = factory.openSession(false);
                Connection competitor = DriverManager.getConnection(url, "sa", "")) {
            holder.selectOne("probe.read", 1);
            holder.selectOne("probe.read", 1); // Local-cache reuse while a genuine lock remains held is legal.
            boolean during = update(competitor);
            boolean expectedDuring = !locking || cached;
            if (during != expectedDuring) {
                throw new AssertionError("Unexpected lock behavior: cached=" + cached + ", locking=" + locking);
            }
            holder.rollback(true);
            if (!update(competitor)) {
                throw new AssertionError("Conflict remained after holder transaction ended");
            }
            System.out.println("locking=" + locking + ", useCache=" + cached
                    + ", competitorDuring=" + during + ", competitorAfterRollback=true");
        }
    }

    public static void main(String[] args) throws Exception {
        Class.forName("org.h2.Driver");
        System.out.println("MyBatis=" + SqlSession.class.getPackage().getImplementationVersion());
        run(true, true);   // Negative input: a cache hit cannot acquire a database row lock.
        run(false, true);  // Positive control: lock blocks a competing update, then releases.
        run(true, false);  // Ordinary reads may legitimately use the cache.
    }
}
