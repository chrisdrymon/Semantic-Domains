import os
import re
import pickle
from bs4 import BeautifulSoup
from utility import deaccent
from collections import Counter

original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 1
word_freq = Counter()

for file in indir:
    if file[-4:] == '.xml':
        word_count = 0
        print(file_count, file)
        greek_file = open(file, 'r', encoding='utf-8')
        greek_text = BeautifulSoup(greek_file, 'xml')
        if greek_text.author:
            author = greek_text.author.text
        else:
            author = 'Unknown'
        if greek_text.title.text == 'Machine readable text':
            title = greek_text.find_all('title')[1].text
        else:
            title = greek_text.title.text
        print(author, title)
        for section in greek_text.find_all('text'):
            split_graph = re.split('[··;.,]', section.text)
            for sentence in split_graph:
                split_sentence = sentence.split()
                for a_word in split_sentence:
                    word_freq[deaccent(a_word).lower()] += 1
                    word_count += 1
        file_count += 1
        print(word_count)
os.chdir(original_folder)
with open('form_freq_dict.pickle', 'wb') as handle:
    pickle.dump(word_freq, handle, protocol=pickle.HIGHEST_PROTOCOL)
