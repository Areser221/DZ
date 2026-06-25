#include <iostream>
#include <vector>
#include <queue>     // Нужен для работы с очередью queue
#include <algorithm> // Нужен для функции max

using namespace std;

int main() {
    int N, M;
    // Подсказка для ввода количества людей N и связей M
    cout << "Enter N (users) and M (friendships) with space: ";
    cin >> N >> M;

    // Создаем граф в виде массива списков (список смежности)
    // graph[i] будет хранить список всех id друзей для пользователя i
    vector<int> graph[10005];

    for (int i = 0; i < M; i++) {
        int u, v;
        cout << "Enter friendship pair " << i + 1 << " (u v): ";
        cin >> u >> v;
        
        // Так как дружба взаимная, добавляем связь в обе стороны
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    // Массив для отслеживания посещенных людей (изначально все false, то есть 0)
    vector<bool> visited(N, false);

    int comp_cnt = 0;  // Счётчик количества компаний
    int max_size = 0;  // Размер самой большой компании

    // Перебираем каждого пользователя от 0 до N-1
    for (int i = 0; i < N; i++) {
        // Если мы этого человека еще не рассматривали, значит нашли НОВУЮ компанию!
        if (visited[i] == false) {
            comp_cnt = comp_cnt + 1;

            // Создаем очередь для обхода текущей компании друзей
            queue<int> q;
            q.push(i);
            visited[i] = true; // Отмечаем первого участника

            int current_size = 0;

            // Пока в нашей очереди есть люди, которых мы еще не "обработали"
            while (!q.empty()) {
                int current_user = q.front(); // Берем первого человека из очереди
                q.pop();                      // Убираем его из очереди
                current_size = current_size + 1; // Считаем его в размер компании

                // Перебираем всех друзей текущего пользователя
                for (int j = 0; j < graph[current_user].size(); j++) {
                    int neighbor = graph[current_user][j];
                    
                    // Если его друг еще не был ни в одной компании ранее
                    if (visited[neighbor] == false) {
                        visited[neighbor] = true; // Отмечаем его
                        q.push(neighbor);         // Добавляем в очередь на обработку
                    }
                }
            }

            // Когда очередь опустела — компания полностью собрана
            // Проверяем, не больше ли она нашего текущего максимума
            if (current_size > max_size) {
                max_size = current_size;
            }
        }
    }

    // Выводим итоговый ответ
    cout << "--- Result ---" << endl;
    cout << "Total companies: " << comp_cnt << ", Max size: " << max_size << endl;

    return 0;
}
