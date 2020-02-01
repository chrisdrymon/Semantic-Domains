# Given a lemma, this returns the PMI of the parts of speech that act as its head.

import os
import math
import pickle
from tabulate import tabulate
from bs4 import BeautifulSoup
from collections import Counter
from utility import deaccent, header, poser

original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)

all_pos_dict = pickle.load(open('all_pos_count.pickle', 'rb'))
pos0_dict = {'a': 'adj', 'n': 'noun', 'v': 'verb', 'd': 'adv', 'c': 'conj', 'g': 'conj', 'r': 'adposition', 'b': 'conj',
             'p': 'pronoun', 'l': 'article', 'i': 'interjection', 'x': 'other', 'm': 'numeral', 'e': 'interjection'}
pos4_dict = {'i': 'indicative', 's': 'subjunctive', 'n': 'infinitive', 'm': 'imperative', 'p': 'participle',
             'o': 'optative'}
agdt2_rel_dict = {'obj': 'object'}
proiel_pos_dict = {'A': 'adj', 'D': 'adv', 'S': 'article', 'M': 'numeral', 'N': 'noun', 'C': 'conj', 'G': 'conj',
                   'P': 'pronoun', 'I': 'interjection', 'R': 'adposition', 'V': 'verb'}

file_count = 0
dependent_count = 0
pos_dict = Counter()
corpus_tokens = 1107273
PMI_dict = {}
dependent_lemma = 'εν'

for file in indir:
    if file[-4:] == '.xml':
        file_count += 1
        print(file_count, file)
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        sentences = soup.find_all('sentence')
        for sentence in sentences:
            tokens = sentence.find_all(['word', 'token'])
            for token in tokens:
                if token.has_attr('lemma'):
                    if deaccent(token['lemma']).lower() == dependent_lemma:
                        dependent_count += 1
                        head = header(tokens, token)
                        if head == 'no head':
                            pos = 'no head'
                        else:
                            pos = poser(head)
                        if pos in pos_dict:
                            pos_dict[pos] += 1
                        else:
                            pos_dict[pos] = 1
        print(pos_dict)

for key in all_pos_dict:
    pos_occurrence = all_pos_dict[key]
    if key in pos_dict:
        mutual_occurrence = pos_dict[key]
        PMI = math.log(mutual_occurrence / ((dependent_count * pos_occurrence) / corpus_tokens), 2)
        precision = '='
    else:
        mutual_occurrence = 0
        PMI = math.log(1 / ((dependent_count * pos_occurrence) / corpus_tokens), 2)
        precision = '<'
    PMI_dict[key] = [precision, round(PMI, 2), mutual_occurrence, pos_occurrence]
print(dependent_lemma, 'occurs', dependent_count, 'times.')
os.chdir(original_folder)

tableform = [['POS', 'p', 'PMI', 'Mutual', 'Tot POS']]
for key in PMI_dict:
    new_list = [key] + PMI_dict[key]
    tableform.append(new_list)
print(tabulate(tableform, headers='firstrow', tablefmt='pipe'))
