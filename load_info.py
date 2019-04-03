import pandas as pd
import xlrd

def load_info_xlsx(filename):
    df = pd.read_excel(filename)
    out = pd.concat([df["File Name"], df["Security Name"], df["Number"]], axis=1)
    print(out["File Name"])
    # print("out", out)
    # print(df["Security Name"].unique())


if __name__ == "__main__":
    load_info_xlsx("rs1 database AN.xlsx")
    print("Finished")