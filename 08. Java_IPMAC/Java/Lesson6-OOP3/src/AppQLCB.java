import java.security.interfaces.ECKey;
import java.util.ArrayList;
import java.util.Scanner;

import javax.lang.model.element.Element;

public class AppQLCB {
    public static void main(String[] args) {
        System.out.println("===CHUONG TRINH AppQLCB===");
        Scanner inScanner = new Scanner(System.in);
        QuanLyCanBo qLyCanBo = new QuanLyCanBo();

        ArrayList<CanBo> arr = new ArrayList<>();
        arr.add(new CanBo());
        QuanLyCanBo quanLyCanBo1 = new QuanLyCanBo(arr);

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
                    qLyCanBo.inDanhSachCanBo(qLyCanBo.getArrCanBo());
                    break;
                case "3":
                    System.out.println("---Ban da chon Tim kiem theo ho ten");
                    System.out.println("Nhap thong tin tim kiem: ");
                    String strHoTen = inScanner.nextLine();
                    ArrayList<CanBo> arrTimKiem = qLyCanBo.timKiemCanBo(strHoTen);
                    if (arrTimKiem.size() > 0) {
                        System.out.println("Danh sach can bo thoa man: ");
                        qLyCanBo.inDanhSachCanBo(arrTimKiem);
                    } else {
                        System.out.println("Khong ton tai can bo thoa man dieu kien!!!");
                    }

                    break;
                case "4":
                    System.out.println("---Ban da chon Sa thai can bo");
                    System.out.println("Nhap ma can bo can sa thai: ");
                    String strMaCanBo = inScanner.nextLine();
                    CanBo canBo = qLyCanBo.timCanBoTheoMa(strMaCanBo);
                    if (canBo != null) {
                        System.out.println("Thong tin can bo co ma la " + strMaCanBo + ": ");
                        canBo.inCanBo();
                        System.out.println("Ban co muon sa thai can bo nay khong?(y/n):");
                        String strConfirm = inScanner.nextLine();
                        if (strConfirm.equalsIgnoreCase("y")) {
                            qLyCanBo.saThaiCanBo(canBo);
                        }
                        System.out.println("Danh sach can bo sau khi sa thai:");
                        qLyCanBo.inDanhSachCanBo(qLyCanBo.getArrCanBo());
                    } else {
                        System.out.println("Khong ton tai can bo thoa man dieu kien!!!");
                    }
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
