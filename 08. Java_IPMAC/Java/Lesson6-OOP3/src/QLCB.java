import java.util.ArrayList;
import java.util.Scanner;

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
    public void inCongNhan() {
        for (CongNhan cn : this.arrCongNhan) {
            cn.inCanBo();
        }
    }

    public void inKySu() {
        for (KySu ks : this.arrKySu) {
            ks.inCanBo();
        }

    }

    public void inNhanVien() {
        for (NhanVien nv : this.arrNhanVien) {
            nv.inCanBo();
        }

    }

    /* Nhap thong tin cong nhan, ky su, nhan vien */
    public void nhapCongNhan() {
        Scanner inScanner = new Scanner(System.in);
        for (int i = 1; i <= this.iSoLuongCongNhan; i++) {
            System.out.println("====Nhap cong nhan thu " + i + ":");
            CongNhan cn = new CongNhan();
            System.out.println("Nhap ma cong nhan: ");
            String strMaCongNhan = inScanner.nextLine();
            cn.setMaCanBo(strMaCongNhan);
            System.out.println("Nhap ho va ten: ");
            String strHoTen = inScanner.nextLine();
            cn.setHoten(strHoTen);
            System.out.print("Nhap tuoi: ");
            Integer iTuoi = Integer.parseInt(inScanner.nextLine());
            cn.setTuoi(iTuoi);
            System.out.println("Nhap gioi tinh (0:NAM, 1:NU):");
            String strGioiTinh = inScanner.nextLine();
            switch (strGioiTinh) {
                case "0":
                    cn.setGioiTinh(EnumGioiTinh.NAM);
                    break;
                case "1":
                    cn.setGioiTinh(EnumGioiTinh.NU);
                    break;
                default:
                    cn.setGioiTinh(EnumGioiTinh.CHUA_XAC_DINH);
                    break;
            }
            System.out.println("Nhap dia chi: ");
            String strDiaChi = inScanner.nextLine();
            cn.setDiaChi(strDiaChi);
            System.out.println("Nhap bac cong nhan (1:CAO, 2:TB, 3:THAP): ");
            String strBacCongNhan = inScanner.nextLine();
            switch (strBacCongNhan) {
                case "1":
                    cn.setBacCongNhan(EnumBacCongNhan.CAO);
                    break;
                case "2":
                    cn.setBacCongNhan(EnumBacCongNhan.TRUNGBINH);
                default:
                    cn.setBacCongNhan(EnumBacCongNhan.THAP);
                    break;
            }
            // Them cong nhan vao arrCongNhan:
            this.arrCongNhan.add(cn);
        }

    }

    public void nhapKySu() {
        Scanner inScanner = new Scanner(System.in);
        for (int i = 1; i <= this.iSoLuongKySu; i++) {
            System.out.println("====Nhap Ky Su thu " + i + ":");
            KySu ks = new KySu();
            System.out.println("Nhap ma Ky Su: ");
            String strMaKySu = inScanner.nextLine();
            ks.setMaCanBo(strMaKySu);
            System.out.println("Nhap ho va ten: ");
            String strHoTen = inScanner.nextLine();
            ks.setHoten(strHoTen);
            System.out.print("Nhap tuoi: ");
            Integer iTuoi = Integer.parseInt(inScanner.nextLine());
            ks.setTuoi(iTuoi);
            System.out.println("Nhap gioi tinh (0:NAM, 1:NU):");
            String strGioiTinh = inScanner.nextLine();
            switch (strGioiTinh) {
                case "0":
                    ks.setGioiTinh(EnumGioiTinh.NAM);
                    break;
                case "1":
                    ks.setGioiTinh(EnumGioiTinh.NU);
                    break;
                default:
                    ks.setGioiTinh(EnumGioiTinh.CHUA_XAC_DINH);
                    break;
            }
            System.out.println("Nhap dia chi: ");
            String strDiaChi = inScanner.nextLine();
            ks.setDiaChi(strDiaChi);
            System.out.println("Nhap nganh dao tao Ky Su: ");
            String strNganhDaoTao = inScanner.nextLine();
            ks.setNganhDaoTao(strNganhDaoTao);
            // Them cong nhan vao arrCongNhan:
            this.arrKySu.add(ks);
        }

    }

    public void nhapNhanVien() {
        Scanner inScanner = new Scanner(System.in);
        for (int i = 1; i <= this.iSoLuongNhanVien; i++) {
            System.out.println("====Nhap Nhan Vien thu " + i + ":");
            NhanVien nv = new NhanVien();
            System.out.println("Nhap ma Nhan vien: ");
            String strMaNhanVien = inScanner.nextLine();
            nv.setMaCanBo(strMaNhanVien);
            System.out.println("Nhap ho va ten: ");
            String strHoTen = inScanner.nextLine();
            nv.setHoten(strHoTen);
            System.out.print("Nhap tuoi: ");
            Integer iTuoi = Integer.parseInt(inScanner.nextLine());
            nv.setTuoi(iTuoi);
            System.out.println("Nhap gioi tinh (0:NAM, 1:NU):");
            String strGioiTinh = inScanner.nextLine();
            switch (strGioiTinh) {
                case "0":
                    nv.setGioiTinh(EnumGioiTinh.NAM);
                    break;
                case "1":
                    nv.setGioiTinh(EnumGioiTinh.NU);
                    break;
                default:
                    nv.setGioiTinh(EnumGioiTinh.CHUA_XAC_DINH);
                    break;
            }
            System.out.println("Nhap dia chi: ");
            String strDiaChi = inScanner.nextLine();
            nv.setDiaChi(strDiaChi);
            System.out.println("Nhap cong viec cua Nhan Vien: ");
            String strCongViec = inScanner.nextLine();
            nv.setCongViec(strCongViec);
            // Them cong nhan vao arrCongNhan:
            this.arrNhanVien.add(nv);
        }

    }
    /* Sa thai cong nhan, ky su, nhan vien */

    /* Tim top 3 luong cao cua cong nhan, ky su, nhan vien */

    /*
     * Tim top 3 tham nien cua Cong nhan, ky su, nhan vien va tang luong 10% cho ho
     */

}
