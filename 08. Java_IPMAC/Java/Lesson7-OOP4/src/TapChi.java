public class TapChi extends TaiLieu {
    private Integer soPhatHanh;
    private Integer thangPhatHanh;

    public void setSoPhatHanh(Integer _soPhatHanh) {
        this.soPhatHanh = _soPhatHanh;
    }

    public void setThangPhatHanh(Integer _thangPhatHanh) {
        this.thangPhatHanh = _thangPhatHanh;
    }

    public Integer getSoPhatHanh() {
        return this.soPhatHanh;
    }

    public Integer getThangPhatHanh() {
        return this.thangPhatHanh;
    }

    public void inThongTin() {
        String strThongTin = super.getThongTin();
        strThongTin += "; So phat hanh: " + this.soPhatHanh
                + "; Thang phat hanh: " + this.thangPhatHanh;
        System.out.println(strThongTin);
    }

}