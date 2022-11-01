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


import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
nltk.download('stopwords')
from IPython import display
from collections import Counter
import math

Finance_List = ['facture', 'bon', 'cheque','devis']

HR_List = ['carte','identite','attestation']



all_stopwords = stopwords.words('english')
all_stopwords.append('‘')
all_stopwords.append('“')
all_stopwords.append('’')
all_stopwords.append(',')
all_stopwords.append('.')
all_stopwords.append('”')
all_stopwords.append(' ')
all_stopwords.append('second')
all_stopwords.append('first')
all_stopwords.append('third')
all_stopwords.append('me')
all_stopwords.append('us')
all_stopwords.append('I')
all_stopwords.append('he')
all_stopwords.append('she')
all_stopwords.append('they')
all_stopwords.append('we')

names_lower=[]
for name in splt:
    names_lower.append(name.lower())

tokens_without_sw = [word for word in names_lower if not word in all_stopwords]
new_text = " ".join(tokens_without_sw)
new_text

counter_data_set = Counter(names_lower)
counter_HR_List = Counter(HR_List)
counter_Finance_List = Counter(Finance_List)



def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def length_similarity(c1, c2):
    lenc1 = sum(c1.values())
    lenc2 = sum(c2.values())
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))

def similarity_score(l1, l2):
    c1, c2 = Counter(l1), Counter(l2)
    return length_similarity(c1, c2) * counter_cosine_similarity(c1, c2)


counter_cosine_similarity_HR_List = counter_cosine_similarity(counter_data_set, counter_HR_List)
counter_cosine_similarity_Finance_List = counter_cosine_similarity(counter_data_set, counter_Finance_List)


Rst_HR_List = similarity_score(tokens_without_sw,HR_List) + counter_cosine_similarity_HR_List

Rst_Finance_List = similarity_score(tokens_without_sw,Finance_List) + counter_cosine_similarity_Finance_List

"""###**validation method**"""

rst = []
rst.append(Rst_HR_List)
rst.append(Rst_Finance_List)

ch=""
if 'facture' in new_text:
    ch = "Finance Department"
elif 'bon' in new_text:
        ch = "Finance Department"
elif 'invoice' in new_text:
        ch = "Finance Department"
elif 'cheque' in new_text:
        ch = "Finance Department"
elif 'devis' in new_text:
        ch = "Finance Department"
else:
    ch = "HR Department"

print(ch)
