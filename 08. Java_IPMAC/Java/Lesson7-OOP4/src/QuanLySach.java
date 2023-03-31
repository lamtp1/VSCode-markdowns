import java.util.ArrayList;

// Lớp viết chi tiết cho các hàm mình khai báo trong interface
public class QuanLySach implements iQuanLySach {
    private ArrayList<TaiLieu> arrTaiLieu;

    public QuanLySach() {
        this.arrTaiLieu = new ArrayList<>();
    }

    @Override
    public void themMoiSach(TaiLieu taiLieu) {
        this.arrTaiLieu.add(taiLieu);
    }

    @Override
    public TaiLieu timTaiLieuTheoMa(String maTaiLieu) {
        TaiLieu taiLieu = null;
        for (TaiLieu tLieu : this.arrTaiLieu) {
            if (tLieu.getMaTaiLieu().equalsIgnoreCase(maTaiLieu)) {
                taiLieu = tLieu;
                break;
            }
        }
        return taiLieu;
    }

    @Override
    public void xoaSach(TaiLieu taiLieu) {
        if (taiLieu != null) {
            this.arrTaiLieu.remove(taiLieu);
        }
    }

    @Override
    public ArrayList<TaiLieu> timKiemSach(String loaiTaiLieu) {
        /*
         * 1: tim sach
         * 2: tim bao
         * 3: tim tap chi
         */
        ArrayList<TaiLieu> arrTimKiem = new ArrayList<>();
        for (TaiLieu taiLieu : arrTimKiem) {
            switch (loaiTaiLieu) {
                case "1":
                    // Tim sach
                    if (taiLieu instanceof Sach) {
                        arrTimKiem.add(taiLieu);
                    }
                    break;
                case "2":
                    // Tim bao
                    if (taiLieu instanceof Bao) {
                        arrTimKiem.add(taiLieu);
                    }
                    break;
                default:
                    // Tim tap chi
                    if (taiLieu instanceof TapChi) {
                        arrTimKiem.add(taiLieu);
                    }
                    break;
            }
        }
        return arrTimKiem;
    }

    @Override
    public void inDanhSach(ArrayList<TaiLieu> arrTaiLieu) {

    }

}
