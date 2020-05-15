import math


# =================================================================================
# get_zipf_buckets
# Takes in a list of numbers, returns the top ten buckets
def get_zipf_buckets(values_list):
    bucket = {}
    for value in values_list:
        bucket[value] = bucket.get(value, 0) + 1
    top_bucket_list = []
    result_list = list(bucket.values())
    while len(result_list) < 10:
        result_list.append(0)
    result_list.sort()
    result_list.reverse()
    # print result_list
    for i in range(0, 10):
        top_bucket_list.append(float(result_list[i]) / float(len(values_list)))
    return top_bucket_list


# =================================================================================
# get_zipf_series
# Takes in a number, returns the supposed top ten
def get_zipf_series(number):
    top_list = [number]
    for i in range(1, 10):
        top_list.append(number / i)
    return top_list


# =================================================================================
# get_zipf_u_value
# Does the Watson variant of the Cramer von Mises test against the Zipf Series.
def get_zipf_u_value(probability_list):
    n = 10
    sub_total = 0
    z_bar = get_watson_z_bar(probability_list)
    for i in range(0, n):
        sub_total += math.pow((get_watson_z_value(i, probability_list) - z_bar), 2) * get_watson_weight(i, probability_list)
    total = sub_total * n
    return total


# =================================================================================
# accumulate_to
# Accumulates to an index of the list
def accumulate_to(in_list, index):
    total = 0
    for i in range(0, index):
        total += in_list[i]
    return total


# =================================================================================
# get_watson_z_value
# gets the Z value for a certain index and zipf index
def get_watson_z_value(list_index, in_list):
    zipf_list = get_zipf_series(in_list[0])
    z_value = accumulate_to(in_list, list_index) - accumulate_to(zipf_list, list_index)
    return z_value


# =================================================================================
# get_watson_z_bar
# gets the Z-bar value for a benfords list and a list of probability
def get_watson_z_bar(in_list):
    total_elements = 10
    z_bar = 0
    for i in range(0, total_elements):
        part_bar = get_watson_weight(i, in_list) * get_watson_z_value(i, in_list)
        z_bar += part_bar
    return z_bar


# =================================================================================
# get_watson_weight
# gets the t value (weight) for any given list index and zipf index
def get_watson_weight(list_index, in_list):
    weight = 0

    try:
        if list_index == (len(in_list) - 1):
            weight = in_list[list_index] + in_list[0]
            weight = weight / 2
        else:
            weight = in_list[list_index] + in_list[list_index + 1]
            weight = weight / 2
    except IndexError:
        raise IndexError
    return weight
# =================================================================================
