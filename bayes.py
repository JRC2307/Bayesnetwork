import itertools
import copy
import json
import decimal
import math

class Node:
    def __init__(self, name, parents, table):
        self.name = name
        self.parents = parents
        self.table = table

    def __repr__(self):
        return "name: %s \n\tparents: %s \n\ttable: %s\n" % (self.name, self.parents, self.table)

    def get_parents(self):
        return self.parents

    def add_parents(self, table):
        for k in table.keys():
            key = copy.deepcopy(k);
            k = k.replace("+", "").replace("-", "")
            split_nodes = k.split('|')

            if self.name == split_nodes[0]:
                self.table[key] = table[key]
                if len(split_nodes) == 2:
                    for parent in split_nodes[1].split(","):
                        if not parent in self.parents:
                            self.parents.append(parent)
                elif len(split_nodes) == 1:
                    if self.name == split_nodes[0]:
                        self.parents = None

    def fill_table(self):
        aux = copy.deepcopy(self.table)
        for t in self.table:
            if t[0] == "+":
                key = t.replace("+", "-", 1)
                if not key in self.table:
                    aux[key] = round(1.0 - self.table[t], 4)
            elif t[0] == "-":
                key = t.replace("-", "+", 1)
                if not key in self.table:
                    aux[key] = round(1.0 - self.table[t], 4)
        self.table = aux

def get_hidden_vars(given, permutations):
    result = []
    for i in range(len(permutations)):
        aux = []
        for element in given:
            aux.append(element)
        for element in permutations[i]:
            aux.append(element)
        result.append(aux)
    return result

def set_parents(list, probabilities):
    for element in list:
        element.add_parents(probabilities)
        element.fill_table()

def ini_nodos(string):
    list = []
    for var in string.split(','):
        list.append(Node(var, [], {}))
    return list

def parse_probabilities(string):
    prob_list = {}
    for statement in string:
        variables = statement.split('=')
        prob_list[variables[0]] = float(variables[1])
    return prob_list

def parse_queries(string, list):
    for e in string:
        num = ""
        den = ""
        aux = e.split("|")
        if len(aux) == 2:
            num = aux[0] + ',' + aux[1]
            den = aux[1]
        elif len(aux) == 1:
            num = aux[0]
        probabilidad_condicional(num, den, list)
    return 0

def get_ancestors(node, list, a):
    if node.parents:
        for element in node.parents:
            if element not in a:
                a.append(element)
            newnode = find_node(element, list)
            get_ancestors(newnode, list, a)
    else:
        if node.name not in a:
            a.append(node.name)

def find_node(name, list):
    for element in list:
        if element.name == name:
            return element
    return False

def permute(unknown_vars):
    permutations = []
    positive_nodes = copy.deepcopy(unknown_vars)
    negative_nodes = copy.deepcopy(unknown_vars)
    aux = True
    for i in range(len(positive_nodes)):
        positive_nodes[i] = "+" + positive_nodes[i]
    for i in range(len(negative_nodes)):
        negative_nodes[i] = "-" + negative_nodes[i]

    for i in range(2**(len(unknown_vars) - 1)):
        number = math.ceil(math.sqrt(i))
        if number == 0:
            number = 1
        perm_aux = []
        for j in range(len(unknown_vars)):
            if j == number - 1:
                if aux:
                    perm_aux.append(positive_nodes[j])
                    aux = False
                else:
                    perm_aux.append(negative_nodes[j])
                    aux = True
            else:
                perm_aux.append(positive_nodes[j])

        permutations.append(perm_aux)
    reverse_combinations = reverse(permutations)
    for element in reverse_combinations:
        permutations.append(element)

    return permutations

def reverse(list):
    reversed_list = []
    for element in list:
        aux =[]
        for item in element:
            if "+" in item:
                aux.append(item.replace("+", "-"))
            elif "-" in item:
                aux.append(item.replace("-", "+"))
        reversed_list.append(aux)
    return reversed_list

