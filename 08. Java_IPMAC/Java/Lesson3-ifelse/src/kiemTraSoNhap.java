import java.util.Scanner;

public class kiemTraSoNhap {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        double number;

        do {
            System.out.print("Nhập một số: ");
            while (!scanner.hasNextDouble()) {
                System.out.println("Đầu vào không hợp lệ. Vui lòng nhập một số.");
                scanner.next();
            }
            number = scanner.nextDouble();
        } while (number <= 0);

        System.out.println("Bạn đã nhập số: " + number);
    }
}
