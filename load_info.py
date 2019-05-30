import pandas as pd
import numpy as np
from load_contracts import preprocess_text, read_contract
import xlrd


def load_info_xlsx(filename, np_array=True):
    df = pd.read_excel(filename)
    # print("DF", df.columns)
    out = pd.concat([df["File Name"], df["Security Name"], df["Number"], df["Security Type"]], axis=1)
    out = out[np.isfinite(df["Number"])]
    out = out.dropna(how='any')
    out["Security Name"] = out["Security Name"].apply(preprocess_text)
    out["Number"] = out["Number"].apply("{:.20g}".format).apply(str).apply(preprocess_text)
    if np_array:
        return out.values
    return out
    # print(out["File Name"])
    # print("out", out)
    # print(df["Security Name"].unique())


def generate_map(y, num_examples=10, filepath="./contracts/"):
    assert (y.shape[0] >= num_examples), "Not enough examples"
    for entry in y:
        cur_filename = entry[0]
        cur_name = entry[1]
        cur_number = entry[2]
        text = read_contract(filepath + cur_filename)
        matches_name = [(i, i + len(cur_name)) for i in range(len(text)) if text[i:i + len(cur_name)] == cur_name]
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


def get_map_from_file(filename, keys):
    file = filename.split("/")[-1]
    df = load_info_xlsx("rs1 database AN.xlsx", np_array=False)
    file_report = df.loc[df["File Name"] == file]
    out = pd.concat((file_report[key] for key in keys), axis=1)
    return out


if __name__ == "__main__":
    # y = load_info_xlsx("rs1 database AN.xlsx")
    # print("x shape", y.shape)
    # generate_map(y)
    filename = "contracts/135_ActelisNetworks_COI_01072005.pdf"
    print(get_map_from_file(filename, ["Security Name", "Number"]))
    print("Finished")
