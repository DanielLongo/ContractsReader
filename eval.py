from generate_stats import generate_stats
from load_info import get_map_from_file
from search_functions import get_IV_intro_text


def eval(generated, y):
    security_name_valid = 0
    security_name_invalid = 0
    stats_performance = []
    for security_name in generated["Security Name"]:
        print("cur name", security_name)
        if security_name in list(y["Security Name"]):
            security_name_valid += 1
            index = generated["Security Name"][generated["Security Name"] == security_name].index[
                0]  # gets index of current row
            cur_stats_performance = eval_security_stats(generated.iloc[index], y.iloc[index])
            stats_performance += [cur_stats_performance]
        else:
            # TODO Handle name variations. E.G. seri seed prefer stock ['common', 'seri seed prefer']
            print(security_name, list(y["Security Name"]))
            security_name_invalid += 1
    percent_security_name_valid = 100 * (security_name_valid / (security_name_valid + security_name_invalid))
    print("Security Name Score", str(percent_security_name_valid) + "% |", "valid:", security_name_valid,
          "invalid:", security_name_invalid)
    flattened_stats_performance = [y for x in stats_performance for y in x]
    percent_stats_valid = 100 * sum(flattened_stats_performance) / len(flattened_stats_performance)
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
    filename = "contracts/17445_955DREAMS_COI_01232012.pdf"
    IV_intro_text = get_IV_intro_text(filename)
    generated = generate_stats(IV_intro_text)
    y = get_map_from_file(filename, ["Security Name", "Security Type", "Number"])
    eval(generated, y)
