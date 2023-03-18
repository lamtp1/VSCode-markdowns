public class CongNhan extends CanBo {
    private EnumBacCongNhan bacCongNhan;

    public void setBacCongNhan(EnumBacCongNhan _bacCongNhan) {
        this.bacCongNhan = _bacCongNhan;
    }

    public EnumBacCongNhan getBacCongNhan() {
        return this.bacCongNhan;
    }

    @Override // the hien tinh da hinh, ham inCanBo nam trong
    public void inCanBo() {
        super.inCanBo(); // goi den lop cha, nhan control+left mouse de cho den lop cha
        System.out.println("Bac cong nhan: " + this.bacCongNhan);
    }
}
