public class SoPhuc {

    // khai bao thuoc tinh
    double dPhanThuc;
    double dPhanAo;

    // Hàm tạo mặc định của class trong java:
    SoPhuc() {

    }

    // Tạo một hàm tạo (constructor) có 2 tham số (phần thực và ảo) cho lớp SoPhuc
    SoPhuc(double dA, double dB) {
        dPhanThuc = dA;
        dPhanAo = dB;
    }

    void HienThiSoPhuc() {
        System.out.println("So Phuc a + bi la: " + dPhanThuc + "+" + dPhanAo + "i");
    }
}
