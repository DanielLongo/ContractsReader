from load_contracts import read_contract
from load_info import get_security_names
from manage_triggers import get_proccessed_triggers
from utils import find_target, get_closest_num, get_closest_string, find_loc, get_names_from_text, get_nums_from_text

Failures = [
    "/Users/DanielLongo/Dropbox/VC RA Avinika Narayan/Contracts project/coi/Done OCR'd/ActiveSemi International/148_ActiveSemi_COI_11082010.pdf",
]


def get_text(filename):
    # TODO: place this function elsewhere
    text = read_contract(filename)
    text = text.split(" ")
    return text


def get_names(text):
    unsplit_names = get_security_names()
    names = [name.split(" ") for name in unsplit_names]
    indicies = []
    types = []
    for name in names:
        if (len(name) == 1):
            name += ["stock"]
        cur_indicies = find_target(text, name)
        if len(cur_indicies) > 0:
            types += [" ".join(name)]
            indicies += [cur_indicies]
    # remove extra "preferred stock"
    has_extra_preferred = True
    if "prefer stock" in types:
        for type in types:
            if type[-6:] == 'prefer':
                has_extra_preferred = True
                break
        if has_extra_preferred:
            indicies.pop(types.index('prefer stock'))
            types.remove('prefer stock')
    return indicies, types


def get_num_of_shares(text, names, buffer=10):
    # buffer is the num of words possible between endpoint names and nums
    # TODO: work out discrepencies between number of names and number of nums
    # TODO: match up nums with share names
    used_names = get_names_from_text(text, names)
    start = used_names[0][1] - buffer
    end = used_names[-1][1] + buffer
    if start < 0:
        start = 0
    if end > len(text):
        end = len(text)
    print("start", start, "end", end)
    text = text[start: end]
    numbers = get_nums_from_text(text, min=100)
    print("names new", used_names, len(used_names))
    print("nums", numbers, len(numbers))


# def get_num_of_shares(text, names):
#     out = []
#     names_used = []
#     for name in names:
#         # print("cur name", name)
#         if name in " ".join(text):
#             names_used += [name]
#             if get_closest_num(text, name, less=True) is None:
#                 out += [get_closest_num(text, name, less=False)]
#             else:
#                 out += [get_closest_num(text, name, less=True)]
#
#         else:
#             pass
#             # out += [None]
#     return out, names_used


def get_types(names):
    types = []
    for name in names:
        if "common" in name:
            types += ["Common"]
        elif "prefer" in name:
            types += ["Preferred"]
        else:
            print("name doesn't contain common or prefer:", "".join(name))
            types += ["No type found"]
    return types


def get_IV_intro_text(filename, beginning_intro_triggers_filename="Beginning_IV",
                      end_intro_triggers_filename="End_IV_intro"):
    beginning_intro_triggers = get_proccessed_triggers(beginning_intro_triggers_filename)
    end_intro_triggers = get_proccessed_triggers(end_intro_triggers_filename)
    text = read_contract(filename)
    text = text.split(" ")
    #     print("text", text)
    #     text = text.split(" ")
    #     text = remove_periods(text)

    if filename in Failures:
        return "Failure expected"
    try:
        beginning_of_IV_intro = find_loc(text, beginning_intro_triggers, allow_contains=False)
        end_of_IV_intro = find_loc(text, end_intro_triggers)[0]

    except TypeError:
        print("failed", filename)
        print(text)
        return None

    # In case triggers didn't work, search the entire document

    if beginning_of_IV_intro is None:
        print("Beginning of IV intro is None")
        beginning_of_IV_intro = 0
    if beginning_of_IV_intro[0] > end_of_IV_intro:
        print("End is less than beginning index of IV intro")
        beginning_of_IV_intro = [0]
        end_of_IV_intro = len(text)

    # assert (beginning_of_IV_intro is not None), "Invalid info file " + " ".join(text) + filename

    beginning_of_IV = get_closest_string(values=beginning_of_IV_intro, target=end_of_IV_intro, less=True)

    if beginning_of_IV == -1:
        print("no beginning found")
        beginning_of_IV = end_of_IV_intro - 300

    IV_intro_text = text[beginning_of_IV:end_of_IV_intro]
    return IV_intro_text
