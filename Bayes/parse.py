inp = []
queries = []
nodes = []

class Node:
    def __init__(self, name, parents, table):
        self.name = name
        self.parents = parents
        self.table = table

    def __repr__(self):
        return "node:\n\tname: %s \n\tparents: %s \n\ttable: %s\n" % (self.name, self.parents, self.table)

    def getParents(self):
        return self.parents


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
    input_probs = {}
    if "|" in prob[0]:
        aux = prob[0].split("|")
        if check_node_exists(aux):
            input_probs["nodes"] = aux
            input_probs["prob"] = prob[1]
            inp.append(input_probs)
    else:
        aux = prob[0]
        aux = aux.replace("+", "").replace("-", "").replace(" ","")
        if aux in nodes:
            input_probs["nodes"] = prob[0]
            input_probs["prob"] = prob[1]
            inp.append(input_probs)


def parse_output(string):
    output_probs = {}
    if "|" in string:
        aux = string.split("|")
        if check_node_exists(aux):
            output_probs["nodes"] = aux
            output_probs["prob"] = None
            queries.append(output_probs)
    else:
        temp_node = string.replace("+", "").replace("-", "").replace(" ", "")
        if temp_node in nodes:
            output_probs["nodes"] = string
            output_probs["prob"] = None
            queries.append(output_probs)


def init_nodes(nodes):
    node_list = []
    for var in nodes.split(','):
        node_list.append(Node(var, [], {}))

    return node_list

def start_bayes(nodes, probs, queries):
    node_list = init_nodes(nodes)

    return


input_nodes = input('Enter nodes: ')

number_of_nodes = int(input('Enter the number of probabilities: '))

for i in range(0, number_of_nodes):
    probability = input('Enter probability: ')
    parse_probabilities(probability)

output_number = int(input('Enter number of outputs: '))
for i in range(0, number_of_nodes):
    out_prob = input('Enter probability: ')
    parse_output(out_prob)


start_bayes(input_nodes, inp, queries)