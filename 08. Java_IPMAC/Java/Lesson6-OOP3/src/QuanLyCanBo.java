import java.util.ArrayList;
import java.util.Scanner;

public class QuanLyCanBo {
    private ArrayList<CanBo> arrCanBo = new ArrayList<>();

    QuanLyCanBo() {
        if (this.arrCanBo == null) {
            this.arrCanBo = new ArrayList<>();
        }
    }

    QuanLyCanBo(ArrayList<CanBo> _arrCanBo) {
        this.arrCanBo = _arrCanBo;
    }

    public void setArrCanBo(ArrayList<CanBo> _arrCanBo) {
        this.arrCanBo = _arrCanBo;
    }

    public ArrayList<CanBo> getArrCanBo() {
        return this.arrCanBo;
    }

    /* Thêm mới cán bộ */
    public void themCanBo() {
        CanBo cb = null;
        System.out.println("===Ban chon loai can bo(CN:Cong nhan,KS:Ky su):");
        Scanner inScanner = new Scanner(System.in);
        String strLoaiCanBo = inScanner.nextLine();
        switch (strLoaiCanBo) {
            case "CN":
                cb = new CongNhan();
                break;
            case "KS":
                cb = new KySu();
                break;
            default:
                cb = new NhanVien();
                break;
        }
        System.out.println("Nhap ma nhan vien:");
        String strMaNhanVien = inScanner.nextLine();
        cb.setMaCanBo(strMaNhanVien);
        System.out.println("Nhap ho ten:");
        String strHoTen = inScanner.nextLine();
        cb.setHoten(strHoTen);
        System.out.println("Nhap Tuoi:");
        Integer iTuoi = Integer.parseInt(inScanner.nextLine());
        cb.setTuoi(iTuoi);
        System.out.println("Nhap gioi tinh (0:NAM, 1:NU):");
        String strGioiTinh = inScanner.nextLine();
        switch (strGioiTinh) {
            case "0":
                cb.setGioiTinh(EnumGioiTinh.NAM);
                break;
            case "1":
                cb.setGioiTinh(EnumGioiTinh.NU);
                break;
            default:
                cb.setGioiTinh(EnumGioiTinh.CHUA_XAC_DINH);
                break;
        }
        System.out.println("Nhap dia chi: ");
        String strDiaChi = inScanner.nextLine();
        cb.setDiaChi(strDiaChi);
        if (cb instanceof CongNhan) {
            System.out.println("Nhap bac cong nhan(0:CAO,1:TRUNGBINH):");
            String strBacCongNhan = inScanner.nextLine();
            switch (strBacCongNhan) {
                case "0":
                    ((CongNhan) cb).setBacCongNhan(EnumBacCongNhan.CAO);
                    break;
                case "1":
                    ((CongNhan) cb).setBacCongNhan(EnumBacCongNhan.TRUNGBINH);
                    break;
                default:
                    ((CongNhan) cb).setBacCongNhan(EnumBacCongNhan.THAP);
                    break;
            }
        } else if (cb instanceof KySu) {
            System.out.println("Nhap nganh dao tao:");
            String strNganhDaoTao = inScanner.nextLine();
            ((KySu) cb).setNganhDaoTao(strNganhDaoTao);
        } else {
            System.out.println("Nhap cong viec cua nhan vien:");
            String strCongViec = inScanner.nextLine();
            ((NhanVien) cb).setCongViec(strCongViec);
        }
        // thêm vào arrCanBo
        this.arrCanBo.add(cb);
    }

    /* In cán bộ */
    public void inDanhSachCanBo(ArrayList<CanBo> arrCanBoIn) {
        for (CanBo cb : arrCanBoIn) {
            if (cb instanceof CongNhan) {
                CongNhan cn = (CongNhan) cb;
                cn.inCanBo(); // gọi hàm incanbo của class CongNhan
                System.out.println("; Loai can bo: CN");
            } else if (cb instanceof KySu) {
                KySu ks = (KySu) cb;
                ks.inCanBo();// gọi hàm incanbo của class KySu
                System.out.println("; Loai can bo: KS");
            } else {
                NhanVien nv = (NhanVien) cb;
                nv.inCanBo(); // gọi hàm incanbo của class NhanVien)cb
                System.out.println("; Loai can bo: NV");
            }
        }
    }

    /* Tìm kiếm cán bộ theo họ tên, không phân biệt hoa thường */
    public ArrayList<CanBo> timKiemCanBo(String strHoTen) {
        ArrayList<CanBo> arrTimKiem = new ArrayList<>();
        for (CanBo canBo : this.arrCanBo) {
            if (canBo.getHoTen().toUpperCase().contains(strHoTen.toUpperCase())) {
                arrTimKiem.add(canBo);
            }
        }

        return arrTimKiem;
    }

    /* Sa thải cán bộ */
    /*--B1.Tìm kiếm cán bộ theo CCCD hoặc Mã */
    public CanBo timCanBoTheoMa(String maCanBo) {
        CanBo cb = null;
        for (CanBo canBo : this.arrCanBo) {
            if (canBo.getMaCanBo().equalsIgnoreCase(maCanBo)) {
                cb = canBo;
                break;
            }
        }
        return cb;
    }

    /*--B2.Tìm kiếm xong thì mới sa thải, tức là remove cán bộ khởi arrCanBo */
    public void saThaiCanBo(CanBo canBo) {
        if (canBo != null) {
            this.arrCanBo.remove(canBo);
        }
    }

}
