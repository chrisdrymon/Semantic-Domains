# Given a corpus, this returns the frequency of each part of speech

import pickle
import os
from bs4 import BeautifulSoup
from collections import Counter
from utility import poser

original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)

file_count = 0
pos_dict = Counter()

for file in indir:
    if file[-4:] == '.xml':
        file_count += 1
        print(file_count, file)
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        tokens = soup.find_all(['word', 'token'])
        for token in tokens:
            pos_dict[poser(token)] += 1
os.chdir(original_folder)
with open('all_pos_count.pickle', 'wb') as handle:
    pickle.dump(pos_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
