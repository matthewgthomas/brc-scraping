
import sys
import tempfile

from PyPDF2 import PdfFileReader, PdfFileWriter

from tabula import read_pdf


def process(filename):
    name = filename.split(".")[0]
    with open(filename, "rb") as fn:
        inputpdf = PdfFileReader(fn)
        for i in range(inputpdf.numPages):
            page = PdfFileWriter()
            page.addPage(inputpdf.getPage(i))
            page_io = tempfile.NamedTemporaryFile(mode="w+b")
            page.write(page_io)
            if page_io.read() is b"":
                continue
            df = read_pdf(page_io.name)
            if df is None:
                continue
            try:
                df.to_csv(f"{name}_page_{i+1}.csv")
            except:
                pass

if __name__ == "__main__":
    process(sys.argv[1])
