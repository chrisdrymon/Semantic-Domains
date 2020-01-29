import pickle
import os
from bs4 import BeautifulSoup
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


for lemma in by_domain_dict['higher cognitive process']:
    print(lemma, by_lemma_dict[lemma])
