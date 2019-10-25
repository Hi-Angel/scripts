import fileinput
import sys
from functools import reduce

average_daytime = 15
base_time = int(input())
assert(base_time >= 0 and base_time <= 24)

# String -> {UInt, String} -> {UInt, String}
def calc_one_drug(description_line, times_accum):
    descr_split = description_line.split()
    n_times_a_day = int(descr_split[-1])
    assert(n_times_a_day >= 1)
    drug_name = " ".join(descr_split[:-1])
    def more_than_one_time():
        optimal_timespan = int(average_daytime / (n_times_a_day-1))
        return [(base_time + h * optimal_timespan) % 24 for h in range(0, n_times_a_day)]
    times = [base_time] if n_times_a_day == 1 else more_than_one_time()
    for time in times:
        if time in times_accum:
            times_accum[time] += ", " + drug_name
        else:
            times_accum[time] = drug_name
    return times_accum

def pretty_hour(h):
    return str(h) + "⁰⁰"

def parse():
    accum = {}
    for descr in fileinput.input():
        if not descr.isspace():
            calc_one_drug(descr, accum)
    return accum

drugs = parse()
for (time, drug_names) in sorted(drugs.items(),
                                 key = lambda pair: pair[0] if pair[0] >= base_time else pair[0] + 24):
    print(pretty_hour(time) + "\t" + drug_names)
