public class Comment {
    public static void main(String[] args) {
        // Outer loop
        int[][] a = { { 1, 2, 4 }, { 2, 4, 7 }, { 4, 6, 6 } };
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < a[i].length; j++) {
                System.out.println(a[i][j]);
                if (a[1][2] == 7) {
                    break;
                }
            }
        }
    }
}