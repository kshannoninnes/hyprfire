import math
import re
import bz2


# ===============================================================================
# GetInterArrivalTimes
# Takes a list of arrival times, finds out what the interarrival times are.
def get_interarrival_times(microsecondlist):
    current_time = 0
    time_diff_list = []
    try:
        current_time = microsecondlist[0]
    except Exception:
        current_time = microsecondlist.next()

    for time in microsecondlist:
        time_diff_list.append(time - current_time)
        current_time = time

    return time_diff_list


# ================================================================================
# GetBenfordsBuckets
# Takes a list of numbers, and a digit index, spits out the benford's prob of the indexth digit
def get_benfords_buckets(number_list, index):
    real_index = index - 1
    bucket_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    probability_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_valid_entries = 0
    for time in number_list:
        if time > 0:
            str_time = str(time)
            # print str_time
            try:
                first_element = int(str_time[real_index])
            except IndexError:
                # print "ERROR, No such value for index " + str(realIndex) + " and time " + str_time
                first_element = 0
            bucket_list[first_element] += 1
            total_valid_entries += 1

    if total_valid_entries != 0:
        for i in range(0, 10):
            probability_list[i] = float(bucket_list[i]) / total_valid_entries
    return probability_list


# ================================================================================
# GetBetterBenfordSeries
# Takes an index, returns the relevant Benfords Series
def get_benford_series(index):
    if index == 1:
        return [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
    elif index == 2:
        return [0.120, 0.114, 0.109, 0.104, 0.100, 0.097, 0.093, 0.090, 0.088, 0.085]
    elif index == 3:
        return [0.102, 0.101, 0.101, 0.101, 0.100, 0.100, 0.099, 0.099, 0.099, 0.098]
    else:
        return [0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100]


# =================================================================================
# GetBenfordsU
# Does the Watson variant of the Cramer von Mises test against the Benfords Series.
def get_benford_u_value(probability_list, benfords_index):
    n = 10
    if benfords_index == 1:
        n = 9
        probability_list = probability_list[1:]
    sub_total = 0
    z_bar = get_watson_z_bar(benfords_index, probability_list)
    for i in range(0, n):
        sub_total += math.pow((get_watson_z_value(benfords_index, i, probability_list) - z_bar), 2) * get_watson_weight(i, probability_list)
    total = sub_total * n
    return total


# =================================================================================
# AccumulateTo
# Accumulates to an index of the list
def accumulate_to(in_list, index):
    total = 0
    for i in range(0, index):
        total += in_list[i]
    return total


# =================================================================================
# GetWatsonZed
# gets the Z value for a certain index and benfords index
def get_watson_z_value(benfords_index, list_index, in_list):
    benford_list = get_benford_series(benfords_index)
    z_value = accumulate_to(in_list, list_index) - accumulate_to(benford_list, list_index)
    return z_value


# =================================================================================
# GetWatsonZedBar
# gets the Z-bar value for a benfords list and a list of probability
def get_watson_z_bar(benfords_index, in_list):
    total_elements = 10
    if benfords_index == 1:
        total_elements = 9
    z_bar = 0
    for i in range(0, total_elements):
        part_bar = get_watson_weight(i, in_list) * get_watson_z_value(benfords_index, i, in_list)
        z_bar += part_bar
    return z_bar


# =================================================================================
# GetWatsonWeight
# gets the t value (weight) for any given list index and benford index
def get_watson_weight(list_index, in_list):
    weight = 0
    if list_index == (len(in_list) - 1):
        weight = in_list[list_index] + in_list[0]
        weight /= 2
    else:
        weight = in_list[list_index] + in_list[list_index + 1]
        weight /= 2
    return weight
