from features_extract.generate_stats import generate_stats
from load_info import get_map_from_file
from utils import check_security_names_equal, get_index_security_names_equal, get_filenames
import numpy as np


# def eval_files(filenames):
#     percent_security_name_valid = []
#     stats_performance = []
#     successful_run = []
#     for filename in filenames:
#         generated = generate_stats(filename)
#         y = get_map_from_file(filename, ["Security Name", "Security Type", "Number"])
#         cur_percent_security_name_valid, cur_stats_performance, cur_successful_run = eval_single_file(generated, y,
#                                                                                                       print_results=False)
#         successful_run += [cur_successful_run]
#         if cur_percent_security_name_valid != None and cur_stats_performance != None:
#             percent_security_name_valid += [cur_percent_security_name_valid]
#             stats_performance += [cur_stats_performance]
#     avg_percent_security_name_valid = sum(percent_security_name_valid) / len(percent_security_name_valid)
#     print("Avg percent_security_name_valid", avg_percent_security_name_valid)
#
#     flattened_stats_performance = [z for x in stats_performance for y in x for z in y]
#     avg_stats_perfomance = sum(flattened_stats_performance) / len(flattened_stats_performance)
#     print("Avg stats_performance", avg_stats_perfomance)
#     avg_successful_run = sum(successful_run) / len(successful_run)
#     print("Avg successful run", avg_successful_run)


def check_security_names_valid(names_extracted, names_real):
    if len(names_extracted) != len(names_real):
        return False
    for name_extracted in names_extracted:
        cur_name_valid = False
        for name_real in names_real:
            if check_security_names_equal(name_real, name_extracted):
                cur_name_valid = True
                break
        if not cur_name_valid:
            return False
    return True


def print_stats_summary(stats):
    keys = stats[0]
    stats.pop(0)
    print("stats", stats)
    stats = np.asarray(stats)
    print("stats shape", stats.shape)


def eval_files(filenames):
    invalid_security_names = 0
    keys = ["Security Name", "Security Type", "Number"]
    stats = [keys]
    for file in filenames:
        generated = generate_stats(file)
        if generated is None:
            continue
        y = get_map_from_file(file, stats[0])
        cur_stats = eval_file(generated, y)
        if not cur_stats:
            invalid_security_names += 1
            continue
        stats += cur_stats

    print_stats_summary(stats)


def eval_file(generated, y):
    if not check_security_names_valid(generated["Security Name"], y["Security Name"]):
        print("Security Names invalid")
        return False

    stats_performance = []
    for i in range(len(generated["Security Name"])):
        cur_stats_performance = eval_security_stats(generated.iloc[i], y.iloc[i])
        stats_performance += [cur_stats_performance]

    return stats_performance


# def eval_single_file(generated, y, print_results=True):
#     if generated is None:
#         return None, None, False
#     security_name_valid = 0
#     security_name_invalid = 0
#     stats_performance = []
#     for security_name in generated["Security Name"]:
#         cur_security_name_valid = False
#         for cur_security_name in list(y["Security Name"]):
#             # cur is real
#             if check_security_names_equal(security_name, cur_security_name):
#                 cur_security_name_valid = True
#         if cur_security_name_valid:
#             security_name_valid += 1
#             index = get_index_security_names_equal(security_name, generated["Security Name"])
#             # index = generated["Security Name"][generated["Security Name"] == security_name].index[0]  # gets index of current row
#             try:
#                 cur_stats_performance = eval_security_stats(generated.iloc[index], y.iloc[index])
#             except (TypeError, IndexError):
#                 print("TYPE ERROR or Index Error", )
#                 print("index", index)
#                 print("generated", generated)
#                 print("y", y)
#                 return None, None, False
#             stats_performance += [cur_stats_performance]
#             stats_performance += [cur_stats_performance]
#         else:
#             if print_results:
#                 print(security_name, list(y["Security Name"]))
#             security_name_invalid += 1
#     try:
#         percent_security_name_valid = 100 * (security_name_valid / (security_name_valid + security_name_invalid))
#         flattened_stats_performance = [y for x in stats_performance for y in x]
#         percent_stats_valid = 100 * sum(flattened_stats_performance) / len(flattened_stats_performance)
#     except ZeroDivisionError:
#         # TODO: Investigate cause of ZeroDivisionError
#         print("Zero Division error")
#         return None, None, False
#     if print_results:
#         print("Security Name Score", str(percent_security_name_valid) + "% |", "valid:", security_name_valid,
#               "invalid:", security_name_invalid)
#         print("Stats Score", str(percent_stats_valid) + "% |", "valid:", sum(flattened_stats_performance), "invalid",
#               len(flattened_stats_performance) - sum(flattened_stats_performance))
#
#     return percent_security_name_valid, stats_performance, True


def eval_security_stats(generated, y):
    out = []
    for stat, key in zip(generated, y):
        if stat is None:
            out += [None]
        try:
            stat = float(stat)
            key = float(key)
            if (stat - key) == 0:
                out += [1]
                continue
        except ValueError:
            print("value error", stat, key)
            if stat == key:
                out += [1]
                continue
        out += [0]
    print("out", out)
    return out


if __name__ == "__main__":
    filenames = get_filenames(5)
    # filenames = ["/Users/DanielLongo/Dropbox/VC RA Avinika Narayan/Contracts project/coi/Done OCR'd/Kabbage/15866_Kabbage_COI_06302015.pdf"]
    # filenames = ["/Users/DanielLongo/Dropbox/VC RA Avinika Narayan/Contracts project/coi/Done OCR'd/Veralight/veralight_inc072806.pdf"]
    eval_files(filenames)
