import os 
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

model_name_list = [
    'ElevatorModel',
    'JavaNioServerSocket3'
     , 'SimpleModel'
]

system_map = {
    'ElevatorModel' : ['ElevatorSystem'], 
    'JavaNioServerSocket3' : ['JavaNioServerSocket3SUT', 'JavaNioServerSocket3SUT.TestClient'], #TODO not sure
    'SimpleModel' : ['SimpleCounterBES']
}

csv_path = f'csvs'
img_general_path = f'images'
os.makedirs(csv_path, exist_ok=True)
# os.makedirs(img_general_path, exist_ok=True)


def list_dir(path):
    return [p for p in os.listdir(path) if p[0] != '.']

def join_path(*paths):
    return os.path.join(*paths)




def filter_frame(csv_file, status, data_type):
    filtered = csv_file[csv_file['status'] == status][data_type]
    return filtered

def filter_frame_array(csv_file, status, data_type):
    return filter_frame(csv_file, status, data_type).to_numpy()


def filter_desired_m_by_list(csv_file, desired_mutants,creteria ):
    only_desired_mutant_df = csv_file[csv_file['mutant_number'].isin(desired_mutants)]
    desired_c_list = only_desired_mutant_df[creteria].tolist()
    
    print(f' old desired_list: {desired_c_list}')
    return desired_c_list


def filter_desired_m_and_fix(csv_file, desired_mutants, creteria, otherwise_value, timeout):
    
    existed_mutants_list = csv_file['mutant_number'].tolist()
    desired_c_list = []
    timeout_list = []
    for m in desired_mutants:
        if int(m) in existed_mutants_list:
            c = csv_file[csv_file['mutant_number'] == int(m)][creteria].values[0]
            desired_c_list.append(c)
            timeout_list.append(0)
#             print(f'founded c: {c}')

        else: 
            desired_c_list.append(otherwise_value)
            timeout_list.append(timeout)
            print(f'mutant {m} not_found')
            
    return (desired_c_list, timeout_list)



def str_arr_to_int(arr):
    res = []
    for a in arr:
        res.append(int(a))
    return res

def int_arr_to_str(arr):
    res = []
    for a in arr:
        res.append(str(a))
    return res 

def str_arr_to_float(arr):
    res = []
    for a in arr:
        res.append(float(a))
    return res 


def get_killed_mutant_array(csv_file):
    data = csv_file['mutant_number']
    array = data.to_numpy()
    str_array = int_arr_to_str(array)
    
    return str_array


def get_float_column(csv_file, field_name):
    data = csv_file[field_name]
    array = data.to_numpy()
    float_array = str_arr_to_float(array)
    
    return float_array





def get_longest_list(m):
    
    if len(m[0]) >= len(m[1])  and len(m[0]) >= len(m[2])and len(m[0]) >= len(m[3]):
            
        return 0
    elif len(m[1]) >= len(m_lists[0]) and len(m[1]) >= len(m_lists[2]) and len(m[1]) >= len(m_lists[3]):
            
        return 1
    elif len(m[2]) >= len(m[0]) and len(m[2]) >= len(m[1]) and len(m[2]) >= len(m[3]):
            
        return 2
    elif len(m[3]) >= len(m[0]) and len(m[3]) >= len(m[1]) and len(m[3]) >= len(m[2]):
        return 3


    
def make_same_size_lists(big_list, small_m_list, small_cretieria_list):
    for i, v in enumerate(big_list):
        if i > len(small_m_list)-1:
            print(f'index= {i} not in list')

            small_m_list.insert(i, '-1')
            small_cretieria_list.insert(i, 0.0)

        elif small_m_list[i] != v:
            print(f'index= {i} has value: {v}')
            small_m_list.insert(i, '-1')
            small_cretieria_list.insert(i, 0.0) 
            
