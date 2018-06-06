
import sys
import tempfile
import os

from PyPDF2 import PdfFileReader, PdfFileWriter

from tabula import read_pdf


def process(filename):
    name = filename.split(".")[0]
    with open(filename, "rb") as fn:
        inputpdf = PdfFileReader(fn)
        for i in range(inputpdf.numPages):
            page = PdfFileWriter()
            page.addPage(inputpdf.getPage(i))
            page_io = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
            page.write(page_io)
            if page_io.read() is b"":
                continue
            try:
                df = read_pdf(page_io.name)
            except:
                pass
            if df is None:
                continue
            page_io.close()
            try:
                df.to_csv(f"{name}_page_{i+1}.csv")
            except:
                pass
            os.remove(page_io.name)

if __name__ == "__main__":
    process(sys.argv[1])
