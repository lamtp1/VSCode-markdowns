/* Kiểm tra có phải là cạnh tam giác */

import java.util.Scanner;

public class bai3 {
    public static void main(String[] args) {
        System.out.println("kiem tra 3 canh tam giac");
        Scanner nhap = new Scanner(System.in);
        System.out.print("Nhap so A: ");
        double dA = nhap.nextDouble();
        System.out.print("Nhap so B: ");
        double dB = nhap.nextDouble();
        System.out.print("Nhap so C: ");
        double dC = nhap.nextDouble();
        boolean isTamGiac = kiemTraLaCanhCuaTamGiac(dA, dB, dC);
        System.out.println(isTamGiac);
        if (isTamGiac) {
            System.out.println("ba so A, B, C la canh tam giac");
        } else {
            System.out.println("ba so A, B, C khong phai canh tam giac");
        }
    }

    static boolean kiemTraLaCanhCuaTamGiac(double dA, double dB, double dC) {
        ;
        boolean isLaCanhTamGiac = false;
        if (dA + dB > dC && dA + dC > dB && dB + dC > dA) {
            isLaCanhTamGiac = true;
        }
        return isLaCanhTamGiac;
    }
}