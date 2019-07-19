from load_contracts import read_contract
from paras_extract.extractor_utils import create_pdf
from paras_extract.extractors import get_board_of_directors_paras, get_securities_info_paras, get_dividend_paras, \
    get_liquidation_paras
from utils import get_filenames


def extract_paras(filename, save_filepath="./sample_reports/"):
    info = {}
    doc_text = read_contract(filename, stem=False).split(" ")
    securities_info = get_securities_info_paras(doc_text)
    dividend_info = get_dividend_paras(doc_text)
    board_of_directors = get_board_of_directors_paras(doc_text)
    liquidation_paras = get_liquidation_paras(doc_text)
    info["Securities Info"] = securities_info
    info["Dividend Info"] = dividend_info
    info["Board of Directors"] = board_of_directors
    info["Liquidation Paras"] = liquidation_paras
    save_filename = save_filepath + "info-" + filename.split("/")[-1]
    create_pdf(info, filename=save_filename, company_name=filename.split("/")[-1][:-4])


if __name__ == "__main__":
    # filename = "../contracts/135_ActelisNetworks_COI_01072005.pdf"
    # filename = "../contracts/17445_955DREAMS_COI_01232012.pdf"
    # filename = "../contracts/gevo03262010.pdf"
    # filename = "~/Dropbox/"
    filenames = get_filenames(4)
    for file in filenames:
        print(file)
        extract_paras(file)
