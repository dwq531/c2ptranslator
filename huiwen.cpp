#include <iostream>
#include <cstring>
using namespace std;
// 判断是否是回文
bool isPalindrome(const char str[]) {
    int start = 0;
    int end = strlen(str) - 1;

    while (start <= end) {
        if (str[start] != str[end]) {
            return false;
        }
        start++;
        end--;
    }

    return true;
}

int main() {
    char input[100];
    float test = 102.329;
    cout << "Enter a string: ";
    cin >> input;

    if (isPalindrome(input)) {
        cout << "The string is a palindrome." << endl;
    } else {
        cout << "The string is not a palindrome." << endl;
    }

    return 0;
}
