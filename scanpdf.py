import PyPDF2
import os 
import re
import sys


load_pdf = sys.argv[1]
read_pdf = PyPDF2.PdfFileReader(load_pdf)
page_count = read_pdf.getNumPages ()
first_page= read_pdf.getPage (0)
page_content=first_page.extractText()
page_content=page_content.replace('\n', ' \n')
splt = page_content.split('\n')
for i in range(len(splt)-1, -1, -1):
  if len(splt[i]) < 4:
    del splt[i]
  else:
    space = True
    for j in splt[i]:
      if j != ' ' and j != '\t':
        space = False
    if space:
      del splt[i]

print (splt)