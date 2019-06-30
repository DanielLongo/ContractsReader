from load_contracts import preprocess_text, read_contract
from search_functions import get_text
from utils import find_loc


def get_board_of_directors_paras(doc_text):
    start_trigger = "election of directors"
    print(start_trigger)
    start_trigger = preprocess_text(start_trigger, stem=False).split(" ")
    print(start_trigger)
    loc = find_loc(doc_text, [start_trigger], allow_contains=True)
    for i in loc:
        print("sample")
        print(" ".join(doc_text[i: i + 10]))
        # TODO: review find_loc function given sample results

if __name__ == "__main__":
    doc_text = read_contract("../contracts/135_ActelisNetworks_COI_01072005.pdf", stem=False).split(" ")
    get_board_of_directors_paras(doc_text)