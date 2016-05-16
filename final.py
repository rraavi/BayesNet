import random
import sys

paths = ['B', 'E', 'A', 'J', 'M']
temp_paths = paths[::-1]

bayesnet = {'B': [[], {'T': .001}],
            'E': [[], {'T': .002}],
            'A': [['B', 'E'], {'FF': .001,
                               'FT': .29,
                               'TF': .94,
                               'TT': .95}],
            'J': [['A'], {'T': 0.90,
                          'F': 0.05}],
            'M': [['A'], {'T': 0.70,
                          'F': 0.01}]}


def calculate_probability(node, truth, evidence_list, bayes_net):
    parentList = bayes_net[node][0]
    if len(parentList) == 0:
        probability = bayes_net[node][1]['T']
    else:
        truths = [evidence_list[eachParent] for eachParent in parentList]
        z = ''.join(truths)
        probability = bayes_net[node][1][z]
    if truth != 'T':
        return 1.0 - probability
    else:
        return probability


def rejection_count_num(truth, keys, r_count, final_samples):
    final_truths_nume = []
    num_count = 0
    for y in xrange(r_count):
        z = []
        for a in keys:
            z.append(final_samples[y][0][a])
        final_truths_nume.append(z)
    for x in final_truths_nume:
        if truth == x:
            num_count += 1
    return num_count


def rejection_sampling(query_list, evidence_dict, bayesnet, r_count):
    final_samples = []

    for x in xrange(r_count):
        rejection_sample(bayesnet, evidence_dict, final_samples)

    den_count = len(final_samples)

    for node in query_list:
        truth = []
        keys = []
        for x1 in evidence_dict:
            truth.append(evidence_dict.get(x1))
            keys.append(x1)
        truth.append('T')
        keys.append(node)
        num_count = rejection_count_num(truth, keys, den_count, final_samples)

        try:
            final_prob = num_count / float(den_count)
            print node, final_prob
        except:
            print 'Divide by Zero Error, i.e not enough Samples'


def enumeration_ask(query_node, evidence_list, bayes_net, temp_paths):
    q = {}
    z = 0.0
    for x in ['T', 'F']:
        evidence_list[query_node] = x
        q[x] = enumerate_all(temp_paths, evidence_list, bayes_net)
        del evidence_list[query_node]
    for k,v in q.items():
        z+=v
    for k,v in q.items():
        q[k] /= z

    print query_node, q['T']


def enumerate_all(temp_paths, evidence_list, bayes_net):
    if len(temp_paths) == 0:
        return 1.0
    temp_node = temp_paths.pop()
    if temp_node not in evidence_list:
        val = 0
        evidence_list[temp_node] = 'T'
        temp_enumerate_return = enumerate_all(temp_paths, evidence_list, bayes_net)
        temp_probab_value = calculate_probability(temp_node, 'T', evidence_list, bayes_net)
        val += temp_probab_value * temp_enumerate_return
        evidence_list[temp_node] = 'F'
        temp_enumerate_return = enumerate_all(temp_paths, evidence_list, bayes_net)
        temp_probab_value = calculate_probability(temp_node, 'F', evidence_list, bayes_net)
        val += temp_probab_value * temp_enumerate_return
        del evidence_list[temp_node]
        temp_paths.append(temp_node)
        return val
    else:
        temp_enumerate_return = enumerate_all(temp_paths, evidence_list, bayes_net)
        temp_probab_value = calculate_probability(temp_node, evidence_list[temp_node], evidence_list, bayes_net)
        val = temp_probab_value * temp_enumerate_return
        temp_paths.append(temp_node)
        return val


