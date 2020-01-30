import pickle
import os
from bs4 import BeautifulSoup
from bs4.formatter import XMLFormatter
from bs4 import UnicodeDammit
import pandas as pd
from utility import deaccent
from collections import Counter
import math
import time


class SortAttributes(XMLFormatter):
    def attributes(self, tag):
        """Reorder a tag's attributes however you want."""
        attrib_order = ['id', 'head', 'head-id', 'postag', 'morphology', 'relation', 'form', 'lemma']
        new_order = []
        for element in attrib_order:
            if element in tag.attrs:
                new_order.append((element, tag[element]))
        for pair in tag.attrs.items():
            if pair not in new_order:
                new_order.append(pair)
        return new_order


by_domain_dict = pickle.load(open('by_domain_dictionary.pickle', 'rb'))
by_lemma_dict = pickle.load(open('by_lemma_dictionary.pickle', 'rb'))
all_sem_dom_pos_dict = pickle.load(open('all_sem_dom_pos_dict.pickle', 'rb'))
original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)

file_count = 0
file = indir[4]
print(file, file_count)
greek_file = open(file, 'r', encoding='utf-8')
greek_text = BeautifulSoup(greek_file, 'xml')
new_text = greek_text.encode(formatter=SortAttributes())
greek_file.close()
print(attr_soup.p.encode(formatter=UnsortedAttributes()))
with open(file, 'w') as writefile:
    writefile.write(str(new_text))
