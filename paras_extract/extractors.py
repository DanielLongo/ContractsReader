from load_contracts import preprocess_text, read_contract
from manage_triggers import get_proccessed_triggers
from search_functions import get_text, get_names, get_num_of_shares
from utils import find_loc, get_closest_string, get_names_from_text, get_nums_from_text
from itertools import product

def get_board_of_directors_paras(doc_text):
    # start_trigger = "election of directors"
    start_trigger = "director elect"
    start_trigger = preprocess_text(start_trigger, stem=False).split(" ")
    print(start_trigger)
    loc = find_loc(doc_text, [start_trigger], allow_contains=False)

    if loc is None:
        loc = find_loc(doc_text, [start_trigger], allow_contains=True)
        if loc is None:
            return "Failed to find directors info text"
    for i in loc:
        if i < 200:
            continue
        print(i)
        return " ".join(doc_text[i: i + 200])
        # TODO: review find_loc function given sample results
    return "Failed to find board of directors info text"


def get_securities_info_paras(doc_text, beginning_intro_triggers_filename="Beginning_IV",
                              end_intro_triggers_filename="End_IV_intro"):
    beginning_intro_triggers = get_proccessed_triggers(beginning_intro_triggers_filename, preproccess=False)
    end_intro_triggers = get_proccessed_triggers(end_intro_triggers_filename, preproccess=False)

    try:
        beginning_of_IV_intro = find_loc(doc_text, beginning_intro_triggers, allow_contains=True)
        end_of_IV_intro = find_loc(doc_text, end_intro_triggers)

    except TypeError:
        return "Failed to find securities info text"

    # In case triggers didn't work, search the entire document
    diffs = sorted(product(beginning_of_IV_intro, end_of_IV_intro), key=lambda t: abs(t[0] - t[1]))
    _, names = get_names(doc_text, stem=False)
    names_used = get_names_from_text(doc_text, names)
    names_used = " ".join([x[0] + ", " for x in names_used])[:-2]
    for dif in diffs:
        if dif[0] < dif[1]:
            return "Types of shares found: " + names_used + "\n" + " ".join(doc_text[dif[0]:dif[1]])
    return "Failed to find securities info text"

def get_dividend_paras(doc_text):
    start_trigger = "shall be entitled to receive dividends"
    start_trigger = preprocess_text(start_trigger, stem=False).split(" ")
    loc = find_loc(doc_text, [start_trigger], allow_contains=True)
    if loc is None:
        return "Failed to find dividend info text"
    loc = loc[0]
    numbers = get_nums_from_text(doc_text, min=0, max=1, decimal=True)
    start_found = False
    start = -1
    for i in range(len(numbers)):
        cur_num = numbers[i]
        if not start_found and cur_num[2] > loc:
            start = cur_num[2] - 10
            start_found = True
            continue
        if start_found:
            if (cur_num[2] - numbers[i - 1][2]) > 140: # value is too far aways
                end = numbers[i-2][2] + 20
                return " ".join(doc_text[start: end])

    if not start_found:
        return "Failed to find dividend info text"

    return " ".join(doc_text[start: numbers[-1][2] + 20])

def get_liquidation_paras(doc_text):
    start_triggers = ["event of any liquidation", "upon any such liquidation"]
    start_triggers = [preprocess_text(start_trigger, stem=False).split(" ") for start_trigger in start_triggers]
    start_locs = find_loc(doc_text, start_triggers, allow_contains=True)
    print(start_locs)
    print(len(doc_text))
    if start_locs is None or start_locs == []:
        return "Failed to find liquidation info text"
    for i in start_locs:
        if i > 200:
            out = " ".join(doc_text[i: i + 200])
            return out
    return "Failed to find liquidation info text"


    # print(beginning_of_IV_intro)
    # print(end_of_IV_intro)
    # if beginning_of_IV_intro is None:
    #     print("Beginning of IV intro is None")
    #     beginning_of_IV_intro = 0
    # if beginning_of_IV_intro[0] > end_of_IV_intro:
    #     print("End is less than beginning index of IV intro")
    #     beginning_of_IV_intro = [0]
    #     end_of_IV_intro = len(doc_text)
    #
    # # assert (beginning_of_IV_intro is not None), "Invalid info file " + " ".join(text) + filename
    # print(beginning_of_IV_intro)
    # print(end_of_IV_intro)
    # beginning_of_IV = get_closest_string(values=beginning_of_IV_intro, target=end_of_IV_intro, less=True)
    #
    # likely = True  # likely program worked
    # if beginning_of_IV == -1:
    #     likely = False
    #     beginning_of_IV = end_of_IV_intro - 300
    #
    # IV_intro_text = " ".join(doc_text[beginning_of_IV:end_of_IV_intro])
    # return IV_intro_text


if __name__ == "__main__":
    doc_text = read_contract("../contracts/135_ActelisNetworks_COI_01072005.pdf", stem=False).split(" ")
    get_board_of_directors_paras(doc_text)
