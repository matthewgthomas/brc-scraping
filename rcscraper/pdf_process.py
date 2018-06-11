
import sys
import tempfile
import os
import shutil

# Things from the subprocess module don't rely on the shell unless you
# explicitly ask for it and can accept a pre-split list of arguments,
# making calling subprocesses much safer.
# (If you really do need to split quoted stuff, use shlex.split() instead)
from subprocess import check_call

from PyPDF2 import PdfFileReader, PdfFileWriter

from tabula import read_pdf

def process(filename):
    name = filename.split(".")[0]
    with open(filename, "rb") as fn:
        inputpdf = PdfFileReader(fn)
        
        # decrypt the PDF if needed. Try to use PyPDF2's built-in decrypter...
        # ... but PyPDF2 can't handle 128-bit AES encryption so use qpdf instead
        # this code came from: https://github.com/mstamy2/PyPDF2/issues/53#issuecomment-134381407
        if inputpdf.isEncrypted:
            try:
                inputpdf.decrypt('')
                print("File decrypted using PyPDF2")
            except:
                # this block of code came from: https://github.com/mstamy2/PyPDF2/issues/53#issuecomment-273012479
                try:
                    # There are a lot of ways to mess up creating temporary files in a way
                    # that's free of race conditions, so just use mkdtemp() to safely
                    # create a temporary folder that only we have permission to work inside
                    # (We ask for it to be made in the same folder as filename because /tmp
                    #  might be on a different drive, which would make the final overwrite
                    #  into a slow "copy and delete" rather than a fast os.rename())
                    tempdir = tempfile.mkdtemp(dir=os.path.dirname(filename))

                    # I'm not sure if a qpdf failure could leave the file in a halfway
                    # state, so have it write to a temporary file instead of reading from one
                    temp_out = os.path.join(tempdir, 'qpdf_out.pdf')

                    # Avoid the shell when possible and integrate with Python errors
                    # (check_call() raises subprocess.CalledProcessError on nonzero exit)
                    check_call(['qpdf', "--password=", '--decrypt', filename, temp_out])

                    # I'm not sure if a qpdf failure could leave the file in a halfway
                    # state, so write to a temporary file and then use os.rename to
                    # overwrite the original atomically.
                    # (We use shutil.move instead of os.rename so it'll fall back to a copy
                    #  operation if the dir= argument to mkdtemp() gets removed)
                    shutil.move(temp_out, filename)
                    print("File decrypted using qpdf")
                finally:
                    # Delete all temporary files
                    shutil.rmtree(tempdir)
        
        for i in range(inputpdf.numPages):
            page = PdfFileWriter()
            page.addPage(inputpdf.getPage(i))
            page_io = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
            page.write(page_io)
            if page_io.read() is b"":
                continue
            try:
                df = read_pdf(page_io.name)
                if df is None:
                    continue
                page_io.close()
                try:
                    df.to_csv(f"{name}_page_{i+1}.csv")
                except:
                    pass
                os.remove(page_io.name)
            except:
                pass


if __name__ == "__main__":
    process(sys.argv[1])
