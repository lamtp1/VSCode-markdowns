package com.springlab01.quanlyvanban.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;

import org.springframework.boot.origin.SystemEnvironmentOrigin;

import com.springlab01.quanlyvanban.models.DmNguoiDung;

public class QlvbDB {
    Connection conn = null;

    public QlvbDB() {
        try {
            this.conn = DriverManager.getConnection("jdbc:mariadb://localhost:3306/sys",
                    "root", "160299");
        } catch (Exception e) {
            System.out.println("Co loi xay ra khi ket noi CSDL!!!" + e);
        }

    }

    public void deleteNguoiDung(String maNguoiDung) {
        try {
            String sqlText = "delete from dm_nguoi_dung where MA_NGUOI_DUNG='" + maNguoiDung + "'";
            System.out.println("sqlText:" + sqlText);

            Statement stmt = this.conn.createStatement();
            stmt.executeQuery(sqlText);

        } catch (Exception e) {
            // TODO: handle exception
            System.out.println("deleteNguoiDung co loi xay ra:" + e);
        }
    }

    public void updateNguoiDung(DmNguoiDung dmNguoiDung) {
        try {
            String sqlText = "update dm_nguoi_dung set ";
            if (dmNguoiDung.getTenNguoiDung() == null || dmNguoiDung.getTenNguoiDung().isEmpty()) {
                sqlText += " TEN_NGUOI_DUNG = null ";
            } else {
                sqlText += " TEN_NGUOI_DUNG = '" + dmNguoiDung.getTenNguoiDung() + "' ";
            }

            if (dmNguoiDung.getMatKhau() == null || dmNguoiDung.getMatKhau().isEmpty()) {
                sqlText += ",MAT_KHAU = null ";
            } else {
                sqlText += ",MAT_KHAU = '" + dmNguoiDung.getMatKhau() + "' ";
            }

            if (dmNguoiDung.getEmail() == null || dmNguoiDung.getEmail().isEmpty()) {
                sqlText += ",EMAIL = null ";
            } else {
                sqlText += ",EMAIL = '" + dmNguoiDung.getEmail() + "' ";
            }

            if (dmNguoiDung.getSoDienThoai() == null || dmNguoiDung.getSoDienThoai().isEmpty()) {
                sqlText += ",SO_DIEN_THOAI = null ";
            } else {
                sqlText += ",SO_DIEN_THOAI = '" + dmNguoiDung.getSoDienThoai() + "' ";
            }

            if (dmNguoiDung.getGioiTinh() == null) {
                sqlText += ",GIOI_TINH = null ";
            } else {
                sqlText += ",GIOI_TINH = " + dmNguoiDung.getGioiTinh() + " ";
            }

            if (dmNguoiDung.getMaPhongBan() == null || dmNguoiDung.getMaPhongBan().isEmpty()) {
                sqlText += ",MA_PHONG_BAN = null ";
            } else {
                sqlText += ",MA_PHONG_BAN = '" + dmNguoiDung.getMaPhongBan() + "' ";
            }

            if (dmNguoiDung.getTrangThai() == null) {
                sqlText += ",TRANG_THAI = null ";
            } else {
                sqlText += ",TRANG_THAI = " + dmNguoiDung.getTrangThai() + " ";
            }

            sqlText += " ,MA_NGUOI_SUA = '" + dmNguoiDung.getMaNguoiDung() + "' ";
            sqlText += " ,NGAY_SUA = now() ";
            sqlText += " WHERE MA_NGUOI_DUNG='" + dmNguoiDung.getMaNguoiDung() + "' ";

            System.out.println("sqlText:" + sqlText);

            Statement stmt = this.conn.createStatement();
            stmt.executeQuery(sqlText);

        } catch (Exception e) {
            // TODO: handle exception
            System.out.println("updateNguoiDung co loi xay ra:" + e);
        }
    }

