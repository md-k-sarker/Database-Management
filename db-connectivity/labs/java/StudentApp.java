import java.sql.*;

public class StudentApp {
    // Credentials come from environment variables, never from source code.
    static final String URL  = System.getenv().getOrDefault("DB_URL",
            "jdbc:mysql://localhost:3306/school?useSSL=false&allowPublicKeyRetrieval=true");
    static final String USER = System.getenv().getOrDefault("DB_USER", "app_user");
    static final String PASS = System.getenv().getOrDefault("DB_PASS", "change_me");

    public static void main(String[] args) {
        // try-with-resources closes Connection, PreparedStatement and ResultSet automatically
        try (Connection conn = DriverManager.getConnection(URL, USER, PASS)) {
            System.out.println("Connected to " + conn.getMetaData().getDatabaseProductName());

            String sql = "SELECT sid, name, gpa FROM student WHERE major = ? AND gpa >= ? ORDER BY sid";
            try (PreparedStatement ps = conn.prepareStatement(sql)) {
                ps.setString(1, "Computer Science");   // placeholders are numbered from 1
                ps.setDouble(2, 3.5);
                try (ResultSet rs = ps.executeQuery()) {
                    while (rs.next()) {                 // moves the cursor; false when rows run out
                        int sid = rs.getInt("sid");
                        String name = rs.getString("name");
                        double gpa = rs.getDouble("gpa");
                        System.out.printf("%d  %s  %.2f%n", sid, name, gpa);
                    }
                }
            }

            String upd = "UPDATE student SET gpa = ? WHERE sid = ?";
            try (PreparedStatement ps = conn.prepareStatement(upd)) {
                ps.setDouble(1, 3.95);
                ps.setInt(2, 1);
                System.out.println("rows updated: " + ps.executeUpdate());
            }
        } catch (SQLException e) {
            System.err.println("SQLState=" + e.getSQLState() + " code=" + e.getErrorCode() + " " + e.getMessage());
        }
    }
}
