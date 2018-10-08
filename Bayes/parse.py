import json


input_probs = {}
nodes = []


def parse_nodes(string):
    string = string.replace(" ", "")
    list = string.split(',')
    return list


def check_node_exists(elements):
    for e in elements:
        element = e.replace("+", "").replace("-", "").replace(" ", "")
        if element in nodes:
            print(element)
            print(nodes)
            continue
        else:
            return False
    return True


def parse_probabilities(string):
    prob = string.replace(" ","").split('=')
    if "|" in prob[0]:
        aux = prob[0].split("|")
        if check_node_exists(aux):
            input_probs[prob[0]] = prob[1]
    else:
        aux = prob[0]
        aux = aux.replace("+", "").replace("-", "").replace(" ","")
        if aux in nodes:
            input_probs[prob[0]] = prob[1]


input_nodes = input('Enter nodes: ')
nodes = parse_nodes(input_nodes)

number_of_nodes = int(input('Enter the number of probabilities: '))

for i in range(0, number_of_nodes):
    probability = input('Enter probability: ')
    parse_probabilities(probability)

print(json.dumps(input_probs))