def sampling(bayes_net, final_samples):
    sample = []
    sample1 = {}

    for path in paths:
        if path == 'A':
            str = sample[0] + sample[1]
            random_number = random.random()
            if random_number < bayes_net[path][1][str]:
                sample.append('T')
                sample1[path] = 'T'
            else:
                sample.append('F')
                sample1[path] = 'F'

        elif path == 'J' or path == 'M':
            str1 = sample[2]
            random_number = random.random()
            if random_number < bayes_net[path][1][str1]:
                sample.append('T')
                sample1[path] = 'T'
            else:
                sample.append('F')
                sample1[path] = 'F'

        elif path == 'B' or path == 'E':
            random_number = random.random()
            if random_number < bayes_net[path][1]['T']:
                sample.append('T')
                sample1[path] = 'T'
            else:
                sample.append('F')
                sample1[path] = 'F'

    abc = []
    abc.append(sample1)
    final_samples.append(abc)
    return final_samples


def count_den(truth, keys, r_count, final_samples):
    den_count = 0
    final_truths_deno = []
    for y in xrange(r_count):
        z = []
        for a in keys:
            z.append(final_samples[y][0][a])
        final_truths_deno.append(z)
    for x in final_truths_deno:
        if truth == x:
            den_count += 1
    return den_count


def rejection_sample(bayes_net, evidence, final_samples):
    sample = []
    sample1 = {}

    for path in paths:
        if path == 'A':
            str = sample[0] + sample[1]
            random_number = random.random()
            if random_number < bayes_net[path][1][str]:
                sample.append('T')
                sample1[path] = 'T'
            else:
                sample.append('F')
                sample1[path] = 'F'
            if path in evidence:
                if sample1[path] == evidence[path]:
                    pass
                else:
                    return

        elif path == 'J' or path == 'M':
            str1 = sample[2]
            random_number = random.random()
            if random_number < bayes_net[path][1][str1]:
                sample.append('T')
                sample1[path] = 'T'
            else:
                sample.append('F')
                sample1[path] = 'F'
            if path in evidence:
                if sample1[path] == evidence[path]:
                    pass
                else:
                    return

        elif path == 'B' or path =='E':
            random_number = random.random()
            if random_number < bayes_net[path][1]['T']:
                sample.append('T')
                sample1[path] = 'T'
            else:
                sample.append('F')
                sample1[path] = 'F'
            if path in evidence:
                if sample1[path] == evidence[path]:
                    pass
                else:
                    return
    abc = []
    abc.append(sample1)
    final_samples.append(abc)
    return final_samples


def count_num(truth, keys, r_count, final_samples):
    final_truths_nume = []
    num_count = 0
    for y in xrange(r_count):
        z = []
        for a in keys:
            z.append(final_samples[y][0][a])
        final_truths_nume.append(z)
    for x in final_truths_nume:
        if truth == x:
            num_count += 1
    return num_count


def prior_sampling(query_list, evidence_dict, bayes_net, r_count):
    final_samples = []
    for x in xrange(r_count):
        sampling(bayes_net, final_samples)

    truth = []
    keys = []

    for x in evidence_dict:
        truth.append(evidence_dict.get(x))
        keys.append(x)
    den_count = count_den(truth, keys, r_count, final_samples)


    for x in query_list:
        truth = []
        keys = []
        for x1 in evidence_dict:
            truth.append(evidence_dict.get(x1))
            keys.append(x1)
        truth.append('T')
        keys.append(x)
        num_count = count_num(truth, keys, r_count, final_samples)

        try:
            final_prob = num_count / float(den_count)
            print x, final_prob
        except:
            print 'Divide by Zero Error, i.evidence_dict not enough Samples'


