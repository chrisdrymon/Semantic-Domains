import pickle
import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent
from collections import Counter
import math
import time

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


# Given the sentence find_all list and a head word, this function returns the words which depend on that head.
def give_dependents(sentence_words, head_word):
    the_words = []
    if head_word.has_attr('id'):
        head_word_id = head_word['id']
        for f_word in sentence_words:
            if f_word.has_attr('head'):
                word_head = f_word['head']
                if word_head == head_word_id:
                    the_words.append(f_word)
            if f_word.has_attr('head-id'):
                word_head = f_word['head-id']
                if word_head == head_word_id:
                    the_words.append(f_word)
    return the_words


# Given a word, this will return its list of semantic domains (parts-of-speech).
def semdom_poser(f_word):
    semdom_pos_list = []
    pos = poser(f_word)
    if f_word.has_attr('lemma'):
        lemma = deaccent(f_word['lemma']).lower()
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


# This takes a token or word and returns its number: singular, plural, dual, or other.
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


# This returns the part-of-speech or the mood if the part-of-speech is a verb for a given word.
def poser(f_word):
    if f_word.has_attr('postag'):
        if len(f_word['postag']) > 0:
            pos0 = f_word['postag'][0]
            if pos0 in pos0_dict:
                pos = pos0_dict[pos0]
                if pos == 'verb':
                    if len(f_word['postag']) > 4:
                        pos4 = f_word['postag'][4]
                        if pos4 in pos4_dict:
                            pos = pos4_dict[pos4]
            else:
                pos = 'other'
        else:
            pos = 'other'
    elif f_word.has_attr('part-of-speech'):
        if len(f_word['part-of-speech']) > 0:
            pos0 = f_word['part-of-speech'][0]
            if pos0 in proiel_pos_dict:
                pos = proiel_pos_dict[pos0]
                if pos == 'verb':
                    if len(f_word['morphology']) > 3:
                        pos3 = f_word['morphology'][3]
                        if pos3 in pos4_dict:
                            pos = pos4_dict[pos3]
            else:
                pos = 'other'
        else:
            pos = 'other'
    else:
        pos = 'other'
    return pos


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
dependent_number = 'singular'
dependent_pos = 'article'
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
