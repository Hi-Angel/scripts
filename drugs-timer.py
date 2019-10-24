import fileinput
import sys
from functools import reduce

average_daytime = 15
base_time = int(input())
assert(base_time >= 0 and base_time <= 24)
def calc_one_drug(description_line):
    descr_split = description_line.split()
    n_times_a_day = int(descr_split[-1])
    assert(n_times_a_day >= 1)
    drug_name = " ".join(descr_split[:-1])
    if n_times_a_day == 1:
        return (drug_name, [base_time])
    else:
        optimal_timespan = int(average_daytime / (n_times_a_day-1))
        return (drug_name, [(base_time + h * optimal_timespan) % 24 for h in range(0, n_times_a_day)])

def pretty_hour(h):
    return str(h) + "⁰⁰"

def parse():
    ret = []
    for descr in fileinput.input():
        if not descr.isspace():
            ret.append(calc_one_drug(descr))
    return ret

drugs = parse()
drugs.sort(key = lambda v: len(v[1]))

for (drug_name, spans) in drugs:
    # align to 3 tabs = 24 spaces
    tabs = '\t\t\t' if len(drug_name) <= 7 else \
        '\t\t' if len(drug_name) <= 15 else \
        '\t'
    print(drug_name + tabs + pretty_hour(spans[0]) + reduce(lambda acc,h: acc + ", " + pretty_hour(h), spans[1:], ""))