def regla_cadena(permutations, nodes):
    f = True
    prob = 0.0
    multiplicador = 1.0
    prob_aux = []
    for perm in permutations:
        probabilities = []
        if type(perm) is list:
            for e in perm:
                name = e.replace("-", "").replace("+", "")
                next_node = find_node(name, nodes)
                if next_node.parents:
                    next_moves = itertools.permutations(range(0, len(next_node.parents)))
                    for move in next_moves:
                        parents = []
                        for l in move:
                            if "+" + next_node.parents[l] in perm:
                                parents.append("+" + next_node.parents[l])

                            elif "-" + next_node.parents[l] in perm:
                                parents.append("-" + next_node.parents[l])
                        string = e + "|"
                        for i in range(len(parents)):
                            string += parents[i]
                            if i < len(parents) - 1:
                                string += ","
                        if string in next_node.table:
                            val = next_node.table[string]
                            probabilities.append(val)
                else:
                    val = next_node.table[e]
                    probabilities.append(val)
            prob_aux.append(probabilities)
        else:
            if perm:
                name = perm.replace("-", "").replace("+", "")
                next_node = find_node(name, nodes)
                if next_node.parents:
                    next_moves = itertools.permutations(range(0, len(next_node.parents)))
                    for move in next_moves:
                        parents = []
                        for l in move:
                            if "+" + next_node.parents[l] in permutations:
                                parents.append("+" + next_node.parents[l])
                            elif "-" + next_node.parents[l] in permutations:
                                parents.append("-" + next_node.parents[l])
                        string = perm + "|"

                        for i in range(len(parents)):
                            string += parents[i]
                            if i < len(parents) - 1:
                                string += ","
                        if string in next_node.table:
                            val = next_node.table[string]
                            probabilities.append(val)

                else:
                    val = next_node.table[perm]
                    probabilities.append(val)
                prob_aux.append(probabilities[0])
    for perm in prob_aux:
        if type(perm) is list:
            f = True
            multiplicador = 1.0
            for e in perm:
                multiplicador *= e
            prob += multiplicador
        else:
            f = False
            multiplicador *= perm
    if f:
        return prob

    else:
        return multiplicador

def probabilidad_condicional(num, den, list):
    hidden_num = []
    know_num = num.split(',')
    for e in know_num:
        if "+" in e:
            aux = e.replace('+', "")
        elif "-" in e:
            aux = e.replace('-', "")
        node = find_node(aux, list)
        ancestor_list = []
        if node.parents:
            get_ancestors(node, list, ancestor_list)
        for ancestor in ancestor_list:
            if not "+" + ancestor in know_num and not "-" + ancestor in know_num and not ancestor in hidden_num:
                hidden_num.append(ancestor)
    if hidden_num:
        perm_num = permute(hidden_num)
        enum_vars = get_hidden_vars(know_num, perm_num)
    else:
        enum_vars = know_num
    num_val = regla_cadena(enum_vars, list)

    if den:
        hidden_den = []
        given_den = den.split(',')
        for e in given_den:
            if "+" in e: aux = e.replace('+', "")
            elif "-" in e: aux = e.replace('-', "")
            node = find_node(aux, list)
            ancestor_list = []
            if node.parents:
                get_ancestors(node, list, ancestor_list)
            for ancestor in ancestor_list:
                if not "+" + ancestor in given_den and not "-" + ancestor in given_den and not ancestor in hidden_den:
                    hidden_den.append(ancestor)
        if hidden_den:
            perm_den = permute(hidden_den)
            en_vars = get_hidden_vars(given_den, perm_den)
        else:
            en_vars = given_den
        den_value = regla_cadena(en_vars, list)
        if(den_value == 0.0):
            den_value = 1.0
    else:
        den_value = 1.0
    result = round( num_val / den_value, 7)
    print(result)
    return 0

def bayes(nodes, prob_strings, query_strings):
    nodes_list = ini_nodos(nodes)
    probabilities_list = parse_probabilities(prob_strings)
    set_parents(nodes_list, probabilities_list)
    parse_queries(query_strings, nodes_list)
    return 0

if __name__ == "__main__":
    nodes = input()
    numberprobabilities = int(input())

    probabilities = []

    for x in range(0, numberprobabilities):
        probabilities.append(input())

    numberqueries = int(input())

    queries = []

    for x in range(0, numberqueries):
        queries.append(input())

    bayes(nodes, probabilities, queries)
