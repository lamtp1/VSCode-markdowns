package com.springlab01.quanlyvanban.models;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class DmNguoiDung {
    private String maNguoiDung;
    private String tenNguoiDung;
    private String matKhau;
    private String email;
    private String soDienThoai;
    private Integer gioiTinh;
    private String maPhongBan;
    private Integer trangThai;
    private String maNguoiNhap;
    private LocalDateTime ngayNhap;
    private String maNguoiSua;
    private LocalDateTime ngaySua;
    private Boolean blTrangThai;


    public DmNguoiDung() {
        
    }

    public DmNguoiDung(String maNguoiDung, String tenNguoiDung, String matKhau, String email, String soDienThoai,
            Integer gioiTinh, String maPhongBan, Integer trangThai, String maNguoiNhap, LocalDateTime ngayNhap,
            String maNguoiSua, LocalDateTime ngaySua) {
        this.maNguoiDung = maNguoiDung;
        this.tenNguoiDung = tenNguoiDung;
        this.matKhau = matKhau;
        this.email = email;
        this.soDienThoai = soDienThoai;
        this.gioiTinh = gioiTinh;
        this.maPhongBan = maPhongBan;
        this.trangThai = trangThai;
        this.maNguoiNhap = maNguoiNhap;
        this.ngayNhap = ngayNhap;
        this.maNguoiSua = maNguoiSua;
        this.ngaySua = ngaySua;
    }
    

    public void setMaNguoiDung(String maNguoiDung) {
        this.maNguoiDung = maNguoiDung;
    }
    public void setTenNguoiDung(String tenNguoiDung) {
        this.tenNguoiDung = tenNguoiDung;
    }
    public void setMatKhau(String matKhau) {
        this.matKhau = matKhau;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    public void setSoDienThoai(String soDienThoai) {
        this.soDienThoai = soDienThoai;
    }
    public void setGioiTinh(Integer gioiTinh) {
        this.gioiTinh = gioiTinh;
    }
    public void setMaPhongBan(String maPhongBan) {
        this.maPhongBan = maPhongBan;
    }
    public void setTrangThai(Integer trangThai) {
        this.trangThai = trangThai;
    }
    public void setMaNguoiNhap(String maNguoiNhap) {
        this.maNguoiNhap = maNguoiNhap;
    }
    public void setNgayNhap(LocalDateTime ngayNhap) {
        this.ngayNhap = ngayNhap;
    }
    public void setMaNguoiSua(String maNguoiSua) {
        this.maNguoiSua = maNguoiSua;
    }
    public void setNgaySua(LocalDateTime ngaySua) {
        this.ngaySua = ngaySua;
    }
   
    public String getMaNguoiDung() {
        return maNguoiDung;
    }
    public String getTenNguoiDung() {
        return tenNguoiDung;
    }
    public String getMatKhau() {
        return matKhau;
    }
    public String getEmail() {
        return email;
    }
    public String getSoDienThoai() {
        return soDienThoai;
    }
    public Integer getGioiTinh() {
        return gioiTinh;
    }
    public String getMaPhongBan() {
        return maPhongBan;
    }
    public Integer getTrangThai() {
        return trangThai;
    }
    public String getMaNguoiNhap() {
        return maNguoiNhap;
    }
    public String getNgayNhap() {
        if (this.ngayNhap == null)
        {
            return "";
        }
        DateTimeFormatter fr =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        
        return this.ngayNhap.format(fr);
    }
    
    public String getMaNguoiSua() {
        return maNguoiSua;
    }
    public String getNgaySua() {
        if (this.ngaySua == null)
        {
            return "";
        }
        DateTimeFormatter fr =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        
        return this.ngaySua.format(fr);
    }

    public void setBlTrangThai(Boolean blTrangThai) {
        this.blTrangThai = blTrangThai;
    }

    public Boolean getBlTrangThai() {
        return blTrangThai;
    }

    

}
