import os 
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

model_name_list = [
    'Array',
    'Linked'
]

model_type_list = [
    'array',
    'linked'
]


# system_map = {
#     'ElevatorModel' : ['ElevatorSystem'], 
#     'JavaNioServerSocket3' : ['JavaNioServerSocket3SUT', 'JavaNioServerSocket3SUT.TestClient'], #TODO not sure
#     'SimpleModel' : ['SimpleCounterBES']
# }


csv_path = f'csvs'
img_general_path = f'images'
os.makedirs(csv_path, exist_ok=True)
# os.makedirs(img_general_path, exist_ok=True)

want_to_extract = ['time_taken', 'total_tests', 'failed_tests', 'nc', 'ec', 'total_bc', 'total_ic', 'bc', 'ic']

needed_data_as_table = ['trie_total_path', 'total_nodes', 'total_edges', 'node_covered', 'edge_covered']


# functions:
def get_unique_rows(csv, row_name):
    return csv[row_name].unique()


def bool_to_str(loopOption):
    if loopOption:
        return "no_loops"
    else:
        return "loops"

    
def extract_unique_as_array(csv_file, unique_depths, unique_field, by_field):
    res = []
    for depth in unique_depths:
        list_unique = csv_file[csv_file[unique_field] == depth][by_field].tolist()
#         if len(list_unique) > 1:
#             print("WARNING: one depth has multiple sizes")
        res.append(np.array(list_unique))
    return res


def extract_unique_as_map(csv_file, unique_depths, unique_field, by_field):
    res_map ={}
#     list_data = []
    for depth in unique_depths:
        list_unique = csv_file[csv_file[unique_field] == depth][by_field].tolist()
        list_data = list(set(list_unique))
#         if len(list_data) > 1:
#             print("WARNING: one depth has multiple sizes")
        res_map[depth] = list_data
    return res_map


def print_map(my_map, key_name):
    for k, v in my_map.items():
        print (f'{key_name} {k} --> {v}')

        
def set_subplot_extra_options(ax, d_map):

    ax.set_title(f"{d_map['title']}")
    ax.set_xlabel(f"{d_map['x_label']}")
    ax.set_ylabel(f"{d_map['y_label']}")
    ax.grid(True)
    
#     ax.plt.ylim()([0, 100])
#     ax.set_aspect('equal', adjustable='box')
#     ax.legend()
#     plt.subplots_adjust()

#     ax.plot(x, y, 'o', label=point_label)
#     ax.plot(x, res.intercept + res.slope*x, 'r', label=f'p-value: {res.pvalue:.3e}')
    


def prepare_sub_plot(ax, csv_f, x_name, y_name, unique_list, data_map):
    all_data = extract_unique_as_array(csv_f, unique_list, x_name, y_name)
    labels = unique_list
    bplot1 = ax.boxplot(all_data,
#                          vert=True,  # vertical box alignment
#                          patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
#     set_subplot_extra_options(bplot1)
    set_subplot_extra_options(ax, data_map)
    
#     ymin, ymax = plt.ylim()
#     plt.ylim( 0.5, ymax * 0.5)


def compare_bes_rand_given_y(bes_csv, rand_csv, bes_x_name, rand_x_name, y_common, 
                             bes_unique_list, rand_unique_list, map_bes, map_rand):
    
    fig, axs = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False, squeeze=False, figsize=(14, 5)
                           ,gridspec_kw={'width_ratios': [map_bes['width_ratio'], map_rand['width_ratio']]})
    
#     plt.gca().set_aspect('equal', adjustable='box')

    ax1, ax2 = axs[0][0], axs[0][1]
    
    prepare_sub_plot(ax1, bes_csv, bes_x_name, y_common, bes_unique_list, map_bes)
    prepare_sub_plot(ax2, rand_csv, rand_x_name, y_common, rand_unique_list, map_rand)
    
#     fig.suptitle(f"BES VS RS in terms of {map_bes['y_label']} for {map_bes['model_name']}", y=map_bes['distance_to_figures'])
    
#     fig.set_figwidth(map_bes['width'])
#     fig.set_figheight(map_bes['hight'])
    
    plt.show()
    img_path = os.path.join(img_general_path, f"{map_bes['model_name']}")
    os.makedirs(img_path, exist_ok=True)
    fig.savefig(os.path.join(img_path,
                        f"{map_bes['y_label']}_bes_rand_{map_bes['model_name']}_{map_bes['loopOpt']}.svg"), 
                        format="svg")

    
def get_csv_unique(model_name, loopOpt):  
    bes_csv = pd.read_csv(os.path.join('csvs', f'bes_{model_name}_{bool_to_str(loopOpt)}.csv'))
    random_csv = pd.read_csv(os.path.join('csvs', f'random_{model_name}_{bool_to_str(loopOpt)}.csv'))

    u_bes = get_unique_rows(bes_csv, 'depth')
    u_random = get_unique_rows(random_csv, 'requested_size')

    if len(u_bes) != len(u_random):
        print(f"[WARNING]: not equal number in x_axis, u_bes != u_random")

    # print(random_csv.head(5))
    print(f'u_bes: {u_bes}')
    print(f'u_random: {u_random}')
    
    return (bes_csv, random_csv, u_bes, u_random)





def extract_unique_as_list(csv_file, unique_depths, unique_field, by_field):
    res_list = []
    for depth in unique_depths:
        list_unique = csv_file[csv_file[unique_field]
                               == depth][by_field].tolist()
        list_data = list(set(list_unique))
        # print(list_data)
        res_list.append(list_data[0])
    return res_list


def plot_one_linear(x_ax, y1_ax, y2_ax, data_map):

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.plot(x_ax, y1_ax, 'ko-', label=f'{data_map["y1_label"]}')
    ax.plot(x_ax, y2_ax, 'ro:', label=f'{data_map["y2_label"]}')

    set_subplot_extra_options(ax, data_map)
    # plt.legend(loc="upper left")
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0., handleheight=3) 

    # fig.suptitle(
    #     f"BES VS RS in terms of {data_map['y_bes_label']} for {data_map['model_name']}", y=data_map['distance_to_figures'])

    
    
    plt.xticks(np.arange(min(x_ax), max(x_ax)+1, 1.0))
    


    plt.show()
    img_path = os.path.join(img_general_path, f"{data_map['model_name']}")
    os.makedirs(img_path, exist_ok=True)
    fig.savefig(os.path.join(img_path,
                        f"trie_vs_actual_{data_map['model_name']}_{data_map['loopOpt']}.svg"),
                        format="svg")




def to_latex_compare(title, x, y1, y2):
    data = []
    # print(over_bound_list)
    for i, e in enumerate(x):
        # print(e)
        data.append(f'{e} & {y1[i]} & {y2[i]}  \\\\ \\hline')

    string_data = '\n'.join(data)
    table_total = f'''\\begin{{table}}[{title}]
\\begin{{tabular}}{{|c||c|c|}}
\\hline
& Depth & Total number of tests generated by the trie & Actual number of tests generated by Modbat \\\\ \\hline \\hline
{string_data}
\end{{tabular}}
\end{{table}}'''

    return table_total



































