from generate_stats import generate_stats, generate_stats_from_text
from load_info import get_map_from_file
from search_functions import get_IV_intro_text
from utils import check_security_names_equal, get_index_security_names_equal, get_filenames

def eval_files(filenames):
    percent_security_name_valid = []
    stats_performance = []
    for filename in filenames:
        generated = generate_stats(filename)
        y = get_map_from_file(filename, ["Security Name", "Security Type", "Number"])
        cur_percent_security_name_valid, cur_stats_performance = eval_single_file(generated, y, print_results=False)
        if cur_percent_security_name_valid != None and cur_stats_performance != None:
            percent_security_name_valid += [cur_percent_security_name_valid]
            stats_performance += [cur_stats_performance]
    avg_percent_security_name_valid = sum(percent_security_name_valid) / len(percent_security_name_valid)
    print("Avg percent_security_name_valid", avg_percent_security_name_valid)

    print(stats_performance)
    flattened_stats_performance = [y for x in stats_performance for y in x]
    print(flattened_stats_performance)
    avg_stats_perfomance = sum(flattened_stats_performance) / len(flattened_stats_performance)
    print("Avg stats_performance", avg_stats_perfomance)


def eval_single_file(generated, y, print_results=True):
    security_name_valid = 0
    security_name_invalid = 0
    stats_performance = []
    for security_name in generated["Security Name"]:
        print("cur name", security_name)
        cur_security_name_valid = False
        for cur_security_name in list(y["Security Name"]):
            if check_security_names_equal(security_name, cur_security_name):
                cur_security_name_valid = True
        if cur_security_name_valid:
            security_name_valid += 1
            index = get_index_security_names_equal(security_name, generated["Security Name"])
            # index = generated["Security Name"][generated["Security Name"] == security_name].index[0]  # gets index of current row
            try:
                cur_stats_performance = eval_security_stats(generated.iloc[index], y.iloc[index])
            except (TypeError, IndexError):
                print("TYPE ERROR or Index Error",)
                print("index", index)
                print("generated", generated)
                print("y", y)
                return None, None
            stats_performance += [cur_stats_performance]
            stats_performance += [cur_stats_performance]
        else:
            if print_results:
                print(security_name, list(y["Security Name"]))
            security_name_invalid += 1
    try:
        percent_security_name_valid = 100 * (security_name_valid / (security_name_valid + security_name_invalid))
        flattened_stats_performance = [y for x in stats_performance for y in x]
        percent_stats_valid = 100 * sum(flattened_stats_performance) / len(flattened_stats_performance)
    except ZeroDivisionError:
        # TODO: Investigate cause of ZeroDivisionError
        print("Zero Division error")
        return None, None
    if print_results:
        print("Security Name Score", str(percent_security_name_valid) + "% |", "valid:", security_name_valid,
            "invalid:", security_name_invalid)
        print("Stats Score", str(percent_stats_valid) + "% |", "valid:", sum(flattened_stats_performance), "invalid",
            len(flattened_stats_performance) - sum(flattened_stats_performance))

    return percent_security_name_valid, stats_performance


def eval_security_stats(generated, y):
    out = []
    for stat, key in zip(generated, y):
        try:
            stat = float(stat)
            key = float(key)
            if (stat - key) == 0:
                out += [1]
                continue
        except ValueError:
            if stat == key:
                out += [1]
                continue
        out += [0]
    return out


if __name__ == "__main__":
    # filename = "contracts/135_ActelisNetworks_COI_01072005.pdf"
    # filename = "contracts/17445_955DREAMS_COI_01232012.pdf"
    filenames = get_filenames(10)
    eval_files(filenames)
    # for filename in filenames
    # IV_intro_text = get_IV_intro_text(filename)
    # generated = generate_stats_from_text(IV_intro_text)
    # y = get_map_from_file(filename, ["Security Name", "Security Type", "Number"])
    # eval(generated, y)
