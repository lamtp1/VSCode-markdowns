import java.time.LocalDate;

public class Bao extends TaiLieu {
    private LocalDate ngayPhatHanh;

    public void setNgayPhatHanh(LocalDate _ngayPhatHanh) {
        this.ngayPhatHanh = _ngayPhatHanh;
    }

    public LocalDate getNgayPhatHanh() {
        return this.ngayPhatHanh;
    }

    public void inThongTin() {
        String strThongTin = super.getThongTin();
        strThongTin += "; Ngay phat hanh: " + this.ngayPhatHanh;
        System.out.println(strThongTin);
    }

}
