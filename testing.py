import pickle
import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent
from collections import Counter
import math
import time
from bs4.formatter import XMLFormatter


def grammatical_number(f_word):
    gram_num = 'other'
    if f_word.has_attr('postag'):
        if len(f_word['postag']) > 2:
            pos2 = f_word['postag'][2]
            if pos2 in pos2_dict:
                gram_num = pos2_dict[pos2]
    if f_word.has_attr('morphology'):
        if len(f_word['morphology']) > 1:
            pos1 = f_word['morphology'][1]
            if pos1 in pos2_dict:
                gram_num = pos2_dict[pos1]
    return gram_num


folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 0
pos2_dict = {'s': 'singular', 'p': 'plural', 'd': 'dual'}

for file in indir:
    if file[-4:] == '.xml' and file[:3] == 'new':
        print(file)
        file_count += 1
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        sentences = soup.find_all('sentence')
        for sentence in sentences:
            tokens = sentence.find_all('token')
            words = sentence.find_all('word')
            for token in tokens:
                try:
                    print(token['form'], grammatical_number(token))
                    time.sleep(0.7)
                except KeyError:
                    pass
