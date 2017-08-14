#!/usr/bin/python
#coding:ut8

import sys, glob

def pdfparser(data):
    fp = file(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()
    return data

def procesa_archivo( D, archivo ):
    contenido = pdfparser(archivo)




if __name__=='__main__':
    L = glob.glob(sys.argv[1])
    cfdis = {}
    for f in L:
        procesa_archivo( cfdis )
