#include <iostream>
using namespace std;
// 冒泡排序
void bubbleSort(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                // Swap arr[j] and arr[j+1]
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main() {
    int size;
    printf("Enter the size of the array: ");
    scanf("%d", &size);

    int arr[size];
    printf("Enter the elements of the array: ");
    for (int i = 0; i < size; i++) {
        scanf("%d", &arr[i]);
    }

    printf("Array before sorting: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }

    bubbleSort(arr, size);

    printf("\nArray after sorting: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }

}
