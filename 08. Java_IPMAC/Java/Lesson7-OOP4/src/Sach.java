public class Sach extends TaiLieu {
    private String tenTacGia;
    private Integer soTrang;

    public void setTenTacGia(String _tenTacGia) {
        this.tenTacGia = _tenTacGia;
    }

    public void setSoTrang(Integer _soTrang) {
        this.soTrang = _soTrang;
    }

    public String getTenTacGia() {
        return this.tenTacGia;
    }

    public Integer getSoTrang() {
        return this.soTrang;
    }

    public void inThongTin() {
        String strThongTin = super.getThongTin();
        strThongTin += "; Ten tac gia: " + this.tenTacGia
                + "; So Trang: " + this.soTrang;
        System.out.println(strThongTin);
    }

}
