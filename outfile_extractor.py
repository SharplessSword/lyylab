from collections import namedtuple

Reaction = namedtuple('Reaction', ['reactant_title', 'temperature', 'column_name', 'branch_data_dict', 'loss',
                                   'capture', 'branch_ratio_dict'])


def extract_useful_part(file_name):
    data = []
    with open('./{}'.format(file_name)) as f:
        start = False
        end = False
        for line in f.readlines():
            if line.startswith('Temperature-Species Rate Tables:'):
                start = True
            if start and line.startswith('Reactant = P1 '):
                end = True
                break
            if start and not end:
                data.append(line)
    return data


def extract_class(reaction):
    reactant_title = reaction[0]
    temperature = [item[0] for item in reaction[2:]]
    column_name = reaction[1][1:-2]
    brach_data_dict = {}
    for i in range(1, len(reaction[1])-2):
        brach_data_dict[reaction[1][i]] = [ item[i] for item in reaction[2:]]
    loss = [float(item[-2]) for item in reaction[2:]]
    capture = [float(item[-1]) for item in reaction[2:]]
    branch_ratio_dict = calculate_branch_ratio(brach_data_dict, loss)
    return Reaction(reactant_title, temperature, column_name, brach_data_dict, loss, capture, branch_ratio_dict)


def clean_data(data):
    splited_data = []
    for i in data[2:]: # remove headers
        if i != '\n':
            i = i.strip()
            if i.startswith('Reactant'):
                splited_data.append([])
                # add Reactant
                splited_data[-1].append(i)
            else:
                splited_data[-1].append(i)
    result_list = []
    for block in splited_data:
        result_list.append([])
        for line in block:
            line = line.strip()
            if line.startswith('Reactant'):
                result_list[-1].append(line)
            elif line != '':
                result_list[-1].append(line.split())

    return result_list


def calculate_branch_ratio(branch_data_dict, loss):
    branch_ration_dict = {}
    for key, value in branch_data_dict.items():
        ration_list = [float(value[i])/loss[i] for i in range(len(value))]
        branch_ration_dict[key] = ration_list
    return branch_ration_dict

def get_reaction():
    data = extract_useful_part('0.01atm-1C5-.out')
    data = clean_data(data)
    r = extract_class(data[0])
    return r