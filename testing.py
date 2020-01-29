import pickle
import os
from bs4 import BeautifulSoup
from bs4.formatter import XMLFormatter
import pandas as pd
from utility import deaccent
from collections import Counter
import math
import time


by_domain_dict = pickle.load(open('by_domain_dictionary.pickle', 'rb'))
by_lemma_dict = pickle.load(open('by_lemma_dictionary.pickle', 'rb'))
all_sem_dom_pos_dict = pickle.load(open('all_sem_dom_pos_dict.pickle', 'rb'))
original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)
pos0_dict = {'a': 'adj', 'n': 'noun', 'v': 'verb', 'd': 'adv', 'c': 'conj', 'g': 'conj', 'r': 'adposition', 'b': 'conj',
             'p': 'pronoun', 'l': 'article', 'i': 'interjection', 'x': 'other', 'm': 'numeral', 'e': 'interjection'}
pos2_dict = {'s': 'singular', 'p': 'plural', 'd': 'dual'}
pos4_dict = {'i': 'indicative', 's': 'subjunctive', 'n': 'infinitive', 'm': 'imperative', 'p': 'participle',
             'o': 'optative'}
proiel_pos_dict = {'A': 'adj', 'D': 'adv', 'S': 'article', 'M': 'numeral', 'N': 'noun', 'C': 'conj', 'G': 'conj',
                   'P': 'pronoun', 'I': 'interjection', 'R': 'adposition', 'V': 'verb'}

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
                new_order = []
                if 'id' in word.attrs:
                    new_order.append(('id', word['id']))
                if 'head' in word.attrs:
                    new_order.append(('head', word['head']))
                if 'head-id' in word.attrs:
                    new_order.append(('head-id', word['head-id']))
                if 'postag' in word.attrs:
                    new_order.append(('postag', word['postag']))
                if 'morphology' in word.attrs:
                    new_order.append(('morphology', word['morphology']))
                if 'relation' in word.attrs:
                    new_order.append(('relation', word['relation']))
                if 'form' in word.attrs:
                    new_order.append(('form', word['form']))
                if 'lemma' in word.attrs:
                    new_order.append(('lemma', word['lemma']))
                for pair in word.attrs.items():
                    if pair not in new_order:
                        new_order.append(pair)
                print(sorted(word.attrs.items()))
                print(new_order)
                time.sleep(5)
