#include <iostream>
#include <vector>
#include <algorithm> // Нужен для функции min

using namespace std;

int main() {
    int K, S;
    // Подсказка для ввода количества номиналов K и целевой суммы S
    cout << "Enter K (number of nominals) and S (total sum) with space: ";
    cin >> K >> S;

    // Наш пул монет (список списков, аналог из твоего Python-кода)
    vector<vector<int>> coins_pool;

    for (int i = 0; i < K; i++) {
        int nominal, count;
        // Подсказка для каждой монеты
        cout << "Enter nominal and count for coin " << i + 1 << ": ";
        cin >> nominal >> count;

        vector<int> item;
        item.push_back(nominal);
        item.push_back(count);
        coins_pool.push_back(item);
    }

    // Список, куда мы будем сохранять результаты выдачи
    vector<vector<int>> coins_issued;

    // Жадный алгоритм перебора
    for (int i = 0; i < K; i++) {
        int nominal = coins_pool[i][0]; // Достаем номинал монеты
        int count = coins_pool[i][1];   // Достаем её доступное количество

        int needed = S / nominal; // Сколько монет ХОТЕЛОСЬ БЫ взять (в C++ деление целых чисел всегда целочисленное)
        int taken = min(needed, count); // Берем столько, сколько реально можем себе позволить

        S = S - taken * nominal; // Уменьшаем оставшуюся сумму

        vector<int> item;
        item.push_back(nominal);
        item.push_back(taken);
        coins_issued.push_back(item);
    }

    // Проверяем результат выдачи
    if (S == 0) {
        cout << "--- Result ---" << endl;
        for (int i = 0; i < coins_issued.size(); i++) {
            // Выводим в формате nominal: amount, как просит условие задачи
            cout << coins_issued[i][0] << ": " << coins_issued[i][1] << endl;
        }
    } else {
        // Если сумма не обнулилась, то точный размен невозможен
        cout << "Impossible" << endl;
    }

    return 0;
}
