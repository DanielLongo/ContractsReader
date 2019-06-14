import pandas as pd
from load_info import get_map_from_file
from manage_triggers import get_proccessed_triggers
from search_functions import get_names, get_types, get_num_of_shares, get_IV_intro_text, get_text, \
    get_original_issue_price
from utils import revert_secuirty_names


def generate_stats(filename):
    print("filename", filename)
    text = get_text(filename)
    generated = generate_stats_from_text(text)
    return generated


def generate_stats_from_text(text):
    _, names = get_names(text)
    nums, names_used = get_num_of_shares(text, names)
    original_issue_prices, names_used = get_original_issue_price(text, names)
    if nums is None and names_used is None:
        return None
    types = get_types(names_used)
    d = {"Security Name": names_used, "Security Type": types, "Number": nums, "Original Issue Price": original_issue_prices}
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

