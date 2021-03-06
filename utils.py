# from io import BytesIO
import itertools
import warnings
from io import StringIO
from random import shuffle
import pdfminer
# from pandas.tests.extension.numpy_.test_numpy_nested import np
import numpy as np
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys
import getopt

warnings.filterwarnings('error', category=UnicodeWarning)
# from http://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/
# converts pdf, returns its text content as a string
import load_info


def get_filepath(target_filename):
    dropbox_path = "/Users/DanielLongo/Dropbox/VC RA Avinika Narayan/Contracts project/coi/Done OCR'd/"
    for root, dirs, files in os.walk(dropbox_path):
        for dir in dirs:
            for filename in os.listdir(dropbox_path + dir):
                if filename == target_filename:
                    return dropbox_path + dir + "/" + filename


def get_filenames(n, shuffle_filenames=True):
    y = load_info.load_info_xlsx("~/Desktop/ContractsProject/rs1 database AN.xlsx", np_array=False)
    filenames = list(y["File Name"])
    assert (len(filenames) > 1), "No filenames found"
    if shuffle_filenames:
        shuffle(filenames)
    out = []
    for filename in filenames:
        cur_filepath = get_filepath(filename)
        if cur_filepath != None:
            out += [cur_filepath]
            if len(out) == n:
                return out
    print("Insufficient filenames")


def check_security_names_equal(a, b):
    # checks if security names are the same just slightly different variations
    a = a.replace(" stock", "")
    b = b.replace(" stock", "")
    return a == b


def get_index_security_names_equal(target, names):
    for i in range(len(names)):
        if check_security_names_equal(names[i], target):
            return i
    return -1


def is_num(x):
    x = x.strip('$')
    try:
        float(x)
    except ValueError:
        return False
    return True


def get_num(x):
    x = x.strip('$')
    try:
        return float(x)
    except ValueError:
        print("Not a number")
        return False


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    # output = BytesIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


def revert_secuirty_names(df):
    df.loc[df["Security Name"] == "common stock", "Security Name"] = "common"
    return df


def find_loc(text, triggers, allow_contains=True):
    for trigger in triggers:
        curIndex = find_target(text, trigger, allow_contains=allow_contains)
        if curIndex != []:
            if len(curIndex) > 1:
                pass
            #                 print("target occurs at multiple indicies")
            return curIndex
    #     print("No trigger found in text")
    return None


def get_filepath(target_filename):
    dropbox_path = "/Users/DanielLongo/Dropbox/VC RA Avinika Narayan/Contracts project/coi/Done OCR'd/"
    for root, dirs, files in os.walk(dropbox_path):
        for dir in dirs:
            for filename in os.listdir(dropbox_path + dir):
                if filename == target_filename:
                    return dropbox_path + dir + "/" + filename


def remove_periods(text):  # doesn't remove decimal places
    out = []
    for word in text:
        if is_num(word):
            out += [word]
            continue
        out += word.split('.')
    return out


def get_closest_string(values, target, less, any=False):
    if not any:
        if less:
            values = [x for x in values if x < target]
        else:
            values = [x for x in values if x > target]
    try:
        val = min(values, key=lambda x: abs(target - x))
    except ValueError:
        return -1
    return val


def find_target(text, target, allow_contains=True):
    target_loc = 0
    indicies = []
    start_index = 0
    between = 0
    between_max = 1
    for i in range(len(text)):
        word = text[i]
        if word == target[target_loc] or (allow_contains and target[target_loc] in word):
            # print(word, target[target_loc])
            if target_loc == 0:  # marks start of sequence
                start_index = i
            target_loc += 1
            if target_loc == len(target):
                indicies += [start_index]
                target_loc = 0
        elif word == target[0] or (allow_contains and target[0] in word):
            target_loc = 1
        else:
            if target_loc > 0:

                between += 1
                if between > between_max:
                    between = 0
                    # reset just incase ababcd
                    i -= (target_loc - 1)
                    target_loc = 0
    return indicies


def get_closest_num(values, target, less, min=-1, max=1e10000, any=False):
    try:
        index = int(target)
    except ValueError:
        indicies = find_target(values, target.split(" "))
        #         print("Indicies", indicies)
        if len(indicies) > 1:
            warnings.warn("Indicies length greath than one", RuntimeWarning)
            for i in range(len(indicies)):
                if less:
                    cur_target = indicies[i]
                else:
                    cur_target = indicies[len(indicies) - 1 - i]  # starts at end of doc
                cur_val = get_closest_num(values, cur_target, less, min=min, max=max, any=any)
                if (cur_val != None):
                    return cur_val
            warnings.warn("No number found", RuntimeWarning)
            print("No num found target:", target, "indicies:", indicies)
            return None
        #         assert(len(indicies) > 1), "Invalid target"
        index = indicies[-1]
    if any:  # doesn't get closest
        iters = range(0, len(values))
    elif less:
        iters = range(index - 1, -1, -1)  # 0 is last
    else:  # less = false
        iters = range(index, len(values))
    for i in iters:
        if (is_num(values[i])):
            return float(values[i].strip("$"))
    print("No num", target, "index", index)
    return None