    public DmNguoiDung getNguoiDungByMaNguoiDung(String maNguoiDung) {
        DmNguoiDung dmNguoiDung = null;
        try {
            String sqlText = "select "
                    + "MA_NGUOI_DUNG, "
                    + "TEN_NGUOI_DUNG,"
                    + "MAT_KHAU,"
                    + "EMAIL,"
                    + "SO_DIEN_THOAI,"
                    + "GIOI_TINH,"
                    + "MA_PHONG_BAN,"
                    + "TRANG_THAI,"
                    + "MA_NGUOI_NHAP,"
                    + "NGAY_NHAP,"
                    + "MA_NGUOI_SUA,"
                    + "NGAY_SUA"
                    + " from sys.dm_nguoi_dung "
                    + " where upper(MA_NGUOI_DUNG) = '"
                    + maNguoiDung.toUpperCase() + "'";

            Statement stmt = this.conn.createStatement();
            ResultSet rs = stmt.executeQuery(sqlText);
            while (rs.next()) {
                dmNguoiDung = new DmNguoiDung();
                dmNguoiDung.setMaNguoiDung(rs.getString("MA_NGUOI_DUNG"));
                dmNguoiDung.setTenNguoiDung(rs.getString("TEN_NGUOI_DUNG"));
                dmNguoiDung.setMatKhau(rs.getString("MAT_KHAU"));
                dmNguoiDung.setEmail(rs.getString("EMAIL"));
                dmNguoiDung.setSoDienThoai(rs.getString("SO_DIEN_THOAI"));
                dmNguoiDung.setGioiTinh(rs.getInt("GIOI_TINH"));
                dmNguoiDung.setMaPhongBan(rs.getString("MA_PHONG_BAN"));
                dmNguoiDung.setTrangThai(rs.getInt("TRANG_THAI"));
                dmNguoiDung.setMaNguoiNhap(rs.getString("MA_NGUOI_NHAP"));

                if (rs.getTimestamp("NGAY_NHAP") != null) {
                    dmNguoiDung.setNgayNhap(
                            rs.getTimestamp("NGAY_NHAP").toLocalDateTime());
                }

                dmNguoiDung.setMaNguoiSua(rs.getString("MA_NGUOI_SUA"));
                if (rs.getTimestamp("NGAY_SUA") != null) {
                    dmNguoiDung.setNgaySua(
                            rs.getTimestamp("NGAY_SUA").toLocalDateTime());
                }

                // arrResult.add(dmNguoiDung);
            }

        } catch (Exception e) {
            // TODO: handle exception
            System.out.println(" getNguoiDungByMaNguoiDung Co loi xay ra:" + e);
        }
        return dmNguoiDung;
    }

    public void insertNguoiDung(DmNguoiDung nguoiDung) {
        try {
            String sqlText = "insert into DM_NGUOI_DUNG("
                    + "MA_NGUOI_DUNG, "
                    + "TEN_NGUOI_DUNG,"
                    + "MAT_KHAU,"
                    + "EMAIL,"
                    + "SO_DIEN_THOAI,"
                    + "GIOI_TINH,"
                    + "MA_PHONG_BAN,"
                    + "TRANG_THAI,"
                    + "MA_NGUOI_NHAP,"
                    + "NGAY_NHAP,"
                    + "MA_NGUOI_SUA,"
                    + "NGAY_SUA"
                    + ")"
                    + "VALUES(";
            if (nguoiDung.getMaNguoiDung() == null ||
                    nguoiDung.getMaNguoiDung().isEmpty()) {
                sqlText += "null";
            } else {
                sqlText += "'" + nguoiDung.getMaNguoiDung() + "'";
            }

            if (nguoiDung.getTenNguoiDung() == null ||
                    nguoiDung.getTenNguoiDung().isEmpty()) {
                sqlText += ",null";
            } else {
                sqlText += ",'" + nguoiDung.getTenNguoiDung() + "'";
            }

            if (nguoiDung.getMatKhau() == null ||
                    nguoiDung.getMatKhau().isEmpty()) {
                sqlText += ",null";
            } else {
                sqlText += ",'" + nguoiDung.getMatKhau() + "'";
            }

            if (nguoiDung.getEmail() == null ||
                    nguoiDung.getEmail().isEmpty()) {
                sqlText += ",null";
            } else {
                sqlText += ",'" + nguoiDung.getEmail() + "'";
            }

            if (nguoiDung.getSoDienThoai() == null ||
                    nguoiDung.getSoDienThoai().isEmpty()) {
                sqlText += ",null";
            } else {
                sqlText += ",'" + nguoiDung.getSoDienThoai() + "'";
            }

            if (nguoiDung.getGioiTinh() == null) {
                sqlText += ",null";
            } else {
                sqlText += "," + nguoiDung.getGioiTinh() + "";
            }

            if (nguoiDung.getMaPhongBan() == null ||
                    nguoiDung.getMaPhongBan().isEmpty()) {
                sqlText += ",null";
            } else {
                sqlText += ",'" + nguoiDung.getMaPhongBan() + "'";
            }

            if (nguoiDung.getTrangThai() == null) {
                sqlText += ",null";
            } else {
                sqlText += "," + nguoiDung.getTrangThai() + "";
            }

            if (nguoiDung.getMaNguoiDung() == null ||
                    nguoiDung.getMaNguoiDung().isEmpty()) {
                sqlText += ",null";
            } else {
                sqlText += ",'" + nguoiDung.getMaNguoiDung() + "'";
            }

            sqlText += ",now()";
            sqlText += ",null";
            sqlText += ",null";
            sqlText += ")";
            ;
            System.out.println("sqlText:" + sqlText);
            Statement stmt = this.conn.createStatement();
            stmt.executeQuery(sqlText);

        } catch (Exception e) {
            // TODO: handle exception
            System.out.println("insertNguoiDung: Co loi xay ra: " + e);
        }
    }

