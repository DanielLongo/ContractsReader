import pandas as pd

from load_info import get_map_from_file
from manage_triggers import get_proccessed_triggers
from search_functions import get_names, get_types, get_num_of_shares, get_IV_intro_text
from utils import revert_secuirty_names


def generate_stats(IV_intro_text):
    _, names = get_names(IV_intro_text)
    types = get_types(names)
    nums = get_num_of_shares(IV_intro_text, names)
    d = {"Security Name": names, "Security Type": types, "Number": nums}
    df = pd.DataFrame(d)
    df = revert_secuirty_names(df)
    return df


if __name__ == "__main__":
    BEGINNING_OF_IV_INTRO_TEXT = get_proccessed_triggers("Begining_IV")
    END_OF_IV_INTRO_TEXT = get_proccessed_triggers("End_IV_intro")
    filename = "contracts/135_ActelisNetworks_COI_01072005.pdf"
    IV_intro_test = get_IV_intro_text(filename, BEGINNING_OF_IV_INTRO_TEXT, END_OF_IV_INTRO_TEXT)
    stats = generate_stats(IV_intro_test)
    print("generated")
    print(stats)
    print("actual")
    print(get_map_from_file(filename, ["Security Name", "Number"]))

