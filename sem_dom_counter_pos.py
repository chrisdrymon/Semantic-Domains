import pickle
import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent
from collections import Counter

by_lemma_dict = pickle.load(open('by_lemma_dictionary.pickle', 'rb'))
original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 0
word_count_total = 0
all_semdom_dict = Counter()
pos0_dict = {'a': 'adj', 'n': 'noun', 'v': 'verb', 'd': 'adv', 'c': 'conj', 'g': 'conj', 'r': 'adposition', 'b': 'conj',
             'p': 'pronoun', 'l': 'article', 'i': 'interjection', 'x': 'other', 'm': 'numeral', 'e': 'exclamation'}
pos2_dict = {'s': 'singular', 'p': 'plural', 'd': 'dual'}
pos4_dict = {'i': 'indicative', 's': 'subjunctive', 'n': 'infinitive', 'm': 'imperative', 'p': 'participle',
             'o': 'optative'}
for file in indir:
    if file[-4:] == '.xml':
        word_count = 0
        file_count += 1
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        words = soup.find_all(['word', 'token'])
        for word in words:
            if word.has_attr('lemma'):
                lemma = deaccent(word['lemma']).lower()
            else:
                lemma = 'nolemma'
            if word.has_attr('postag'):
                if len(word['postag']) > 0:
                    if word['postag'][0] in pos0_dict:
                        pos = pos0_dict[word['postag'][0]]
                    else:
                        pos = 'other'
                else:
                    pos = 'other'
            else:
                pos = 'other'
            if pos == 'verb':
                if len(word['postag']) > 4:
                    if word['postag'][4] in pos4_dict:
                        pos = pos4_dict[word['postag'][4]]
            if lemma in by_lemma_dict:
                for domain in by_lemma_dict[lemma]:
                    domain_pos = domain + ' (' + pos + ')'
                    all_semdom_dict[domain_pos] += 1
            else:
                all_semdom_dict['lemma_unknown' + ' (' + pos + ')'] += 1
            word_count += 1
        print(word_count, 'words in', file)
        word_count_total += word_count
        xml_file.close()
os.chdir(original_folder)
df = pd.DataFrame.from_dict(all_semdom_dict, orient='index')
df.to_csv('all_sem_dom_count_pos.csv')
with open('all_sem_dom_pos_dict.pickle', 'wb') as handle:
    pickle.dump(all_semdom_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Total word count:', word_count_total)
