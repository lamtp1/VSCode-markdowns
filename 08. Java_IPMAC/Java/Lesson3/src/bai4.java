
/* Tính tổng các số chẵn từ 0 đến N */
import java.util.Scanner;

public class bai4 {
    public static void main(String[] args) {
        Scanner nhScanner = new Scanner(System.in);
        System.out.println("Nhap vao mot so nguyen > 0");
        int iN = nhScanner.nextInt();
        while (iN <= 0) {
            System.out.println("Nhap vao mot so nguyen > 0");
            iN = nhScanner.nextInt();
        }
        int TongChan = bai4TinhTong(iN);
        System.out.println("Tong cac so chan tu 0 den " + iN + " la: " + TongChan);
        System.out.println("Trung binh cac so chan tu 0 den " + iN + " la: " + (float) TongChan / ((iN - 2) / 2 + 1));

    }

    static int bai4TinhTong(int in) {
        int iTongChan = 0;
        for (int i = 0; i <= in; i++) {
            if (i % 2 == 0) {
                iTongChan = iTongChan + i;
            }
        }
        return iTongChan;
    }
}
