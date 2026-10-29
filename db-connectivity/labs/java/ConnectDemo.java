import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnectDemo {
    public static void main(String[] args) {
        // jdbc:<subprotocol>://<host>:<port>/<database>?<options>
        String url  = "jdbc:mysql://localhost:3306/school";
        String user = System.getenv("DB_USER");
        String pass = System.getenv("DB_PASS");

        // No Class.forName(...) needed: a JDBC 4+ driver jar on the classpath registers itself.
        try (Connection conn = DriverManager.getConnection(url, user, pass)) {
            System.out.println("Connected: " + conn.getMetaData().getDatabaseProductName()
                    + " " + conn.getMetaData().getDatabaseProductVersion());
        } catch (SQLException e) {
            System.err.println("Could not connect: " + e.getMessage());
        }   // the connection is closed here, even if an exception was thrown
    }
}
