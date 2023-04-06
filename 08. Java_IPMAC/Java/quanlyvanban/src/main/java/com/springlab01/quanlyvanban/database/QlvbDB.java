package com.springlab01.quanlyvanban.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;

import javax.swing.plaf.basic.BasicInternalFrameTitlePane.SystemMenuBar;

import com.springlab01.quanlyvanban.models.DmNguoiDung;

public class QlvbDB {
    Connection conn = null;

    public QlvbDB() {
        try {
            this.conn = DriverManager.getConnection("jdbc:mariadb://localhost:3306/qlvbdb",
                    "root", "admin#123");
        } catch (Exception e) {
            System.out.println("Co loi xay ra khi ket noi CSDL!!!" + e);
        }

    }

    public ArrayList<DmNguoiDung> getNguoiDungAll(){
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
                            + " from qlvbdb.dm_nguoi_dung";
            Statement stmt = this.conn.createStatement();
            ResultSet rs = stmt.executeQuery(sqlText);    
            while(rs.next()) {
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

                if (rs.getTimestamp("NGAY_NHAP") !=null) {
                    dmNguoiDung.setNgayNhap(
                        rs.getTimestamp("NGAY_NHAP").toLocalDateTime()
                        );
                }
                
                dmNguoiDung.setMaNguoiSua(rs.getString("MA_NGUOI_SUA"));
                if(rs.getTimestamp("NGAY_SUA") !=null ) {
                    dmNguoiDung.setNgaySua(
                        rs.getTimestamp("NGAY_SUA").toLocalDateTime()
                        );
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
