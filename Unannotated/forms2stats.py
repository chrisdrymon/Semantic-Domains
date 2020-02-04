import os
import re
import statistics
import math
from scipy.stats import t
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

word_form_1 = 'υιος'
word_form_2 = 'θεου'
word_1_freq = 0
word_2_freq = 0
total_word_count = 0

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
                    no_accent_word = deaccent(a_word).lower()
                    if no_accent_word == word_form_1:
                        word_1_freq += 1
                    if no_accent_word == word_form_2:
                        word_2_freq += 1
                    unaccented_sentence.append(no_accent_word)
                    total_word_count += 1
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

variance = statistics.variance(word_distances)
expected_cooccurrence = word_1_freq * word_2_freq / total_word_count
independent_mean = expected_cooccurrence / total_word_count
bernoulli_variance = independent_mean * (1 - independent_mean)
sample_mean = distance_count[1]/total_word_count
t_score = (sample_mean - independent_mean)/math.sqrt(sample_mean/total_word_count)

print('Total word count is', total_word_count)
print(word_1_freq, 'occurrences of', word_form_1)
print(word_2_freq, 'occurrences of', word_form_2)
print('Expected independent mean:', independent_mean)
print(expected_cooccurrence, 'expected bigram co-occurrences.')
print(distance_count[1], 'occurrences of', word_form_1, word_form_2)
print('Bernoulli Trial Variance:', bernoulli_variance)
print('Collocation t-score:', t_score)
print('Collocation p-score:', t.sf(t_score, total_word_count-1), '\n')
print(distance_count)
print(len(word_distances), 'co-occurrences within a sentence.')
print(statistics.mean(word_distances), 'is the average distance.')
print(variance, 'is the distance variance.')
print(math.sqrt(variance), 'is the distance standard deviation.')
x_axis = []
y_value = []
for key in distance_count.keys():
    x_axis.append(key)
    y_value.append(distance_count[key])
plt.bar(x_axis, y_value)
plt.show()
