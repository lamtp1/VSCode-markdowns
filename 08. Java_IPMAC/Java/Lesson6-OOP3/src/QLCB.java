import java.util.ArrayList;

public class QLCB {
    private ArrayList<CongNhan> arrCongNhan;
    private ArrayList<KySu> arrKySu;
    private ArrayList<NhanVien> arrNhanVien;
    private Integer iSoLuongCongNhan;
    private Integer iSoLuongKySu;
    private Integer iSoLuongNhanVien;

    // Ham khoi tao co tham so, muon nhap phai biet so luong nhan vien
    QLCB(Integer _iSoLuongCongNhan, Integer _iSoLuongKySu, Integer _iSoLuongNhanVien) {
        this.iSoLuongCongNhan = _iSoLuongCongNhan;
        this.iSoLuongKySu = _iSoLuongKySu;
        this.iSoLuongNhanVien = _iSoLuongNhanVien;
        this.arrCongNhan = new ArrayList<>();
        this.arrKySu = new ArrayList<>();
        this.arrNhanVien = new ArrayList<>();

    }

    /* Them moi cong nhan, ky su, nhan vien */
    public void themMoiCongNhan(CongNhan cn) {
        this.arrCongNhan.add(cn);
    }

    public void themMoiKySu(KySu ks) {
        this.arrKySu.add(ks);
    }

    public void themMoiNhanVien(NhanVien nv) {
        this.arrNhanVien.add(nv);
    }

    /* tim kiem cong nhan, ky su theo ten */
    public ArrayList<CongNhan> timKiemCongNhan(String keySearch) {
        ArrayList<CongNhan> arrSearch = new ArrayList<>();
        for (CongNhan cn : arrSearch) {
            if (cn.getHoTen().toLowerCase().contains(keySearch.toLowerCase())) {
                arrSearch.add(cn);
            }
        }

        return arrSearch;
    }

    public ArrayList<KySu> timKySu(String keySearch) {
        ArrayList<KySu> arrSearch = new ArrayList<>();
        for (KySu ks : arrSearch) {
            if (ks.getHoTen().toLowerCase().contains(keySearch.toLowerCase())) {
                arrSearch.add(ks);
            }
        }

        return arrSearch;
    }

    public ArrayList<NhanVien> timKiemNhanVien(String keySearch) {
        ArrayList<NhanVien> arrSearch = new ArrayList<>();
        for (NhanVien nv : arrSearch) {
            if (nv.getHoTen().toLowerCase().contains(keySearch.toLowerCase())) {
                arrSearch.add(nv);
            }
        }

        return arrSearch;
    }

    /* In thong tin cong nhan, ky su, nhan vien */

    /* Nhap thong tin cong nhan, ky su, nhan vien */

    /* Sa thai cong nhan, ky su, nhan vien */

    /* Tim top 3 luong cao cua cong nhan, ky su, nhan vien */

    /*
     * Tim top 3 tham nien cua Cong nhan, ky su, nhan vien va tang luong 10% cho ho
     */

}
