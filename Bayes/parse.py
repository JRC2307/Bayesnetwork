import json


probs = []
querys = []
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
            input_probs = {}
            input_probs["nodes"] = aux
            input_probs["probability"] = prob[1]
            probs.append(input_probs)
    else:
        aux = prob[0]
        aux = aux.replace("+", "").replace("-", "").replace(" ","")
        if aux in nodes:
            input_probs[prob[0]] = prob[1]





# def dictionary(string):
#     for n in nodes:
#         dict = {'Node': node[n]}
#     print (dict)

input_nodes = input('Enter nodes: ')
nodes = parse_nodes(input_nodes)

number_of_nodes = int(input('Enter the number of probabilities: '))
for i in range(0, number_of_nodes):
    probability = input('Enter probability: ')
    parse_probabilities(probability)

number_of_queries = int(input('Enter the number of Querys: '))
for i in range(0, number_of_queries):
    query = input('Enter query: ')
    parse_query(query)


print(probs)
