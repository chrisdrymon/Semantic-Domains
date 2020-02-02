import os
import re
import statistics
from bs4 import BeautifulSoup
from utility import deaccent
from collections import Counter
from matplotlib import pyplot as plt

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 1
word_distances = []
distance_count = Counter()

word_form_1 = 'χριστος'
word_form_2 = 'ιησους'

for file in indir:
    if file[-4:] == '.xml':
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
                unaccented_sentence = []
                split_sentence = sentence.split()
                for a_word in split_sentence:
                    unaccented_sentence.append(deaccent(a_word).lower())
                if word_form_1 in unaccented_sentence and word_form_2 in unaccented_sentence:
                    word_place_1_list = [i for i, e in enumerate(unaccented_sentence) if e == word_form_1]
                    word_place_2_list = [i for i, e in enumerate(unaccented_sentence) if e == word_form_2]
                    for num_2 in word_place_2_list:
                        for num_1 in word_place_1_list:
                            word_distances.append(num_2 - num_1)
                            print(num_2 - num_1)
        file_count += 1
for number in word_distances:
    distance_count[number] += 1
print(distance_count)
print(len(word_distances), 'instances:')
print(statistics.mean(word_distances), 'is the average distance.')
print(statistics.variance(word_distances), 'is the variance.')
x_axis = []
y_value = []
for key in distance_count.keys():
    x_axis.append(key)
    y_value.append(distance_count[key])
plt.bar(x_axis, y_value)
plt.show()
