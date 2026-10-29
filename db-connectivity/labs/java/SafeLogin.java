import java.sql.*;

public class SafeLogin {
    // VULNERABLE: the input becomes part of the SQL text
    static boolean loginBad(Connection c, String user, String pass) throws SQLException {
        String sql = "SELECT 1 FROM users WHERE username = '" + user + "' AND password = '" + pass + "'";
        try (Statement st = c.createStatement(); ResultSet rs = st.executeQuery(sql)) {
            return rs.next();
        }
    }

    // SAFE: fixed SQL text, values sent separately
    static boolean loginGood(Connection c, String user, String pass) throws SQLException {
        String sql = "SELECT 1 FROM users WHERE username = ? AND password = ?";
        try (PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, user);
            ps.setString(2, pass);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        }
    }

    // A placeholder cannot hold a column name, so check against a fixed list
    static String sortColumn(String requested) {
        switch (requested) {
            case "name": case "price": return requested;
            default: throw new IllegalArgumentException("bad sort column");
        }
    }
}
