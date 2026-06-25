#include <iostream>
#include <vector>
#include <algorithm> // Нужен для функции max

using namespace std;

int main() {
    int N;
    // Подсказка для ввода количества элементов N
    cout << "Enter N (number of elements): ";
    cin >> N;

    // Создаем обычный динамический массив (vector) чисел
    vector<int> x;
    
    // Считываем все элементы массива через пробел
    cout << "Enter " << N << " numbers separated by spaces: ";
    for (int i = 0; i < N; i++) {
        int num;
        cin >> num;
        x.push_back(num); // Добавляем число в массив x
    }

    // Задаем начальные значения для шагов динамики
    // prev2 — максимальная сумма на позапрошлом шаге (для 0 элементов равна 0)
    int prev2 = 0;
    // prev1 — максимальная сумма на прошлом шаге (для 0 элементов тоже 0)
    int prev1 = 0;

    // Последовательно перебираем каждое число из нашего массива x
    for (int i = 0; i < N; i++) {
        int num = x[i];
        
        // Выбираем лучший вариант для текущего числа:
        // Либо берем накопленное у соседа слева (prev1),
        // Либо берем накопленное через один элемент (prev2) + само текущее число
        int current_max = max(prev1, prev2 + num);
        
        // Шагаем вперед для следующего цикла
        prev2 = prev1;
        prev1 = current_max;
    }

    // В переменной prev1 лежит финальный правильный ответ
    cout << "--- Result ---" << endl;
    cout << "Maximum possible sum: " << prev1 << endl;

    return 0;
}
