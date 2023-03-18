/* Xay dung chuong trinh quan ly sinh vien:
       Co cac menu sau:
        1. Nhap sinh vien (them moi)
        2. Tim kiem sinh vien theo ho ten hoac CCCD
        3. In thong tin sinh vien
        4. Duoi hoc sinh vien
        5. Thoat chuong trinh
        Va thong bao cho nguoi dung la: Hay nhap mot so tu 1 den 4 de tiep tuc, nhap
        5 exit.
*/

import java.util.ArrayList;
import java.util.Scanner;

public class App {
    public static void main(String[] args) throws Exception {
        System.out.println("Bai 5_1");
        Scanner inScanner = new Scanner(System.in);
        ManageStudent manageStudent = new ManageStudent();
        String strNhap = "";
        do {
            System.out.println("===Quan ly sinh vien===");
            System.out.println("===1. Nhap sinh vien (them moi)===");
            System.out.println("===2. Tim kiem sinh vien theo ho ten hoac CCCD===");
            System.out.println("===3. In thong tin sinh vien===");
            System.out.println("===4. Duoi hoc sinh vien===");
            System.out.println("===5. Thoat chuong trinh===");
            System.out.println("===Hay nhap mot so tu 1 den 4 de tiep tuc===");
            System.out.println("===nhap 5 exit===");
            System.out.println("===Ban chon: ");
            strNhap = inScanner.nextLine();
            switch (strNhap) {
                case "1":
                    System.out.println("---Ban da chon nhap sinh vien");
                    System.out.println("Nhap so sinh vien cua lop: ");
                    int iSoLuongSinhVien = Integer.parseInt(inScanner.nextLine());
                    for (int i = 0; i < iSoLuongSinhVien; i++) {
                        System.out.println("Nhap sinh vien thu: " + (i + 1));
                        Student sv = new Student();
                        System.out.println("Nhap cccd");
                        sv.cccd = inScanner.nextLine();
                        System.out.println("Nhap ho va ten: ");
                        sv.fullName = inScanner.nextLine();
                        System.out.println("Nhap tuoi: ");
                        sv.age = Integer.parseInt(inScanner.nextLine());
                        System.out.println("Nhap ngay sinh: ");
                        sv.dateOfBirth = inScanner.nextLine();
                        System.out.println("Nhap lop hoc: ");
                        sv.className = inScanner.nextLine();

                        System.out.println("========Thong tin sinh vien vua nhap=========");
                        sv.printStudent();
                        // them moi vao danh sach sinh vien
                        manageStudent.themMoiStudent(sv);
                    }
                    break;
                case "2":
                    System.out.println("---Ban da chon In thong tin sinh vien");
                    manageStudent.inDanhSachStudent();
                    break;
                case "3":
                    System.out.println("---Ban da chon Tim kiem sinh vien theo ho ten hoac CCCD");
                    System.out.println("Nhap thong tin muon tim");
                    String keySearch = inScanner.nextLine();
                    ArrayList<Student> arrSearch = manageStudent.searchStudent(keySearch);
                    System.out.println("Danh sach sinh vien tim kiem theo: " + keySearch);
                    for (Student student : arrSearch) {
                        student.printStudent();
                    }
                    break;
                case "4":
                    System.out.println("---Ban da chon Duoi hoc sinh vien");
                    System.out.println("---Nhap cccd cua sinh vien muon duoi hoc:");
                    String strCCCD = inScanner.nextLine();
                    Student svDuoiHoc = manageStudent.timKiemStudent(strCCCD);
                    if (svDuoiHoc != null) {
                        System.out.println("Ban chac chan muon duoi hoc sinh vien: " + svDuoiHoc.fullName + "? (Y/N)");
                        String strConfirm = inScanner.nextLine();
                        if (strConfirm.equalsIgnoreCase("Y")) {
                            manageStudent.duoiHocStudent(svDuoiHoc);
                            System.out.println("Da duoi hoc thanh cong!");
                        }
                        manageStudent.duoiHocStudent(svDuoiHoc);
                    } else {
                        System.out.println("Khong ton tai sinh vien co CCCD la: " + strCCCD);
                    }
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
