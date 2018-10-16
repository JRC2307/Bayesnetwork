import copy
import itertools
import math

class Node:
    def __init__(self, name, parents, table):
        self.name = name
        self.parents = parents
        self.table = table

    def __repr__(self):
        return "node:\n\tname: %s \n\tparents: %s \n\ttable: %s\n" % (self.name, self.parents, self.table)

    def getParents(self):
        return self.parents

    def tableParent(self, probs):
            for n in probs.keys():
                key = copy.deepcopy(n);
                n = n.replace("+", "").replace("-", "")
                queries = n.split("|")

                if self.name == queries[0]:
                    self.table[key] = probs[key]
                    if len(queries) == 2:
                        for parent in queries[1].split(","):
                            if not parent in self.parents:
                                self.parents.append(parent)
                elif len(queries):
                    if self.name == queries[0]:
                        self.parents = None

    def tableFill(self):
        key = None
        d = copy.deepcopy(self.table)
        for t in self.table:
            if t[0] == "+":
                key = t.replace("+", "-", 1)
                if not key in self.table:
                    d[key] = round(1.0 - self.table[t], 5)
            elif t[0] == "-":
                key = t.replace("-", "+", 1)
                if not key in self.table:
                    d[key] = round(1.0 - self.table[t], 4)
        self.table = d


def get_hidden_vars(known, permutations):
    result = []
    aux = []
    for i in range(len(permutations)):
        aux = []
        for element in known:
            aux.append(element)
        for element in permutations[i]:
            aux.append(element)
        result.append(aux)
    return result


def set_parents(node_list, inp):
    for x in node_list:
        x.addParentandTable(inp)
        x.completeTable()


def parse_nodes(string):
    string = string.replace(" ", "")
    list = string.split(',')
    return list


def get_ancestors(node, list, ancestors):
    if node.parents:
        for element in node.parents:
            if element not in ancestors:
                ancestors.append(element)
            next_node = find_node(element, list)
            get_ancestors(next_node, list, ancestors)
    else:
        if node.name not in ancestors:
            ancestors.append(node.name)


def find_node(name, list):
    for n in list:
        if n.name == name:
            return n
    return False


def permute(vars):
    permutations = []
    positive_elements = copy.deepcopy(vars)
    negative_elements = copy.deepcopy(vars)
    permutation_list = []
    number = 0

    negative_aux = True

    for i in range(len(positive_elements)):
        positive_elements[i] = "+" + positive_elements[i]
    for i in range(len(negative_elements)):
        negative_elements[i] = "-" + negative_elements[i]

    for i in range(2 ** (len(vars) - 1)):
        number = math.ceil(math.sqrt(i))
        if number == 0:
            number = 1
        permutation_list = []
        for j in range(len(vars)):
            if j != number - 1:
                permutation_list.append(positive_elements[j])
            else:
                if negative_aux:
                    permutation_list.append(positive_elements[j])
                    negative_aux = False
                else:
                    permutation_list.append(negative_elements[j])
                    negative_aux = True
        permutations.append(permutation_list)
    rev_permutations = reverse(permutations)
    for r in rev_permutations:
        permutations.append(r)

    return permutations


def reverse(combinations):
    reversed_list = []
    aux = []
    for e in combinations:
        aux =[]
        for item in e:
            if "+" in item:
                aux.append(item.replace("+", "-"))
            elif "-" in item:
                aux.append(item.replace("-", "+"))
        reversed_list.append(aux)
    return reversed_list


def regla_cadena(permutations, list):
    probabilidad = 0.0
    marker = True
    probs = []
    for element in permutations:
        probabilities = []
        #If it's not a terminal
        if type(element) is list:
            for e in element:
                name = e.replace("-", "").replace("+", "")
                next_node = find_node(name, list)
                if next_node.parents:
                    permutations = itertools.permutations(range(0, len(next_node.parents)))
                    for p in permutations:
                        parent_nodes = []
                        for l in p:
                            if "+" + next_node.parents[l] in element:
                                parent_nodes.append("+" + next_node.parents[l])
                            elif "-" + next_node.parents[l] in element:
                                parent_nodes.append("-" + next_node.parents[l])
                        parents_string = e + "|"
                        for i in range(len(parent_nodes)):
                            parents_string += parent_nodes[i]
                            if i < len(parent_nodes) - 1:
                                parents_string += ","
                        if parents_string in next_node.table:
                            value = next_node.table[parents_string]
                            probabilities.append(value)

                else:
                    value = next_node.table[e]
                    probabilities.append(value)
            probs.append(probabilities)
        #its terminal
        else:
            if element:
                name = element.replace("-", "").replace("+", "")
                next_node = find_node(name, list)
                if next_node.parents:
                    permutations = itertools.permutations(range(0, len(next_node.parents)))
                    for p in permutations:
                        parent_nodes = []
                        for l in p:

                            if "+" + next_node.parents[l] in permutations:
                                parent_nodes.append("+" + next_node.parents[l])
                            elif "-" + next_node.parents[l] in permutations:
                                parent_nodes.append("-" + next_node.parents[l])
                        parents_string = element + "|"

                        for i in range(len(parent_nodes)):
                            parents_string += parent_nodes[i]
                            if i < len(parent_nodes) - 1:
                                parents_string += ","
                        if parents_string in next_node.table:
                            value = next_node.table[parents_string]
                            probabilities.append(value)

                else:
                    value = next_node.table[element]
                    probabilities.append(value)
                probs.append(probabilities[0])

    multiplicador = 1.0

    for element in probs:
        if type(element) is list:
            marker = True
            multiplicador = 1.0
            for e in element:
                multiplicador *= e
            probabilidad += multiplicador
        else:
            marker = False
            multiplicador *= element
    if marker:
        return probabilidad
    else:
        return multiplicador



def init_nodes(nodes):
    node_list = []
    for var in nodes.split(','):
        node_list.append(Node(var, [], {}))

    return node_list


def start_bayes(nodes, probs, queries):
    node_list = init_nodes(nodes)
    prob = parse_probabilities(probs)


    return


def parse_probabilities(string):
    statement_list = {}
    for statement in string:
        variables = statement.split('=')
        statement_list[variables[0]] = float(variables[1])
    return statement_list


def parse_queries(string, list):
    for s in string:
        num = ""
        den = ""

        aux = s.split('|')
        if len(aux) == 2:
            num = aux[0] + ',' + aux[1]
            den = aux[1]
        elif len(aux) == 1:
            num = aux[0]

    return 0

input_nodes = input('Enter nodes: ')

number_of_nodes = int(input('Enter the number of probabilities: '))

probs = []

for i in range(0, number_of_nodes):
    probability = input('Enter probability: ')
    probs.append(probability)

queries = []

output_number = int(input('Enter number of outputs: '))
for i in range(0, number_of_nodes):
    out_prob = input('Enter probability: ')
    queries.append(out_prob)

start_bayes(input_nodes, probs, queries)
