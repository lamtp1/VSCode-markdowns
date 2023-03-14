public class BubbleSort {
    public static void main(String[] args) {
        int[] numbers = { 7, 4, 20, 8, 5, 9, 3, 12, 13, 6 };

        // Call the bubbleSort method to sort the array
        bubbleSort(numbers);

        // Print the sorted array
        for (int i = 0; i < numbers.length; i++) {
            System.out.print(numbers[i] + " ");
        }
    }

    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap arr[j] and arr[j+1]
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}
