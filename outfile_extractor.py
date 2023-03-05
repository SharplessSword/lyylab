import math
from collections import namedtuple
from smart_lyy import fitnlm, f_model, get_fit_curve_ydata
Reaction = namedtuple('Reaction', ['reactant_title', 'temperature', 'column_name', 'branch_data_dict', 'loss',
                                   'capture', 'branch_ratio_dict', 'important_branch_list'])


def extract_useful_part(content):
    data = []
    start = False
    end = False
    for line in content.split('\n'):
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
    temperature = [int(float(item[0])) for item in reaction[2:]]
    column_name = reaction[1][1:-2]
    branch_data_dict = {}
    for i in range(1, len(reaction[1])-2):
        branch_data_dict[reaction[1][i]] = [ float(item[i]) for item in reaction[2:]]
    loss = [float(item[-2]) for item in reaction[2:]]
    capture = [float(item[-1]) for item in reaction[2:]]
    branch_ratio_dict = calculate_branch_ratio(branch_data_dict, loss)
    import_branch_list = get_important_branch(branch_ratio_dict)
    # for import_branch in import_branch_list:
    #     print(branch_data_dict[import_branch])
    #     ydata_ln = [math.log(k) for k in branch_data_dict[import_branch]]
    #     print(ydata_ln)
    #     A, n, E = fitnlm(temperature, ydata_ln, f_model)
    #     print(A, n, E)
        # print([ get_fit_curve_ydata(A, n, E, one_temperature) for one_temperature in temperature])
    return Reaction(reactant_title, temperature, column_name, branch_data_dict, loss, capture, branch_ratio_dict,
                    import_branch_list)


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
        ration_list = [round(number, 4) for number in ration_list]
        branch_ration_dict[key] = ration_list
    return branch_ration_dict


def get_important_branch(branch_ratio_dict):
    important_branch_list = []
    for key, value_list in branch_ratio_dict.items():
        for value in value_list:
            if value >= 0.05:
                important_branch_list.append(key)
                break

    return important_branch_list


def get_reaction(content):
    data = extract_useful_part(content)
    data = clean_data(data)
    reaction_list = [extract_class(reaction) for reaction in data]
    return reaction_list

