# from io import BytesIO
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


if __name__ == "__main__":
    text = convert("./135_ActelisNetworks_COI_01072005.pdf", pages=[1])
    print(text)
