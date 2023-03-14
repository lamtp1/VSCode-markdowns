/* viết chương trình để nhập một số nguyên, tìm kết quả phép nhân của số đó với các số từ 
1 đến 20, sau đó in kết quả ra màn hình */

import java.util.Scanner;

public class bai5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Nhap mot so nguyen: ");
        int x = scanner.nextInt();
        int i = 1;
        while (i <= 20) {
            int result = i * x;
            System.out.println(x + "x" + i + " = " + result);
            i++;
        }
    }
}
