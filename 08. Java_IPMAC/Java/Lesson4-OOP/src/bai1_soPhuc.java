import java.util.Scanner;

public class bai1_soPhuc {
    public static void main(String[] args) {
        System.out.println("Lesson4-OOP");

        // Tạo một số phức:
        SoPhuc soPhucA = new SoPhuc(2, 3);
        soPhucA.HienThiSoPhuc();

        // Nhập số phức 1:
        Scanner inputScanner = new Scanner(System.in);
        System.out.println("Nhap so phuc thu 1: ");
        System.out.println("---Nhap phan thuc: ");
        double dPhanThuc1 = inputScanner.nextDouble();
        System.out.println("---Nhap phan ao: ");
        double dPhanAo1 = inputScanner.nextDouble();
        SoPhuc soPhuc1 = new SoPhuc(dPhanThuc1, dPhanAo1);
        soPhuc1.HienThiSoPhuc();

        // Nhập số phức 2:
        System.out.println("Nhap so phuc thu 2: ");
        System.out.println("---Nhap phan thuc: ");
        double dPhanThuc2 = inputScanner.nextDouble();
        System.out.println("---Nhap phan ao: ");
        double dPhanAo2 = inputScanner.nextDouble();
        SoPhuc soPhuc2 = new SoPhuc(dPhanThuc2, dPhanAo2);
        soPhuc2.HienThiSoPhuc();

        // Tổng 2 số phức:
        System.out.println("Tong 2 so phuc la: ");
        SoPhuc soPhucTong = tongSoPhuc(soPhuc1, soPhuc2);
        soPhucTong.HienThiSoPhuc();
    }

    // Cộng số phức:
    static SoPhuc tongSoPhuc(SoPhuc soPhuc1, SoPhuc soPhuc2) {
        SoPhuc soPhucTong = new SoPhuc();
        soPhucTong.dPhanThuc = soPhuc1.dPhanThuc + soPhuc2.dPhanThuc;
        soPhucTong.dPhanThuc = soPhuc1.dPhanAo + soPhuc2.dPhanAo;
        return soPhucTong;
    }
}
