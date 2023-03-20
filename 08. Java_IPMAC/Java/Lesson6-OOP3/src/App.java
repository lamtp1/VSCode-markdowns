import java.util.Scanner;
// import java.util.ArrayList;

public class App {
    public static void main(String[] args) throws Exception {
        System.out.println("CHUONG TRINH QUAN LY CAN BO");
        Scanner inScanner = new Scanner(System.in);
        System.out.println("Nhap so luong cong nhan: ");
        Integer iSoCongNhan = Integer.parseInt(inScanner.nextLine());
        System.out.println("Nhap so luong Ky Su: ");
        Integer iSoKySu = Integer.parseInt(inScanner.nextLine());
        System.out.println("Nhap so luong Nhan Vien: ");
        Integer iSoNhanVien = Integer.parseInt(inScanner.nextLine());

        // khoi tao quan ly can bo
        QLCB qlcb = new QLCB(iSoCongNhan, iSoKySu, iSoNhanVien);
        String strNhap = "";
        do {
            System.out.println("===Quan ly sinh vien===");
            System.out.println("===1. Nhap can bo===");
            System.out.println("===2. In thong tin can bo===");
            System.out.println("===3. Tim kiem ho va ten===");
            System.out.println("===4. Sa thai can bo===");
            System.out.println("===5. Thoat chuong trinh===");
            System.out.println("===Hay nhap mot so tu 1 den 4 de tiep tuc===");
            System.out.println("===nhap 5 exit===");
            System.out.println("===Ban chon: ");
            strNhap = inScanner.nextLine();
            switch (strNhap) {
                case "1":
                    System.out.println("---Ban da chon Nhap can bo");
                    System.out.println("===Nhap Cong Nhan: ");
                    qlcb.nhapCongNhan();
                    System.out.println("===Nhap Ky Su: ");
                    qlcb.nhapKySu();
                    System.out.println("===Nhap Nhan Vien; ");
                    qlcb.nhapNhanVien();
                    break;
                case "2":
                    System.out.println("---Ban da chon In thong tin can bo");
                    System.out.println("====In thong tin Cong Nhan: ");
                    qlcb.inCongNhan();
                    System.out.println("====In thong tin Ky Su: ");
                    qlcb.inKySu();
                    System.out.println("====In thong tin Nhan Vien: ");
                    qlcb.inNhanVien();
                    break;
                case "3":
                    System.out.println("---Ban da chon Tim kiem ho va ten");
                    break;
                case "4":
                    System.out.println("---Ban da chon Sa thai can bo");
                    break;
                case "5":
                    System.out.println("---Cam on da su dung chuong trinh!");
                    break;
                default:
                    System.out.println("---Ban chi duoc nhap gia tri tu 1 -> 5");
                    break;
            }
        } while (!strNhap.equals("5"));
    }
}
