/* Nhập một số từ bàn phím và kiểm tra nguyên dương, đọc số. */

import java.util.Scanner;

public class bai2 {
    public static void main(String[] args) {
        System.out.println("--===Practice 03===--");
        // Nhap 1 số từ màn hình
        Scanner scanner = new Scanner(System.in);
        System.out.print("Nhap mot so nguyen bat ky: ");
        int iSoVuaNhap = scanner.nextInt();
        kiemTraSoNguyen(iSoVuaNhap);
        System.out.print("Doc so nguyen: ");
        String strDocSO = docSoNguyen(iSoVuaNhap);
        System.out.println(strDocSO);
    }

    static void kiemTraSoNguyen(int iSo) {
        if (iSo > 0) {
            System.out.println("So " + iSo + " la so nguyen duong");
        } else {
            System.out.println("So " + iSo + " la so nguyen am");
        }
    }

    static String docSoNguyen(int iSo) {
        String strChuSo = "";
        switch (iSo) {
            case 1:
                strChuSo = "Mot";
                break;
            case 2:
                strChuSo = "Hai";
                break;
            default:
                strChuSo = "So nay la: " + iSo;
        }
        return strChuSo;
    }
}
