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


def set_parents(node_list, inp):
    for x in node_list:
        x.addParentandTable(inp)
        x.completeTable()


def parse_nodes(string):
    string = string.replace(" ", "")
    list = string.split(',')
    return list


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


def find_node(name, list):
    for n in list:
        if n.name == name:
            return n
    return False


def conditional_probability(numerator, denominator, list):
    numhid = []
    input_num = numerator.split(',')
    for e in input_num:

        if "+" in e:
            aux = e.replace('+', "")
        elif "-" in e:
            aux = e.replace('-', "")
        node = find_node(aux, list)

        ancestors = []
        if node.parents:
            find_node(node, list, ancestors)

        for ancestor in ancestors:

            if not ("+" + ancestor) in input_num and not ("-" + ancestor) in input_num and not (ancestor in numhid):
                numhid.append(ancestor)


def init_nodes(nodes):
    node_list = []
    for var in nodes.split(','):
        node_list.append(Node(var, [], {}))

    return node_list

def start_bayes(nodes, probs, queries):
    node_list = init_nodes(nodes)
    prob = parse_probabilities(probs)


    return


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
