#include <iostream>
#include <vector>
#include <algorithm> // Нужен для работы sort

using namespace std;

int main() {
    int V, E;
    // Подсказка для ввода количества вершин V и ребер E
    cout << "Enter V (vertices) and E (edges) with space: ";
    cin >> V >> E;

    // Список всех ребер графа (аналог списка списков из Python)
    vector<vector<int>> edges;

    for (int i = 0; i < E; i++) {
        int u, v, w;
        cout << "Enter edge " << i + 1 << " (u v weight): ";
        cin >> u >> v >> w;

        // Важная деталь: кладем ВЕС (w) на первое место!
        // Благодаря этому стандартный sort() отсортирует ребра от легких к тяжелым.
        vector<int> item;
        item.push_back(w);
        item.push_back(u);
        item.push_back(v);
        edges.push_back(item);
    }

    // Сортируем все ребра по возрастанию веса
    sort(edges.begin(), edges.end());

    // Создаем список цветов для вершин. Изначально цвет равен номеру вершины.
    vector<int> color;
    for (int i = 0; i < V; i++) {
        color.push_back(i);
    }

    int mst_weight = 0; // Сюда будем суммировать вес дерева

    // Проходим по всем отсортированным ребрам
    for (int i = 0; i < E; i++) {
        int w = edges[i][0]; // Вес ребра
        int u = edges[i][1]; // Вершина u
        int v = edges[i][2]; // Вершина v

        // Если цвета вершин разные, значит они еще не соединены и цикла НЕ будет!
        if (color[u] != color[v]) {
            mst_weight = mst_weight + w; // Забираем этот вес в ответ

            int old_color = color[v];
            int new_color = color[u];

            // Перекрашиваем все вершины старого цвета в новый (объединяем компоненты)
            for (int j = 0; j < V; j++) {
                if (color[j] == old_color) {
                    color[j] = new_color;
                }
            }
        }
    }

    // Выводим итоговый суммарный вес минимального остовного дерева
    cout << "--- Result ---" << endl;
    cout << "Total weight of MST: " << mst_weight << endl;

    return 0;
}
