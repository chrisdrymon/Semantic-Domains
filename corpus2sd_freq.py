# Given a corpus, this returns frequency of every semantic domain

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
            if lemma in by_lemma_dict:
                for domain in by_lemma_dict[lemma]:
                    all_semdom_dict[domain] += 1
            else:
                all_semdom_dict['unknown'] += 1
            word_count += 1
        print(word_count, 'words in', file)
        word_count_total += word_count
        xml_file.close()
os.chdir(original_folder)
# df = pd.DataFrame.from_dict(all_semdom_dict, orient='index')
# df.to_csv('all_sem_dom_count.csv')
# with open('all_sem_dom_ct_dict.pickle', 'wb') as handle:
#    pickle.dump(all_semdom_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Total word count:', word_count_total)
