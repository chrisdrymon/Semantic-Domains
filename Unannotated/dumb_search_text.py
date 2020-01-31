import os
from utility import deaccent
from collections import Counter
import pandas
import re

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL',
                           'Plaintext')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 1
word_count = 0
word_list = Counter()

for file in indir:
    small_word_count = 0
    if file[-4:] == '.xml':
        print(file_count, file)
        perseus = open(file, 'r', encoding='utf-8')
        perseus_text = perseus.read()
        split_graph = re.split('[·;.]', perseus_text)
        for sentence in split_graph:
            split_sentence = sentence.split()
            i = 0
            for word in split_sentence:
                if deaccent(word) == 'αντι':
                    try:
                        next_word = split_sentence[i + 1]
                    except IndexError:
                        next_word = 'none'
                    print(word, next_word)
                    small_word_count += 1
                    word_count += 1
                    word_list[deaccent(next_word)] += 1
                i += 1
        file_count += 1
        print(small_word_count, 'αντιs in work.')
df = pandas.DataFrame.from_dict(word_list, orient='index').reset_index()
df.to_csv('Antis.csv', encoding='utf-8')
print(file_count - 1, 'files in', folder_path)
print(word_count, 'αντιs in corpus.')
print(word_list)
print(len(word_list), 'unique words follow αντι.')