def likelihood_sampling(bayes_net, evidence, final_samples):

    paths_to_sample = list(paths)
    for x in evidence:
        paths_to_sample.pop(paths_to_sample.index(x))

    sample = []
    sample1 = {}
    weight_vec = 1.0
    for path in paths:
        if path == 'B' or path == 'E':
            if path in paths_to_sample:
                random_number = random.random()
                if random_number < bayes_net[path][1]['T']:
                    sample.append('T')
                    sample1[path] = 'T'
                else:
                    sample.append('F')
                    sample1[path] = 'F'
            else:
                sample.append(evidence[path])
                sample1[path] = evidence[path]
                if evidence[path] in bayes_net[path][1]:
                    weight_vec *= bayes_net[path][1][evidence[path]]
                else:
                    if evidence[path] == 'F':
                        weight_vec *= (1 - bayes_net[path][1]['T'])

        elif path == 'A':
            if path in paths_to_sample:
                str = sample[0] + sample[1]
                random_number = random.random()
                if random_number < bayes_net[path][1][str]:
                    sample.append('T')
                    sample1[path] = 'T'
                else:
                    sample.append('F')
                    sample1[path] = 'F'
            else:
                str = sample[0] + sample[1]
                sample.append(evidence[path])
                sample1[path] = evidence[path]
                if evidence[path] == 'T':
                    weight_vec *= bayes_net[path][1][str]
                elif evidence[path] == 'F':
                    weight_vec *= (1 - bayes_net[path][1][str])

        elif path == 'J' or path == 'M':
            if path in paths_to_sample:
                str1 = sample[2]
                random_number = random.random()
                if random_number < bayes_net[path][1][str1]:
                    sample.append('T')
                    sample1[path] = 'T'
                else:
                    sample.append('F')
                    sample1[path] = 'F'
            else:
                str1 = sample[2]
                sample.append(evidence[path])
                sample1[path] = evidence[path]
                if evidence[path] == 'T':
                    weight_vec *= bayes_net[path][1][str1]
                elif evidence[path] == 'F':
                    weight_vec *= (1 - bayes_net[path][1][str1])

    abc = []
    abc.append(sample1)
    abc.append(weight_vec)
    final_samples.append(abc)
    return final_samples


def likelihood_count_den(truth, keys, r_count, final_samples):
    den_count = 0
    final_truths_deno = []
    for y in xrange(r_count):
        z = []
        for a in keys:
            z.append(final_samples[y][0][a])
        final_truths_deno.append(z)
    for x in xrange(len(final_truths_deno)):
        if truth == final_truths_deno[x]:
            den_count += final_samples[x][1]
    return den_count


def likelihood_count_num(truth, keys, r_count, final_samples):
    final_truths_nume = []
    num_count = 0
    for y in xrange(r_count):
        z = []
        for a in keys:
            z.append(final_samples[y][0][a])
        final_truths_nume.append(z)
    for x in xrange(len(final_truths_nume)):
        if truth == final_truths_nume[x]:
            num_count += final_samples[x][1]
    return num_count


def likelihood_weighting(query_list, evidence_dict, bayesnet, r_count):
    final_samples = []

    for x in xrange(r_count):
        likelihood_sampling(bayesnet, evidence_dict, final_samples)

    truth = []
    keys = []

    for x in evidence_dict:
        truth.append(evidence_dict.get(x))
        keys.append(x)
    den_count = likelihood_count_den(truth, keys, r_count, final_samples)

    for x in query_list:
        truth = []
        keys = []
        for x1 in evidence_dict:
            truth.append(evidence_dict.get(x1))
            keys.append(x1)
        truth.append('T')
        keys.append(x)
        num_count = likelihood_count_num(truth, keys, r_count, final_samples)

        try:
            final_prob = num_count / float(den_count)
            print x, final_prob
        except:
            print 'Divide by Zero Error, i.evidence_dict not enough Samples'


n, t = [int(x) for x in raw_input().split()]
evidence = {}
query = []

for x in xrange(n):
    node, truth_value = raw_input().split()
    if truth_value.lower() == 't':
        truth_value = 'T'
    elif truth_value.lower() == 'f':
        truth_value = 'F'
    evidence[node] = truth_value

for x in xrange(t):
    query.append(raw_input())

var1 = sys.argv[1]
var2 = sys.argv[2]

var2 = int(var2)

if var1 == 'e':
    for x in query:
        enumeration_ask(x, evidence, bayesnet, temp_paths)
elif var1 == 'p':
    prior_sampling(query, evidence, bayesnet, var2)
elif var1 == 'r':
    rejection_sampling(query, evidence, bayesnet, var2)
elif var1 == 'l':
    likelihood_weighting(query, evidence, bayesnet, var2)
