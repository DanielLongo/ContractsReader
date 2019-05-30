from load_contracts import read_contract
from load_info import get_security_names
from manage_triggers import get_proccessed_triggers
from utils import find_target, get_closest_num, get_closest_string, find_loc

Failures = [
    "/Users/DanielLongo/Dropbox/VC RA Avinika Narayan/Contracts project/coi/Done OCR'd/ActiveSemi International/148_ActiveSemi_COI_11082010.pdf",
]


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


def get_num_of_shares(text, names):
    out = []
    names_used = []
    for name in names:
        # print("cur name", name)
        if name in " ".join(text):
            names_used += [name]
            out += [get_closest_num(text, name, less=True)]
        else:
            pass
            # out += [None]
    return out, names_used


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


def get_IV_intro_text(filename, beginning_intro_triggers_filename="Beginning_IV", end_intro_triggers_filename="End_IV_intro"):
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
    #         print("end IV sample", " ".join(text[end_of_IV_intro: end_of_IV_intro + 50])
    #         end_of_IV_intro = end_of_IV_intro[0]
    #         end_of_IV_intro =
    except TypeError:
        print("failed", filename)
        print(text)
        return None
    assert (beginning_of_IV_intro is not None), "Invalid info file " + " ".join(text) + filename

    #     assert(end_of_IV_intro != None), "END Sequence not found"
    #     articl_forth_occur = find_target(text, ["articl", "fourth"])
    #     assert(articl_forth_occur != None), "Article fourth Sequence not found"
    beginning_of_IV = get_closest_string(values=beginning_of_IV_intro, target=end_of_IV_intro, less=True)
    if beginning_of_IV == -1:
        print("no beginning found")
        beginning_of_IV = end_of_IV_intro - 100
    print("beginning", beginning_of_IV, "end", end_of_IV_intro)
    IV_intro_text = text[beginning_of_IV:end_of_IV_intro]
    # print(" ".join(IV_intro_text))
    return IV_intro_text
