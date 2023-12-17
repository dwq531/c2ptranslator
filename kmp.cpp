#include <iostream>
#include <cstring>
#include <vector>
using namespace std;
// 生成匹配表
void computeLPSArray(const char* pattern, int patternLength, int* lps) {
    int len = 0;
    int i = 1;
    lps[0] = 0;

    while (i < patternLength) {
        if (pattern[i] == pattern[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
}
// KMP算法
vector<int> kmp(const char* text, const char* pattern) {
    vector<int> positions;
    int textLength = strlen(text);
    int patternLength = strlen(pattern);

    int* lps = new int[patternLength];
    computeLPSArray(pattern, patternLength, lps);

    int i = 0;
    int j = 0;

    while (i < textLength) {
        if (pattern[j] == text[i]) {
            j++;
            i++;
        }

        if (j == patternLength) {
            positions.push_back(i - j);
            j = lps[j - 1];
        } else if (i < textLength && pattern[j] != text[i]) {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }

    delete[] lps;
    return positions;
}

int main() {
    const char* text = "ABABDABACDABABCABAB";
    const char* pattern = "ABABCABAB";
    vector<int> positions = kmp(text, pattern);

    if (positions.empty()) {
        std::cout << "false" << std::endl;
    } else {
        for (int i = 0; i < positions.size(); i++) {
            cout << "Pattern found at index " << positions[i] << std::endl;
        }
    }

    return 0;
}