def print_4_models(lists, list_type):
    print(f"bes_loop_{list_type}:     {lists[0]}")
    print(f"rand_loop_{list_type}:    {lists[1]}")
    
    print(f"bes_no_loop_{list_type}:  {lists[2]}")
    print(f"rand_no_loop_{list_type}: {lists[3]}")
    print("-----------------------------------------------")
    
    
#

def get_killed_mutant_all(dfs):
    bes_m_l_list     = get_killed_mutant_array(dfs[0]) 
    rand_m_l_list    = get_killed_mutant_array(dfs[1]) 
    bes_m_no_l_list  = get_killed_mutant_array(dfs[2]) 
    rand_m_no_l_list = get_killed_mutant_array(dfs[3]) 

    m_lists = (bes_m_l_list, rand_m_l_list, bes_m_no_l_list, rand_m_no_l_list)
    return m_lists

#old one:
def get_cretiera_all(dfs, creteria):
    bes_lo_c     = get_float_column(dfs[0], creteria)
    rand_lo_c    = get_float_column(dfs[1], creteria) 
    bes_no_lo_c  = get_float_column(dfs[2], creteria)
    rand_no_lo_c = get_float_column(dfs[3], creteria)

    c_lists = (bes_lo_c, rand_lo_c, bes_no_lo_c, rand_no_lo_c)
    return c_lists



#new one
def get_cretiera_all_desired_m(dfs, desired_mutants, creteria, otherwise_value, timeout=120):
    bes_lo_c     = filter_desired_m_and_fix(dfs[0], desired_mutants, creteria, otherwise_value, timeout)
    rand_lo_c    = filter_desired_m_and_fix(dfs[1], desired_mutants, creteria, otherwise_value, timeout)
    bes_no_lo_c  = filter_desired_m_and_fix(dfs[2], desired_mutants, creteria, otherwise_value, timeout)
    rand_no_lo_c = filter_desired_m_and_fix(dfs[3], desired_mutants, creteria, otherwise_value, timeout)

    c_lists = (bes_lo_c, rand_lo_c, bes_no_lo_c, rand_no_lo_c)
    return c_lists




def get_cretiera_only_2(dfs, desired_mutants, creteria, otherwise_value, timeout=120):
    bes_lo_c     = filter_desired_m_and_fix(dfs[0], desired_mutants, creteria, otherwise_value, timeout)
    bes_no_lo_c  = filter_desired_m_and_fix(dfs[2], desired_mutants, creteria, otherwise_value, timeout)

    c_lists = (bes_lo_c, bes_no_lo_c)
    return c_lists


def diff_killed_mutants(bes_killed_df, rand_killed_df):
    bes_killed = sorted(bes_killed_df.tolist())
    rand_killed = sorted(rand_killed_df.tolist())
    
    print(f"bes:  {bes_killed}")
    print("------------------")
    print(f"rand: {rand_killed}")
    print("------------------")

    diff = list(set(bes_killed).symmetric_difference(set(rand_killed))) 
    print(f"The mutant/s: {diff} \nhas been kiled by bes/random and not the other")
    
    return diff

def get_mutation_score(csv_file, all_mutants):
    killed_mutants = csv_file['mutant_number'].tolist()
    return (len(killed_mutants) / len(all_mutants), len(killed_mutants), len(all_mutants))



def prepare_plottting(m_lists, c_lists, creteria):
    biggest = get_longest_list(m_lists)
    print(biggest)
    
    (m_lists, 'killed_mutant')
    print_4_models(c_lists, creteria)

    for i, l in enumerate(m_lists):
        make_same_size_lists(m_lists[biggest], l, c_lists[i])

    print_4_models(m_lists, 'killed_mutant')
    print_4_models(c_lists, creteria)
    
    return biggest



