import pandas as pd

from load_info import get_map_from_file
from manage_triggers import get_proccessed_triggers
from search_functions import get_names, get_types, get_num_of_shares, get_IV_intro_text
from utils import revert_secuirty_names

def generate_stats(filename):
    # for filename in filenames:
    IV_intro_text = get_IV_intro_text(filename)
    generated = generate_stats_from_text(IV_intro_text)
    return generated


def generate_stats_from_text(IV_intro_text):
    _, names = get_names(IV_intro_text)
    nums, names_used = get_num_of_shares(IV_intro_text, names)
    types = get_types(names_used)
    d = {"Security Name": names_used, "Security Type": types, "Number": nums}
    df = pd.DataFrame(d)
    df = revert_secuirty_names(df)
    return df


if __name__ == "__main__":
    filename = "contracts/135_ActelisNetworks_COI_01072005.pdf"
    IV_intro_text = get_IV_intro_text(filename)
    stats = generate_stats(IV_intro_text)
    print("generated")
    print(stats)
    print("actual")
    print(get_map_from_file(filename, ["Security Name", "Security Type", "Number"]))

