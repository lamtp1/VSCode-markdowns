public class TaiLieu {
    private String maTaiLieu;
    private String tenNhaXuatBan;
    private Integer soBanPhatHanh;

    // Hàm set thông tin
    public void setMaTaiLieu(String _maTaiLieu) {
        this.maTaiLieu = _maTaiLieu;
    }

    public void setTenNhaXuatBan(String _tenNhaXuatBan) {
        this.maTaiLieu = _tenNhaXuatBan;
    }

    public void setSoBanPhatHanh(String _soBanPhatHanh) {
        this.maTaiLieu = _soBanPhatHanh;
    }

    // Hàm get thông tin
    public String getMaTaiLieu() {
        return this.maTaiLieu;
    }

    public String getTenNhaXuatBan() {
        return this.tenNhaXuatBan;
    }

    public Integer getSoBanPhatHanh() {
        return this.soBanPhatHanh;
    }

    public String getThongTin() {
        String strThongTin = "";
        strThongTin += "Ma tai lieu: " + this.maTaiLieu
                + "; Ten nha san xuat: " + this.tenNhaXuatBan
                + "; So ban phat hanh: " + this.soBanPhatHanh;
        return strThongTin;
    }
}
