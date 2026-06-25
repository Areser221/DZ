#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int N;
    // КРАСИВЫЙ ВЫВОД: подсказываем пользователю, что нужно сделать
    cout << "Enter N: ";
    cin >> N;

    vector<vector<int>> s;

    for (int i = 0; i < N; i++) {
        int start, end;
        // КРАСИВЫЙ ВЫВОД: пишем, какой именно по счету интервал мы ждем
        cout << "Enter start and end " << i + 1 << "with space: ";
        cin >> start >> end;

        if (start < 0 || end < 0) {
            break; 
        }

        vector<int> item;
        item.push_back(end);
        item.push_back(start);
        s.push_back(item);
    }

    sort(s.begin(), s.end());

    int cnt = 0;
    int last = 0;

    for (int i = 0; i < s.size(); i++) {
        int end = s[i][0];
        int start = s[i][1];

        if (start >= last) {
            cnt = cnt + 1;
            last = end;
        }
    }

    // КРАСИВЫЙ ВЫВОД: поясняем, что за число мы вывели в конце
    cout << "Answer: " << cnt << endl;

    return 0;
}
