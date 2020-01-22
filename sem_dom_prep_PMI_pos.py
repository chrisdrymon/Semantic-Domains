import pickle
import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent
from collections import Counter
import math

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
preposition = 'περι'
for file in indir:
    if file[-4:] == '.xml':
        file_count += 1
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        sentences = soup.find_all('sentence')
        for sentence in sentences:
            words = sentence.find_all(['word', 'token'])
            for head in words:
                if head.has_attr('lemma'):
                    if deaccent(head['lemma']).lower() == preposition:
                        wiq_counter += 1
                        wiq_id = head['id']
                        for word in words:
                            if word.has_attr('head'):
                                if word['head'] == wiq_id:
                                    if word.has_attr('lemma'):
                                        word_lemma = deaccent(word['lemma']).lower()
                                    else:
                                        word_lemma = 'nolemma'
                                    if word.has_attr('postag'):
                                        word_pos = word['postag']
                                        if len(word_pos) > 0:
                                            if word_pos[0] in pos0_dict:
                                                pos = pos0_dict[word['postag'][0]]
                                            else:
                                                pos = 'other'
                                        else:
                                            pos = 'other'
                                        if pos == 'verb':
                                            if len(word_pos) > 4:
                                                if word_pos[4] in pos4_dict:
                                                    pos = pos4_dict[word_pos[4]]
                                    else:
                                        pos = 'other'
                                    if word_lemma in by_lemma_dict:
                                        for domain in by_lemma_dict[word_lemma]:
                                            domain_pos = domain + ' (' + pos + ')'
                                            wiq_sem_pref_dict[domain_pos] += 1
                                    else:
                                        wiq_sem_pref_dict['lemma_unknown' + ' (' + pos + ')'] += 1
                            if word.has_attr('head-id'):
                                if word['head-id'] == wiq_id:
                                    if word.has_attr('lemma'):
                                        word_lemma = deaccent(word['lemma']).lower()
                                    else:
                                        word_lemma = 'nolemma'
                                    if word.has_attr('part-of-speech'):
                                        word_pos = word['part-of-speech']
                                        if len(word_pos) > 0:
                                            if word_pos[0] in proiel_pos_dict:
                                                pos = proiel_pos_dict[word_pos[0]]
                                            else:
                                                pos = 'other'
                                        else:
                                            pos = 'other'
                                        if pos == 'verb':
                                            if word.has_attr('morphology'):
                                                if len(word['morphology']) > 3:
                                                    if word['morphology'][3] in pos4_dict:
                                                        pos = pos4_dict[word['morphology'][3]]
                                    else:
                                        pos = 'other'
                                    if word_lemma in by_lemma_dict:
                                        for domain in by_lemma_dict[word_lemma]:
                                            domain_pos = domain + ' (' + pos + ')'
                                            wiq_sem_pref_dict[domain_pos] += 1
                                    else:
                                        wiq_sem_pref_dict['lemma_unknown' + ' (' + pos + ')'] += 1
        print(wiq_counter, preposition, file)
        xml_file.close()
for semantic_domain in all_sem_dom_ct_dict:
    if semantic_domain in wiq_sem_pref_dict:
        mutual_occurrences = wiq_sem_pref_dict[semantic_domain]
        sem_dom_occurrence = all_sem_dom_ct_dict[semantic_domain]
        PMI = math.log(mutual_occurrences/((wiq_counter * sem_dom_occurrence)/1107273), 2)
    else:
        PMI = 'N/A'
        mutual_occurrences = 0
    PMI_dict[semantic_domain] = [PMI, mutual_occurrences, all_sem_dom_ct_dict[semantic_domain]]
os.chdir(original_folder)
filename_string = preposition+'_sem_dom_PMIs.csv'
wiq_sem_dom_PMI = pd.DataFrame.from_dict(PMI_dict, orient='index')
wiq_sem_dom_PMI.to_csv(filename_string)
