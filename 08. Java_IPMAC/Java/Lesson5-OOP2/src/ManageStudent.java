import java.util.ArrayList;

public class ManageStudent {
    ArrayList<Student> arrSinhVien;

    ManageStudent() {
        arrSinhVien = new ArrayList<>();
    }

    public void themMoiStudent(Student sv) {
        arrSinhVien.add(sv);
        System.out.println("Da them thanh cong 01 sinh vien");
        sv.printStudent();
    }

    public void duoiHocStudent(Student sv) {
        arrSinhVien.remove(sv);
        System.out.println("Da duoi hoc 01 sinh vien");
        sv.printStudent();
    }

    public Student timKiemStudent(String strCCCD) {
        Student sv = null;
        for (int i = 0; i < arrSinhVien.size(); i++) {
            if (arrSinhVien.get(i).cccd.equals(strCCCD)) {
                sv = arrSinhVien.get(i);
                break;
            }
        }
        return sv;
    }

    public ArrayList<Student> searchStudent(String keySearch) {
        // Kiem tra cccd hoac fullname co chua ky tu keysearch thi add vao
        // ArrayList<Student>
        ArrayList<Student> arrSinhVienSearch = new ArrayList<>();
        for (int i = 0; i < arrSinhVien.size(); i++) {
            if (arrSinhVien.get(i).cccd.toUpperCase().contains(keySearch.toUpperCase()) ||
                    arrSinhVien.get(i).fullName.toUpperCase().contains(keySearch.toUpperCase())) {
                arrSinhVienSearch.add(arrSinhVien.get(i));
            }
        }

        return arrSinhVienSearch;
    }

    public void inDanhSachStudent() {
        for (int i = 0; i < arrSinhVien.size(); i++) {
            Student sv = arrSinhVien.get(i);
            sv.printStudent();
        }
    }
}
