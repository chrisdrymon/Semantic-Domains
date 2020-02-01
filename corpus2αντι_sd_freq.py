# This returns the semantic domain frequencies of dependents of αντι.

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
anti_counter = 0
anti_object_dict = Counter()
anti_object_semdom_dict = Counter()
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
                    if deaccent(head['lemma']).lower() == 'αντι':
                        anti_counter += 1
                        anti_id = head['id']
                        for word in words:
                            if word.has_attr('head'):
                                if word['head'] == anti_id:
                                    if word.has_attr('lemma'):
                                        word_lemma = deaccent(word['lemma']).lower()
                                    else:
                                        word_lemma = 'nolemma'
                                    anti_object_dict[word_lemma] += 1
                                    if word_lemma in by_lemma_dict:
                                        for domain in by_lemma_dict[word_lemma]:
                                            anti_object_semdom_dict[domain] += 1
                                    else:
                                        anti_object_semdom_dict['unknown'] += 1
                            if word.has_attr('head-id'):
                                if word['head-id'] == anti_id:
                                    if word.has_attr('lemma'):
                                        word_lemma = deaccent(word['lemma']).lower()
                                    else:
                                        word_lemma = 'nolemma'
                                    anti_object_dict[word_lemma] += 1
                                    if word_lemma in by_lemma_dict:
                                        for domain in by_lemma_dict[word_lemma]:
                                            anti_object_semdom_dict[domain] += 1
                                    else:
                                        anti_object_semdom_dict['unknown'] += 1
        print(anti_counter, 'αντι', file)
        xml_file.close()
os.chdir(original_folder)
df = pd.DataFrame.from_dict(anti_object_dict, orient='index')
df.to_csv('anti_objects.csv')
anti_sem_dom = pd.DataFrame.from_dict(anti_object_semdom_dict, orient='index')
anti_sem_dom.to_csv('anti_sem_pref.csv')
