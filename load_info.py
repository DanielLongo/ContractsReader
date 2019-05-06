import pandas as pd
import numpy as np
from load_contracts import preprocess_text, read_contract
import xlrd

def load_info_xlsx(filename):
    df = pd.read_excel(filename)
    out = pd.concat([df["File Name"], df["Security Name"], df["Number"]], axis=1)
    out = out[np.isfinite(df["Number"])]
    out = out.dropna(how='any')
    out["Security Name"] = out["Security Name"].apply(preprocess_text)
    out["Number"] = out["Number"].apply("{:.20g}".format).apply(str).apply(preprocess_text)
    return out.values
    # print(out["File Name"])
    # print("out", out)
    # print(df["Security Name"].unique())

def generate_map(y, num_examples=10, filepath="./contracts/"):
    assert(y.shape[0] >= num_examples), "Not enough examples"
    for entry in y:
        cur_filename = entry[0]
        cur_name = entry[1]
        cur_number = entry[2]
        text = read_contract(filepath + cur_filename)
        matches_name = [(i, i+len(cur_name)) for i in range(len(text)) if text[i:i+len(cur_name)] == cur_name]
        for match in matches_name:
            print(match)
            print(text[match[0]:match[1]])
        print(entry)


def get_security_names(key="Security Name", filename="rs1 database AN.xlsx"):
    df = pd.read_excel(filename)
    out = pd.concat([df["File Name"], df["Security Name"], df["Number"]], axis=1)
    out = out[np.isfinite(df["Number"])]
    out = out.dropna(how='any')
    out["Security Name"] = out["Security Name"].apply(preprocess_text)
    out = out[key].unique()
    return out


if __name__ == "__main__":
    y = load_info_xlsx("rs1 database AN.xlsx")
    print("x shape", y.shape)
    generate_map(y)
    print("Finished")