def plot_4_bars(labels, data_list, d_map):
    
    bes_l, rand_l, bes_no_l, rand_no_l = data_list
    
    x = d_map['x_distance'] * np.arange(len(labels))
    width = d_map['bar_width'] #0.35  # the width of the bars

    indent = width / 2
    
    print(f'bes_l data: {bes_l}')
    print(f'rand_l data: {rand_l}')
    print(f'bes_no_l data: {bes_no_l}')
    print(f'rand_no_l data: {rand_no_l}')

    
    fig, ax = plt.subplots( figsize=(d_map['fig_width'], d_map['fig_hight']))

                           #,gridspec_kw={'width_ratios': [map_bes['width_ratio'], map_rand['width_ratio']]})
    
    rects1 = ax.bar(x - indent, bes_l[0], width, label=d_map['bes_l_label'], edgecolor='white', color='#FF3B00', hatch='-')
    rects2 = ax.bar(x + indent, rand_l[0], width, label=d_map['random_l_label'], color='#00B3FF', hatch='+')
    
    rects3 = ax.bar(x + 3*indent, bes_no_l[0], width, label=d_map['bes_no_l_label'], color='#22E65C', hatch='x')
    # rects4 = ax.bar(x - 3*indent, rand_no_l[0], width, label=d_map['random_no_l_label'], edgecolor='black', color='#FFFFFF', hatch='/')
    rects4 = ax.bar(x - 3*indent, rand_no_l[0], width, label=d_map['random_no_l_label'], edgecolor='white', color='#000000', hatch='/')



    #time outs:
    time1 = ax.bar(x - indent, bes_l[1], width, label=f'{d_map["bes_l_label"]}_timeout', color='#FF3B00', hatch='\\')
    time2 = ax.bar(x + indent, rand_l[1], width, label=f'{d_map["random_l_label"]}_timeout', color='#00B3FF', hatch='*')
    
    time3 = ax.bar(x + 3*indent, bes_no_l[1], width, label=f'{d_map["bes_no_l_label"]}_timeout',  edgecolor='black', color='white', hatch='o')
    time4 = ax.bar(x - 3*indent, rand_no_l[1], width, label=f'{d_map["random_no_l_label"]}_timeout', color='#000000', hatch='.')


    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(d_map['x_label'])
    ax.set_ylabel(d_map['y_label'])

    ax.set_title(d_map['title'])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

#     ax.bar_label(rects1, padding=3)
#     ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    
    ax.set_xlim([-3*width, d_map['x_lim']])
    ax.set_ylim([0, d_map['y_lim']])

    plt.show()
    img_path = os.path.join(img_general_path, f"{d_map['model_name']}")
    os.makedirs(img_path, exist_ok=True)
    fig.savefig(os.path.join(img_path,
            f"{d_map['comp_type']}_mutants_comparison_for_{d_map['model_name']}.svg"), 
            format="svg")



def plot_2_bars(labels, data_list, d_map):
    
    bes_l, bes_no_l = data_list
    
    x = d_map['x_distance'] * np.arange(len(labels)) # 1
    width = d_map['bar_width'] #0.35  # the width of the bars

    indent = width / 2

    fig, ax = plt.subplots(figsize=(d_map['fig_width'], d_map['fig_hight']))

    rects1 = ax.bar(x - width/2, bes_l[0], width, label=d_map['bes_l_label'])
    rects2 = ax.bar(x + width/2, bes_no_l[0], width, label=d_map['bes_no_l_label'])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(d_map['x_label'])
    ax.set_ylabel(d_map['y_label'])

    ax.set_title(d_map['title'])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

#     ax.bar_label(rects1, padding=3)
#     ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    ax.set_xlim([-3*width, d_map['x_lim']])
    ax.set_ylim([0, d_map['y_lim']])

    plt.show()
    img_path = os.path.join(img_general_path, f"{d_map['model_name']}")
    os.makedirs(img_path, exist_ok=True)
    fig.savefig(os.path.join(img_path,
            f"{d_map['comp_type']}_mutants_comparison_for_{d_map['model_name']}.svg"), 
            format="svg")



