    public ArrayList<DmNguoiDung> getNguoiDungAll() {
        ArrayList<DmNguoiDung> arrResult = new ArrayList<>();
        try {
            String sqlText = "select "
                    + "MA_NGUOI_DUNG, "
                    + "TEN_NGUOI_DUNG,"
                    + "MAT_KHAU,"
                    + "EMAIL,"
                    + "SO_DIEN_THOAI,"
                    + "GIOI_TINH,"
                    + "MA_PHONG_BAN,"
                    + "TRANG_THAI,"
                    + "MA_NGUOI_NHAP,"
                    + "NGAY_NHAP,"
                    + "MA_NGUOI_SUA,"
                    + "NGAY_SUA"
                    + " from sys.dm_nguoi_dung";
            Statement stmt = this.conn.createStatement();
            ResultSet rs = stmt.executeQuery(sqlText);
            while (rs.next()) {
                DmNguoiDung dmNguoiDung = new DmNguoiDung();
                dmNguoiDung.setMaNguoiDung(rs.getString("MA_NGUOI_DUNG"));
                dmNguoiDung.setTenNguoiDung(rs.getString("TEN_NGUOI_DUNG"));
                dmNguoiDung.setMatKhau(rs.getString("MAT_KHAU"));
                dmNguoiDung.setEmail(rs.getString("EMAIL"));
                dmNguoiDung.setSoDienThoai(rs.getString("SO_DIEN_THOAI"));
                dmNguoiDung.setGioiTinh(rs.getInt("GIOI_TINH"));
                dmNguoiDung.setMaPhongBan(rs.getString("MA_PHONG_BAN"));
                dmNguoiDung.setTrangThai(rs.getInt("TRANG_THAI"));
                dmNguoiDung.setMaNguoiNhap(rs.getString("MA_NGUOI_NHAP"));

                if (rs.getTimestamp("NGAY_NHAP") != null) {
                    dmNguoiDung.setNgayNhap(
                            rs.getTimestamp("NGAY_NHAP").toLocalDateTime());
                }

                dmNguoiDung.setMaNguoiSua(rs.getString("MA_NGUOI_SUA"));
                if (rs.getTimestamp("NGAY_SUA") != null) {
                    dmNguoiDung.setNgaySua(
                            rs.getTimestamp("NGAY_SUA").toLocalDateTime());
                }

                arrResult.add(dmNguoiDung);
            }

        } catch (Exception e) {
            // TODO: handle exception
            System.out.println("Co loi xay ra: " + e);
        }

        return arrResult;
    }

    public void getThongTinNguoiDung() {
        try {
            String sqlText = "select MA_NGUOI_DUNG , TEN_NGUOI_DUNG , MAT_KHAU , EMAIL, NGAY_NHAP,"
                    + " NGAY_SUA from dm_nguoi_dung"
                    + " where 1=1";

            Statement stmt = this.conn.createStatement();
            ResultSet rs = stmt.executeQuery(sqlText);
            HashMap<Integer, Integer> hmap = new HashMap<>();
            while (rs.next()) {
                for (int i = 1; i <= rs.getMetaData().getColumnCount(); i++) {
                    if (hmap.get(i) == null) {
                        hmap.put(i, 0);
                    }

                    if (hmap.get(i) < rs.getMetaData().getColumnName(i).length()) {
                        hmap.put(i, rs.getMetaData().getColumnName(i).length());
                    }

                    if (rs.getObject(i) != null) {
                        if (hmap.get(i) < rs.getString(i).length()) {
                            hmap.put(i, rs.getString(i).length());
                        }
                    }
                }
            }
            System.out.println("hmap: " + hmap);
            String strFormatColumns = "";
            for (Integer key : hmap.keySet()) {
                strFormatColumns += "%1$" + hmap.get(key) + "s |";
            }
            System.out.println("strFormatColumns: " + strFormatColumns);
            for (int i = 1; i <= rs.getMetaData().getColumnCount(); i++) {
                System.out.print(String.format("%1$"
                        + (hmap.get(i) == 0 ? "" : hmap.get(i)) + "s |", rs.getMetaData().getColumnName(i)));

            }
            ResultSet rs2 = stmt.executeQuery(sqlText);
            while (rs2.next()) {
                System.out.println();
                for (int i = 1; i <= rs2.getMetaData().getColumnCount(); i++) {
                    // System.out.println(rs.getString(i));
                    System.out.print(String.format("%1$"
                            + (hmap.get(i) == 0 ? "" : hmap.get(i)) + "s |", rs2.getString(i)));

                }

            }

        } catch (Exception e) {
            System.out.println("Co loi xay ra!!!" + e);
        }

    }
}
