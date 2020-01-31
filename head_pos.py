import os
import math
import pickle
import pandas as pd
from tabulate import tabulate
from bs4 import BeautifulSoup
from collections import Counter
from utility import deaccent

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


# This returns the head of the word
def header(f_sentence, f_word):
    return_head = 'no head'
    f_head_id = 0
    if f_word.has_attr('head'):
        f_head_id = f_word['head']
    if f_word.has_attr('head-id'):
        f_head_id = f_word['head-id']
    for f_head in f_sentence:
        if f_head.has_attr('id'):
            if f_head['id'] == f_head_id:
                return_head = f_head
    return return_head


# This returns the part-of-speech or the mood if the part-of-speech is a verb for a given word.
def poser(f_word):
    if f_word.has_attr('postag'):
        if len(f_word['postag']) > 0:
            pos0 = f_word['postag'][0]
            if pos0 in pos0_dict:
                f_pos = pos0_dict[pos0]
                if f_pos == 'verb':
                    if len(f_word['postag']) > 4:
                        pos4 = f_word['postag'][4]
                        if pos4 in pos4_dict:
                            f_pos = pos4_dict[pos4]
            else:
                f_pos = 'other'
        else:
            f_pos = 'other'
    elif f_word.has_attr('part-of-speech'):
        if len(f_word['part-of-speech']) > 0:
            pos0 = f_word['part-of-speech'][0]
            if pos0 in proiel_pos_dict:
                f_pos = proiel_pos_dict[pos0]
                if f_pos == 'verb':
                    if len(f_word['morphology']) > 3:
                        pos3 = f_word['morphology'][3]
                        if pos3 in pos4_dict:
                            f_pos = pos4_dict[pos3]
            else:
                f_pos = 'other'
        else:
            f_pos = 'other'
    else:
        f_pos = 'other'
    return f_pos


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
filename_string = 'pos_' + dependent_lemma + '_PMIs.csv'
wiq_sem_dom_PMI = pd.DataFrame.from_dict(PMI_dict, orient='index', columns=['Precision', 'PMI', 'Co-occurrence',
                                                                            'POS Occurrence'])
tableform = [['POS', 'p', 'PMI', 'Mutual', 'Tot POS']]
for key in PMI_dict:
    new_list = [key] + PMI_dict[key]
    tableform.append(new_list)
print(tabulate(tableform, headers='firstrow', tablefmt='pipe'))
