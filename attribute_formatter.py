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
        new_order = []
        if 'id' in tag.attrs:
            new_order.append(('id', tag['id']))
        if 'head' in tag.attrs:
            new_order.append(('head', tag['head']))
        if 'head-id' in tag.attrs:
            new_order.append(('head-id', tag['head-id']))
        if 'postag' in tag.attrs:
            new_order.append(('postag', tag['postag']))
        if 'morphology' in tag.attrs:
            new_order.append(('morphology', tag['morphology']))
        if 'relation' in tag.attrs:
            new_order.append(('relation', tag['relation']))
        if 'form' in tag.attrs:
            new_order.append(('form', tag['form']))
        if 'lemma' in tag.attrs:
            new_order.append(('lemma', tag['lemma']))
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

for file in indir:
    if file[-4:] == '.xml':
        file_count += 1
        print(file_count, file)
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        sentences = soup.find_all('sentence')
        for sentence in sentences:
            tokens = sentence.find_all('token')
            words = sentence.find_all('word')
            for word in words:
                dammit = UnicodeDammit(word.encode(formatter=SortAttributes()))
                print(dammit.unicode_markup)
                time.sleep(5)


