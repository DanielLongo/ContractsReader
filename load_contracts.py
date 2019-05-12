import string
from utils import convert
from vectorizers import count_vectorizer
import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import sys
from utils import is_num
# import slate3k

# keep the $ sign and .
chars_to_remove = string.punctuation.replace("$", "").replace(".", "")
remove_chars = str.maketrans(chars_to_remove, " " * len(chars_to_remove))

def remove_periods(text): #doesn't remove decimal places
    out = []
    for word in text:
        if is_num(word):
            out += [word]
            continue
        out += word.split('.')
    return out

def preprocess_text(text):
    text = text.lower()
    text = text.replace("\n", "")
    text = text.replace(". ", " ")
    text = text.replace(",", "")
    text = text.encode('ascii', errors='ignore').decode('utf-8')
    text = text.translate(remove_chars)
    ps = PorterStemmer()
    tokens = [ps.stem(word) for word in text.split(" ")]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    tokens = list(filter(lambda a: a != '', tokens))
    tokens = remove_periods(tokens)
    
    return " ".join(tokens)
    # text = text.strip()
    # stop_words = set(stopwords.words('english'))
    # tokens = word_tokenize(text)
    # tokens = [i for i in tokens if not i in stop_words]
    # ps = PorterStemmer()
    # tokens = [ps.stem(word) for word in tokens]
    # lemmatizer = WordNetLemmatizer()
    # tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # tokens = tokens[:-1]
    # return tokens#, tokens


def read_contract(filename):
    file = open(filename, "rb")
    read_file = PyPDF2.PdfFileReader(file)
    num_pages = read_file.getNumPages()
    final_string = ""
    for i in range(num_pages):
        text = convert(filename, pages=[i])
        string = preprocess_text(text)
        final_string += string + " "
    # final = " ".join(final_string)
    return final_string


if __name__ == "__main__":
    # print("hello")
    loc = "contracts/"
    string = []
    string += [read_contract(loc + "135_ActelisNetworks_COI_01072005.pdf")]
    string += [read_contract(loc + "17445_955DREAMS_COI_01232012.pdf")]

    v = count_vectorizer(string)
    x = v.transform(string).toarray()
    print(type(x), len(x))
    print(x[0].shape)
