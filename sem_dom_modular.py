import pickle
import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent
from collections import Counter
import math
import time

by_lemma_dict = pickle.load(open('by_lemma_dictionary.pickle', 'rb'))
all_sem_dom_ct_dict = pickle.load(open('all_sem_dom_pos_dict.pickle', 'rb'))
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

# I'm going to use "wiq" for word-in-question.
file_count = 0
wiq_counter = 0
wiq_sem_pref_dict = Counter()
PMI_dict = {}
eulogew_en_counter = 0
wiq = 'ευλογεω'

# Given the sentence words and head word, this function returns the words whose head is the head_word.
def header(sentence_words, head_word):
    the_words = []
    if head_word.has_attr('id'):
        head_word_id = head_word['id']
        for word in sentence_words:
            if word.has_attr('head'):
                word_head = word['head']
                if word_head == head_word_id:
                    the_words.append(word_head)
            if word.has_attr('head-id'):
                word_head = word['head-id']
                if word_head == head_word_id:
                    the_words.append(word_head)
    return the_words

# Given a word, this will return its list of semantic domains (parts-of-speech)
def agdt_semdom_pos_counter(word):
    semdom_pos_list = []
    if word.has_attr('postag'):
        if len(word['postag']) > 0:
            pos0 = word['postag'][0]
            if pos0 in pos0_dict:
                pos = pos0_dict[pos0]
                if pos == 'verb':
                    if len(word['postag']) > 4:
                        pos4 = word['postag'][4]
                        if pos4 in pos4_dict:
                            pos = pos4_dict[pos4]
            else:
                pos = 'other'
        else:
            pos = 'other'
    elif word.has_attr('part-of-speech'):
        if len(word['part-of-speech']) > 0:
            pos0 = word['part-of-speech'][0]
            if pos0 in proiel_pos_dict:
                pos = proiel_pos_dict[pos0]
                if pos == 'verb':
                    if len(word['morphology']) > 3:
                        pos3 = word['morphology'][3]
                        if pos3 in pos4_dict:
                            pos = pos4_dict[pos3]
            else:
                pos = 'other'
        else:
            pos = 'other'
    else:
        pos = 'other'
    if word.has_attr('lemma'):
        lemma = deaccent(word['lemma']).lower()
        if lemma in by_lemma_dict:
            sem_doms = by_lemma_dict[lemma]
        else:
            sem_doms = ['lemma_unknown']
    else:
        sem_doms = ['lemma_unknown']
    for domain in sem_doms:
        sem_dom_poss = domain + ' (' + pos + ')'
        semdom_pos_list.append(sem_dom_poss)
    return semdom_pos_list


def agdt(f_words):
    f_wiq_counter = 0
    f_eulogew_en_counter = 0
    for head in f_words:
        if head.has_attr('lemma'):
            if deaccent(head['lemma']).lower() == wiq:
                f_wiq_counter += 1
                if head.has_attr('id'):
                    wiq_id = head['id']
                    for en in f_words:
                        if en.has_attr('lemma'):
                            en_lemma = deaccent(en['lemma']).lower()
                            if en_lemma == 'εν':
                                if en.has_attr('head'):
                                    if en['head'] == wiq_id:
                                        f_eulogew_en_counter += 1
                                        if en.has_attr('id'):
                                            en_id = en['id']
                                            for oop in f_words:
                                                if oop.has_attr('head'):
                                                    if oop[head] == 'en_id':
                                                        if oop.has_attr('lemma'):
                                                            oop_lemma = oop['lemma']




#def proiel(f_tokens):


for file in indir:
    if file[-4:] == '.xml':
        print(file)
        file_count += 1
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        sentences = soup.find_all('sentence')
        for sentence in sentences:
            tokens = sentence.find_all(['token'])
            words = sentence.find_all(['word'])
            if len(tokens) > 0:
                proiel(tokens)
            if len(words) > 0:
                agdt(words)

                                    if en.has_attr('postag'):
                                        word_pos = en['postag']
#                                         if len(word_pos) > 0:
#                                             if word_pos[0] in pos0_dict:
#                                                 pos = pos0_dict[word['postag'][0]]
#                                             else:
#                                                 pos = 'other'
#                                         else:
#                                             pos = 'other'
#                                         if pos == 'verb':
#                                             if len(word_pos) > 4:
#                                                 if word_pos[4] in pos4_dict:
#                                                     pos = pos4_dict[word_pos[4]]
#                                     else:
#                                         pos = 'other'
#                                     if word_lemma in by_lemma_dict:
#                                         for domain in by_lemma_dict[word_lemma]:
#                                             domain_pos = domain + ' (' + pos + ')'
#                                             wiq_sem_pref_dict[domain_pos] += 1
#                                     else:
#                                         wiq_sem_pref_dict['lemma_unknown' + ' (' + pos + ')'] += 1
#                             if word.has_attr('head-id'):
#                                 if word['head-id'] == wiq_id:
#                                     if word.has_attr('lemma'):
#                                         word_lemma = deaccent(word['lemma']).lower()
#                                     else:
#                                         word_lemma = 'nolemma'
#                                     if word.has_attr('part-of-speech'):
#                                         word_pos = word['part-of-speech']
#                                         if len(word_pos) > 0:
#                                             if word_pos[0] in proiel_pos_dict:
#                                                 pos = proiel_pos_dict[word_pos[0]]
#                                             else:
#                                                 pos = 'other'
#                                         else:
#                                             pos = 'other'
#                                         if pos == 'verb':
#                                             if word.has_attr('morphology'):
#                                                 if len(word['morphology']) > 3:
#                                                     if word['morphology'][3] in pos4_dict:
#                                                         pos = pos4_dict[word['morphology'][3]]
#                                     else:
#                                         pos = 'other'
#                                     if word_lemma in by_lemma_dict:
#                                         for domain in by_lemma_dict[word_lemma]:
#                                             domain_pos = domain + ' (' + pos + ')'
#                                             wiq_sem_pref_dict[domain_pos] += 1
#                                     else:
#                                         wiq_sem_pref_dict['lemma_unknown' + ' (' + pos + ')'] += 1
#         print(wiq_counter, wiq, file)
#         xml_file.close()
# for semantic_domain in all_sem_dom_ct_dict:
#     if semantic_domain in wiq_sem_pref_dict:
#         mutual_occurrences = wiq_sem_pref_dict[semantic_domain]
#         sem_dom_occurrence = all_sem_dom_ct_dict[semantic_domain]
#         PMI = math.log(mutual_occurrences/((wiq_counter * sem_dom_occurrence)/1107273), 2)
#     else:
#         PMI = 'N/A'
#         mutual_occurrences = 0
#     PMI_dict[semantic_domain] = [PMI, mutual_occurrences, all_sem_dom_ct_dict[semantic_domain]]
# os.chdir(original_folder)
# filename_string = wiq + '_sem_dom_PMIs.csv'
# wiq_sem_dom_PMI = pd.DataFrame.from_dict(PMI_dict, orient='index', columns=['PMI', 'Co-occurrence',
#                                                                             'Domain Occurrence'])
# wiq_sem_dom_PMI.to_csv(filename_string)
