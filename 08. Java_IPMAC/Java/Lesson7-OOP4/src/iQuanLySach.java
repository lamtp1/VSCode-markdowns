import java.util.ArrayList;

public interface iQuanLySach {
    // Khai bao khung chương trình quản lý sách, tất cả các hàm phải có trong chương
    // trình này
    void themMoiSach(TaiLieu taiLieu);

    TaiLieu timTaiLieuTheoMa(String maTaiLieu);

    void xoaSach(TaiLieu taiLieu);

    ArrayList<TaiLieu> timKiemSach(String loaiTaiLieu);

    void inDanhSach(ArrayList<TaiLieu> arrTaiLieu);
}
