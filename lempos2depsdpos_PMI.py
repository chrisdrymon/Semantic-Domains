# Given a lemma and part of speech, this returns the PMIs of the semantic domains of its dependants.

import pickle
import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent, give_dependents, semdom_poser, poser
from collections import Counter
import math

all_sem_dom_pos_dict = pickle.load(open('all_sem_dom_pos_dict.pickle', 'rb'))
original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)


# This is designed to modify the semantic preference dictionary for prepositions without an article.
def prep_no_art_dependent(sentence_words, f_head_counter, f_sem_pref_dict):
    for f_head_word in sentence_words:
        if f_head_word.has_attr('lemma'):
            if deaccent(f_head_word['lemma']).lower() == head_lemma and poser(f_head_word) == head_pos:
                f_head_counter += 1
                for f_dependent in give_dependents(sentence_words, f_head_word):
                    if f_dependent.has_attr('form'):
                        print(head_lemma, f_dependent['form'])
                    else:
                        print(head_lemma)
                    for f_sem_dom_pos in semdom_poser(f_dependent):
                        f_sem_pref_dict[f_sem_dom_pos] += 1
    return f_head_counter, f_sem_pref_dict


file_count = 0
head_counter = 0
corpus_tokens = 1107273
sem_pref_dict = Counter()
PMI_dict = {}

head_lemma = 'αντι'
head_pos = 'adposition'

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
            if len(tokens) > 0:
                head_counter, sem_pref_dict = prep_no_art_dependent(tokens, head_counter, sem_pref_dict)
            if len(words) > 0:
                head_counter, sem_pref_dict = prep_no_art_dependent(words, head_counter, sem_pref_dict)
        print(head_counter)
        xml_file.close()

for semantic_domain_pos in all_sem_dom_pos_dict:
    sem_dom_occurrence = all_sem_dom_pos_dict[semantic_domain_pos]
    if semantic_domain_pos in sem_pref_dict:
        mutual_occurrences = sem_pref_dict[semantic_domain_pos]
        PMI = math.log(mutual_occurrences / ((head_counter * sem_dom_occurrence) / corpus_tokens), 2)
        precision = '='
    else:
        PMI = math.log(1 / ((head_counter * sem_dom_occurrence) / corpus_tokens), 2)
        precision = '<'
        mutual_occurrences = 0
    PMI_dict[semantic_domain_pos] = [precision, PMI, mutual_occurrences, all_sem_dom_pos_dict[semantic_domain_pos]]
print(head_lemma, 'occurs', head_counter, 'times.')
os.chdir(original_folder)
filename_string = head_lemma + '_anything_sem_dom_PMIs.csv'
wiq_sem_dom_PMI = pd.DataFrame.from_dict(PMI_dict, orient='index', columns=['Precision', 'PMI', 'Co-occurrence',
                                                                            'Domain Occurrence'])
wiq_sem_dom_PMI.to_csv(filename_string)
