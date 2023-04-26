import matplotlib.pyplot as plt
import networkx as nx


def find_smallest_el_in_row(row):
    """Находит значения минимальных элементов в массиве и список их индексов"""
    min_el = 1000
    list = []
    for i in range(len(row)):
        if min_el > row[i] != 0:
            min_el = row[i]
            list = [i]
        elif row[i] == min_el:
            list.append(i)
    return min_el, list


def create_start_paths(graph):
    """Cоздает массив со всеми возможными началами путей обхода"""
    all_paths = []
    for i in range(len(graph)):
        all_paths.append([0, [i]])
    return all_paths


def add_next_neighbor(path, ind, all_paths, graph):
    """Добавляет все возможные ветки путей"""
    new_g = zero_v_vert(path, graph)
    min_s, list_min_s = find_smallest_el_in_row(new_g[path[1][ind - 1]])

    save_path = path[1][:]
    if len(list_min_s) != 0:
        path[0] += min_s
        path[1].append(list_min_s[0])

        if len(list_min_s) > 1:
            for i in range(1, len(list_min_s)):
                a = save_path[:]
                a.append(list_min_s[i])
                all_paths.append([path[0], a])


def zero_v_vert(path, graph):
    """Обнуляет вертикальные столбцы в матрице graph по индексам из path"""
    leng = len(graph[0])
    for i in range(leng):
        if i in path[1]:
            for j in range(leng):
                graph[j][i] = 0
    return graph


def create_multigraph_struct(graph):
    G = nx.MultiDiGraph()
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] != 0 and i != j:
                G.add_edge(f'{i}', f'{j}', weight=graph[i][j])
    return G


def create_graph_struct(path_arr, graph):
    G = nx.DiGraph()
    data = []
    for j in range(len(path_arr)):
        if j + 1 < len(path_arr):
            data.append(path_arr[j + 1])
    data.append(path_arr[0])
    for i in range(len(path_arr)):
        G.add_edge(f'{path_arr[i]}', f'{data[i]}', weight=graph[path_arr[i]][data[i]])
    return G


def make_plt(flag, path_arr, graph, i):
    pos = {'0': [0, 0.25],
           '1': [-0.55, 0.25],
           '2': [-0.55, -0.4],
           '3': [0.2, -0.5],
           '4': [0.45, 0],
           '5': [-0.15, -0.0775903]}
    path = ''

    if flag == 'multi':
        G = create_multigraph_struct(graph)
        snapshot_name = "pictures/initial.png"
    else:
        G = create_graph_struct(path_arr, graph)
        snapshot_name = f"pictures/{i}.png"
        path = f'{str(path_arr[0])}-{str(path_arr[1])}-' \
               f'{str(path_arr[2])}-{str(path_arr[3])}-' \
               f'{str(path_arr[4])}-{str(path_arr[5])}'

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='green', alpha=0.6)
    # edges
    nx.draw_networkx_edges(G, pos, width=2)
    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    if flag == "basic":
        # edge weight labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.title(f'Путь: {path}')
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    plt.savefig(snapshot_name, dpi=50, bbox_inches='tight')
    plt.close()


def draw_graph(paths_arr, graph):
    """Визуализация графов"""

    flag = 'multi'
    make_plt(flag, paths_arr[0], graph, 0)

    # рисуем графы наикратчайших гамильтоновых циклов
    for i in range(len(paths_arr)):
        flag = 'basic'
        make_plt(flag, paths_arr[i], graph, i)


def closest_neighbor_method(graph):
    # создаем массив со всеми возможными началами путей обхода
    all_paths = create_start_paths(graph)

    # каждый путь продолжаем до конца
    for j in range(1, len(graph)):
        for i in range(len(all_paths)):
            deep_graph = [x[:] for x in graph]
            add_next_neighbor(all_paths[i], j, all_paths, deep_graph)

    # удаляем пути, где пройдены не все вершины, которые не явл циклами и ищем кратчайшие
    best_paths = []
    best_len = 1000
    mas_del = []
    for i in range(len(all_paths)):
        if len(all_paths[i][1]) == len(graph) and \
                graph[all_paths[i][1][len(graph) - 1]][all_paths[i][1][0]] != 0:
            print(i)
            all_paths[i][0] += graph[all_paths[i][1][len(graph) - 1]][all_paths[i][1][0]]
            if all_paths[i][0] < best_len:
                best_len = all_paths[i][0]
        else:
            mas_del.append(all_paths[i])

    for l in mas_del:
        all_paths.remove(l)

    print('all paths')
    for el in all_paths:
        print(el)
        if el[0] == best_len:
            best_paths.append(el[1])

    print('best paths')
    print('len = ', best_len)
    for el in best_paths:
        print(el)

    draw_graph(best_paths, graph)

    return best_len, best_paths

# closest_neighbor_method()
