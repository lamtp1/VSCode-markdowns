public class Student {
    String fullName; // Ho ten day du
    String className; // Ten lop hoc
    Integer age; // Tuoi
    String dateOfBirth; // Ngay sinh: DD/MM/YYYY
    String cccd; // Can cuoc

    void printStudent() {
        System.out.println("Ho ten: " + fullName + "; Lop hoc: " + className + "; Tuoi: " + age + "; Nam sinh: "
                + dateOfBirth + "; CCCD: " + cccd);
    }
}
