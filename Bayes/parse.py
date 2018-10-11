inp = []
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
            querys.append(output_probs)
    else:
        temp_node = string.replace("+", "").replace("-", "").replace(" ", "")
        if temp_node in nodes:
            output_probs["nodes"] = string
            output_probs["prob"] = None
            querys.append(output_probs)


input_nodes = input('Enter nodes: ')
nodes = parse_nodes(input_nodes)

number_of_nodes = int(input('Enter the number of probabilities: '))

for i in range(0, number_of_nodes):
    probability = input('Enter probability: ')
    parse_probabilities(probability)

output_number = int(input('Enter number of outputs: '))
for i in range(0, number_of_nodes):
    out_prob = input('Enter probability: ')
    parse_output(out_prob)



print(inp)
print(querys)