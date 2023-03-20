import java.util.Scanner;

public class AppQLCB {
    public static void main(String[] args) {
        System.out.println("===CHUONG TRINH AppQLCB===");
        Scanner inScanner = new Scanner(System.in);
        QuanLyCanBo qLyCanBo = new QuanLyCanBo();
        // Xây dựng Menu quản lý cán bộ
        String strNhap = "";
        do {
            System.out.println("==Menu chuong trinh Quan ly can bo====");
            System.out.println("====1. Nhap can bo (them moi)====");
            System.out.println("====2. In thong tin can bo====");
            System.out.println("====3. Tim kiem theo ho ten====");
            System.out.println("====4. Sa thai can bo====");
            System.out.println("====5. Thoat chuong trinh====");
            System.out.println("====Hay nhap so tu 1 -> 4 de tiep tuc====");
            System.out.println("====Nhap 5 de thoat====");
            System.out.println("====Ban chon:");
            strNhap = inScanner.nextLine();
            switch (strNhap) {
                case "1":
                    System.out.println("---Ban da chon Nhap can bo (them moi)");
                    qLyCanBo.themCanBo();
                    break;
                case "2":
                    System.out.println("---Ban da chon IN thong tin can bo");
                    qLyCanBo.inDanhSachCanBo();
                    break;
                case "3":
                    System.out.println("---Ban da chon Tim kiem theo ho ten");
                    break;
                case "4":
                    System.out.println("---Ban da chon Sa thai can bo");
                    break;
                case "5":
                    System.out.println("---Cam on da su dung chuong trinh!");
                    break;
                default:
                    System.out.println("---Ban chi duoc nhap gia tri tu 1->5");
                    break;
            }
        } while (!strNhap.equals("5"));
    }
}
