public class NhanVien extends CanBo {
    private String congViec;

    public void setCongViec(String _congViec) {
        this.congViec = _congViec;
    }

    public String getCongViec() {
        return this.congViec;
    }

    @Override
    public void inCanBo() {
        super.inCanBo();
        System.out.println("Cong viec: " + this.congViec);
    }
}