def get_names_from_text(text, names):
    assert (type(text) == list), "Text is a list of strings"
    text = " ".join(text)
    used_names = {}
    for name in names:
        try:
            index = text.index(name)  # returns index of first occurrence
            used_names[name] = index
        except ValueError:  # Substring not found
            pass
    used_names = sorted(used_names.items(), key=lambda kv: kv[1])
    return used_names


def subsetSums(arr, l, r, sum=0):
    # print("subset Sums start")
    # from https://www.geeksforgeeks.org/print-sums-subsets-given-set/
    # Print current subset
    out = []
    if l > r:
        return sum

    # Subset including arr[l]
    out += [subsetSums(arr, l + 1, r, sum + arr[l])]

    # Subset excluding arr[l]
    out += [subsetSums(arr, l + 1, r, sum)]
    # print("subset Sums finish")
    return out


def remove_sums(nums_w_index):
    # TODO: Get better sum algorithm
    # removes values that are sums of values
    nums = [num[0] for num in nums_w_index]
    n = len(nums)
    sums = subsetSums(nums, 0, n - 1)
    sums = np.asarray(sums).flatten()
    sums = sums.tolist()
    out = []
    for num in nums_w_index:
        if sums.count(num[0]) == 1:
            out += [num]
    return out


def get_num_substring(x):
    # if x contains a numeric substring will return the number, else returns the string
    # TODO: ensure works properly with decimal points

    if is_num(x.strip("$")):
        return x.strip("$")
    start = 0
    end = -1
    first = True
    for i in range(len(x)):
        char = x[i]
        if char.isdigit():
            if first:
                start = i
                first = False
                continue
        elif not first:
            return x[start:i]

    return x[start:]


def get_nums_from_text(text, min=-1, max=sys.maxsize, decimal=False):
    assert (type(text) == list), "Text is a list of strings"
    str_text = " ".join(text)
    numbers = []
    loc = 0
    for word in text:
        loc += 1
        num_from_word = get_num_substring(word)
        if is_num(num_from_word):
            val = get_num(num_from_word)
            if min < val < max:
                if decimal or float(val).is_integer():  # checks if values behind decimal place
                    numbers += [(val, str_text.index(word), loc)]
    return numbers


# def get_nums_from_text(text, min=-1, max=sys.maxsize, decimal=False):
#     assert (type(text) == list), "Text is a list of strings"
#     str_text = " ".join(text)
#     numbers = []
#     for word in text:
#         # print(word, text.index(word))
#         # num_from_word = get_num_substring(word)
#         # print("num", num_from_word)
#         if is_num(word):
#             val = get_num(word)
#             if min < val < max:
#                 if decimal or float(val).is_integer():  # checks if values behind decimal place
#                     numbers += [(val, str_text.index(word))]
#     return numbers

def match_nums_with_targets(nums, targets, buffer=300, max_diff=200):
    min_index = targets[0][1] - buffer
    max_index = targets[-1][1] + buffer

    nums_in_range = []
    for num in nums:
        if min_index < num[1] < max_index:
            nums_in_range += [num]
    # print("Length of nums in range", len(nums_in_range))
    if len(nums_in_range) > 15:  # takes too long to run
        print("skipped")
        return None
    else:
        nums_in_range = remove_sums(nums_in_range)

    if len(targets) > len(nums_in_range):
        print('MORE  TARGETS THAN NUMS')
        # print("targets", targets)
        # print("Nums in range", nums_in_range)
        return

    out = []
    i = 0

    # if len(nums_in_range) == len(targets):
    #     print("IT'S A MATCH", len(nums_in_range))
    # else:
    #     return
    #     print("No MATCH")
    # prev_diff = 9999
    for target in targets:
        while i < len(nums_in_range):
            diff = abs(nums_in_range[i][1] - target[1])
            if diff < max_diff:
                out += [(target[0], nums_in_range[i][0])]
                i += 1
                break
            # if diff > prev_diff:
            #     out += [None]
            #     i += 1
            i += 1
    if len(out) != len(targets):
        # print("Unsuccessful match", out, targets)
        pass
    # print("SUCCESSFUL", out)
    return out


if __name__ == "__main__":
    # text = convert("./135_ActelisNetworks_COI_01072005.pdf", pages=[1])
    # print(text)
    get_filenames(3)
