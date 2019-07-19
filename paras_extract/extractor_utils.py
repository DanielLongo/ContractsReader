from fpdf import FPDF

def create_pdf(text_chuncks, filename, company_name=""):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 5, txt=company_name, align="C", border=1)
    for title, text in text_chuncks.items():
        print(text)
        pdf.multi_cell(0, 5)
        pdf.multi_cell(0, 5, txt=title, align="C")
        pdf.multi_cell(0, 5, txt=text)
        pdf.cell(0, 5, txt=("-"*300), align="C")
    pdf.output(filename)

if __name__ == "__main__":
    text_chuncks = {
        "share info": "lorum ipsum more here wer call the line method and pass it two pairs of x/y coordinates",
        "board of directos": "nates that represent the upper left corner of the drawing. Then you will want to pass in the width and height of the shape. The last argument you can pa",
    }
    filename = "sample_reports/test.pdf"

    create_pdf(text_chuncks, filename, company_name="A Company")