import javax.print.DocFlavor.STRING;

public class CanBo {
    private String maCanBo;
    private String hoTen;
    private Integer tuoi;
    private EnumGioiTinh gioiTinh;
    private String diaChi;

    public void setMaCanBo(String _maCanBo) {
        this.maCanBo = _maCanBo;
    }

    public void setHoten(String _hoTen) {
        this.hoTen = _hoTen; // this hieu la class can bo
    }

    public void setTuoi(Integer _tuoi) { // de gach _ de phan biet param va thuoc tinh cua class
        this.tuoi = _tuoi;
    }

    public void setGioiTinh(EnumGioiTinh _gioiTinh) {
        this.gioiTinh = _gioiTinh;
    }

    public void setDiaChi(String _diaChi) {
        this.diaChi = _diaChi;

    }

    // Get gia tri cua cac thuoc tinh
    public String getMaCanBo() {
        return this.maCanBo;
    }

    public String getHoTen() {
        return this.hoTen;
    }

    public Integer getTuoi() {
        return this.tuoi;
    }

    public String getDiaChi() {
        return this.diaChi;
    }

    public Enum getGioiTinh() {
        return this.gioiTinh;
    }

    // phuong thuc in can bo
    public void inCanBo() {
        System.out.println("Ho ten:" + this.hoTen
                + "; Tuoi: " + this.tuoi
                + "; Gioi tinh: " + this.gioiTinh
                + "; Dia chi: " + this.diaChi);
    }
}
