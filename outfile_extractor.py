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
    print(reaction)
    reactant_title = reaction[0]
    temperature = [item[0] for item in reaction[2:]]
    print(len(reaction))
    brach_data_dict = {}
    for i in range(1, len(reaction[1])-2):
        brach_data_dict[reaction[1][i]] = [ item[i] for item in reaction[2:]]


    loss = [float(item[-2]) for item in reaction[2:]]
    capture = [float(item[-1]) for item in reaction[2:]]

    #return Reaction(reactant_title, temperature, reactant_data_dict, loss)


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


def calculate(result):
    calculated_result =[]
    for block in result:
        calculated_result.append([])
        for i, line in enumerate(block):
            if i == 0 :
                calculated_result[-1].append(line)
            elif i == 1:
                line_list = []
                line_list.append(line[0])
                for column_name in line[1:-2]:
                    line_list.append(column_name)
                    line_list.append('分支比')
                line_list += line[-2:]
                calculated_result[-1].append(line_list)
            else:
                line_list = []
                line_list.append(line[0])
                for column_value in line[1:-2]:
                    column_value = float(column_value)
                    line_list.append(column_value)
                    line_list.append(column_value/float(line[-2]))
                line_list += line[-2:]
                calculated_result[-1].append(line_list)
    return calculated_result



data = extract_useful_part('0.01atm-1C5-.out')
data = clean_data(data)
extract_class(data[0])