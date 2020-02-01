# Given a lemma and part of speech; and the lemma, number, and part of speech of its dependent's dependent, this will
# return the PMIs of the dependant's semantic domains so long as the dependent's dependent has the given
# characteristics. It's especially useful for investigating how the presence and number of the article effects PMIs.

import pickle
import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent, give_dependents, semdom_poser, grammatical_number, poser
from collections import Counter
import math

all_sem_dom_pos_dict = pickle.load(open('all_sem_dom_pos_dict.pickle', 'rb'))
original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)


# This is designed to modify the semantic preference dictionary for prepositions with an article.
def prep_art_dependent(sentence_words, f_head_counter, f_head_dep_dep_cooccur, f_sem_pref_dict):
    for f_head_word in sentence_words:
        if f_head_word.has_attr('lemma'):
            if deaccent(f_head_word['lemma']).lower() == head_lemma and poser(f_head_word) == head_pos:
                f_head_counter += 1
                for f_dependent in give_dependents(sentence_words, f_head_word):
                    for f_article in give_dependents(sentence_words, f_dependent):
                        if f_article.has_attr('lemma'):
                            if deaccent(f_article['lemma']).lower() == dependent_dependent_lemma\
                                    and poser(f_article) == dependent_dependent_pos and \
                                    grammatical_number(f_article) == dependent_dependent_number:
                                f_head_dep_dep_cooccur += 1
                                print(head_lemma, f_article['form'], f_dependent['form'])
                                for f_sem_dom_pos in semdom_poser(f_dependent):
                                    f_sem_pref_dict[f_sem_dom_pos] += 1
    return f_head_counter, f_head_dep_dep_cooccur, f_sem_pref_dict


file_count = 0
head_counter = 0
qualified_head_occurrence = 0
corpus_tokens = 1107273
sem_pref_dict = Counter()
PMI_dict = {}

head_lemma = 'αντι'
head_pos = 'adposition'
dependent_dependent_lemma = 'ο'
dependent_dependent_number = 'plural'
dependent_dependent_pos = 'article'

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
                head_counter, qualified_head_occurrence, sem_pref_dict = prep_art_dependent(tokens, head_counter,
                                                                                            qualified_head_occurrence,
                                                                                            sem_pref_dict)
            if len(words) > 0:
                head_counter, qualified_head_occurrence, sem_pref_dict = prep_art_dependent(words, head_counter,
                                                                                            qualified_head_occurrence,
                                                                                            sem_pref_dict)
        print(head_counter, qualified_head_occurrence)
        xml_file.close()

corpus_tokens -= qualified_head_occurrence

for semantic_domain_pos in all_sem_dom_pos_dict:
    sem_dom_occurrence = all_sem_dom_pos_dict[semantic_domain_pos]
    if semantic_domain_pos in sem_pref_dict:
        mutual_occurrences = sem_pref_dict[semantic_domain_pos]
        PMI = math.log(mutual_occurrences / ((qualified_head_occurrence * sem_dom_occurrence) / corpus_tokens), 2)
        precision = '='
    else:
        PMI = math.log(1 / ((qualified_head_occurrence * sem_dom_occurrence) / corpus_tokens), 2)
        precision = '<'
        mutual_occurrences = 0
    PMI_dict[semantic_domain_pos] = [precision, PMI, mutual_occurrences, all_sem_dom_pos_dict[semantic_domain_pos]]
print(head_lemma, 'occurs', head_counter, 'times.')
print(head_lemma, dependent_dependent_lemma, dependent_dependent_number, qualified_head_occurrence, 'times.')
os.chdir(original_folder)
filename_string = head_lemma + '_' + dependent_dependent_lemma + '_' + dependent_dependent_number + '_sem_dom_PMIs.csv'
wiq_sem_dom_PMI = pd.DataFrame.from_dict(PMI_dict, orient='index', columns=['Precision', 'PMI', 'Co-occurrence',
                                                                            'Domain Occurrence'])
wiq_sem_dom_PMI.to_csv(filename_string)
