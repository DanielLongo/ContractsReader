# from io import BytesIO
import warnings
from io import StringIO
import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys
import getopt


# from http://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/
# converts pdf, returns its text content as a string

def is_num(x):
    x = x.strip('$')
    try:
        float(x)
    except ValueError:
        return False
    return True


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
    for i in range(len(text)):
        word = text[i]
        #         print("target_loc", target_loc)
        if word == target[target_loc] or (allow_contains and word in target[target_loc]):
            if target_loc == 0:  # marks start of sequence
                start_index = i
            target_loc += 1
            if target_loc == len(target):
                indicies += [start_index]
                target_loc = 0
        elif word == target[0] or (allow_contains and word in target[0]):
            target_loc = 1
        else:
            if target_loc > 0:
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


if __name__ == "__main__":
    text = convert("./135_ActelisNetworks_COI_01072005.pdf", pages=[1])
    print(text)
