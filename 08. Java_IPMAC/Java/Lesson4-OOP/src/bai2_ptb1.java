import java.util.Scanner;

public class bai2_ptb1 {
    public static void main(String[] args) {
        System.out.println("Giai phuong trinh bac 1");
        Scanner inScanner = new Scanner(System.in);
        System.out.println("=====Nhap A:");
        double A = inScanner.nextDouble();
        System.out.println("=====Nhap B:");
        double B = inScanner.nextDouble();
        if (A == 0 && B == 0) {
            System.out.println("Phuong tirnh vo so nghiem");
        } else if (A == 0 && B != 0) {
            System.out.println("Phuong tirnh vo nghiem");
        } else {
            ptb1 pt1 = new ptb1(A, B);
            System.out.println("Phuong trinh " + A + "X " + "+ " + B + "=0 co nghiem la:" + pt1.dX);
        }
    }
}
