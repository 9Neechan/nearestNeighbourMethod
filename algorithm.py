from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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


def add_next_neighbor(path, ind, all_paths, graph): # not ok
    """Добавляет все возможные ветки путей"""
    new_g = zero_v_vert(path, graph)
    min_s, list_min_s = find_smallest_el_in_row(new_g[path[1][ind-1]])

    save_path = path[1][:]
    if len(list_min_s) != 0:
        path[0] += min_s
        path[1].append(list_min_s[0])

        if len(list_min_s) > 1:
            for i in range(1, len(list_min_s)):
                a = save_path[:]
                a.append(list_min_s[i])
                all_paths.append([path[0], a])


def zero_v_vert(path, graph): # not ok
    """Обнуляет вертикальные столбцы в матрице graph по индексам из path"""
    '''
    graph = [
        # [a, b, c, d, f, g] в
        [0, 3, 0, 0, 1, 0],  # a из
        [3, 0, 8, 0, 0, 3],  # b
        [0, 3, 0, 1, 0, 1],  # c
        [0, 0, 8, 0, 1, 0],  # d
        [3, 0, 0, 3, 0, 0],  # f
        [3, 3, 3, 5, 4, 0]  # g
    ]'''
    leng = len(graph[0])
    for i in range(leng):
        if i in path[1]:
            for j in range(leng):
                graph[j][i] = 0
    return graph


def create_graph_struct(graph):
    G = nx.MultiDiGraph()
    elist = []
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] != 0 and i != j:
                G.add_edge(f'{i}', f'{j}', weight=graph[i][j])
    return G


def draw_graph(im_arr, paths_arr, graph):
    # рисуем и сохраняем исходный граф
    G = create_graph_struct(graph)
    snapshot_name = "pictures/initial.png"
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    #for edge in G.edges(data=True): edge[2]['label'] = edge[2]['weight']
    nx.draw(G, with_labels=True, node_size=80, alpha=0.5, linewidths=10)

    plt.savefig(snapshot_name, dpi=70, bbox_inches='tight')
    im_arr.append(snapshot_name)

    plt.close()

    for i in range(len(paths_arr)):
        snapshot_name = f"pictures/{i}.png"
        path = f'{str(paths_arr[i][0])}-{str(paths_arr[i][1])}-{str(paths_arr[i][2])}-{str(paths_arr[i][3])}-' \
               f'{str(paths_arr[i][4])}-{str(paths_arr[i][5])}'
        pos = nx.spring_layout(G, seed=7)

        data = [[], []]
        e_higlight = []

        for i in range(len(paths_arr[0])):
            data[0].append(i)
            if i == len(paths_arr[0])-1:
                data[1].append(0)
            else:
                data[1].append(i+1)

        #for (u, v, d) in G.edges(data=True):
            #if data[0][data.index(v)] == u:
                #e_higlight.append((u, v))

        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        plt.text(-1.5, 1, f'Путь: {path}')

        df = pd.DataFrame({'from': data[0], 'to': data[1]})
        G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.MultiGraph())
        nx.draw(G, with_labels=True, node_size=80, alpha=0.5, linewidths=10)
        nx.draw_networkx_edges(G, pos, edgelist=e_higlight, width=6)
        plt.savefig(snapshot_name, dpi=70, bbox_inches='tight')
        im_arr.append(snapshot_name)

        plt.close()
    plt.close()


def closest_neighbor_method(graph):
    '''
    graph = [
        # [a, b, c, d, f, g] в
        [0, 3, 0, 0, 1, 0],  # a из
        [3, 0, 8, 0, 0, 3],  # b
        [0, 3, 0, 1, 0, 1],  # c
        [0, 0, 8, 0, 1, 0],  # d
        [3, 0, 0, 3, 0, 0],  # f
        [3, 3, 3, 5, 4, 0]   # g
    ]'''

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
        if len(all_paths[i][1]) == len(graph) and graph[all_paths[i][1][len(graph)-1]][all_paths[i][1][0]] != 0:
            print(i)
            all_paths[i][0] += graph[all_paths[i][1][len(graph)-1]][all_paths[i][1][0]]
            if all_paths[i][0] < best_len:
                best_len = all_paths[i][0]
        else:
            mas_del.append(all_paths[i])

    for l in mas_del:
        all_paths.remove(l)

    print(best_len)
    for el in all_paths:
        print(el)
        if el[0] == best_len:
            best_paths.append(el[1])

    print('best paths')
    print('len = ', best_len)
    for el in best_paths:
        print(el)

    data = pd.DataFrame(graph)
    #data.columns = ['0', '1', '2', '3', '4', '5']
    #data.index = ['0', '1', '2', '3', '4', '5']

    img_arr = []
    draw_graph(img_arr, best_paths, graph)

    return best_len, best_paths


#closest_neighbor_method()