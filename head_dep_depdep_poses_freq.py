import os
from tabulate import tabulate
from bs4 import BeautifulSoup
from collections import Counter
from utility import deaccent, header, poser, give_dependents

original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)

file_count = 0
freq_dict = Counter()
head_pos = 'noun'
dependent_pos = 'adposition'
depdep_pos = 'noun'

for file in indir:
    if file[-4:] == '.xml':
        file_count += 1
        print(file_count, file)
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        sentences = soup.find_all('sentence')
        for sentence in sentences:
            tokens = sentence.find_all(['word', 'token'])
            for token in tokens:
                if poser(token) == head_pos:
                    for possible_prep in give_dependents(tokens, token):
                        if poser(possible_prep) == dependent_pos:
                            for possible_noun in give_dependents(tokens, possible_prep):
                                if poser(possible_noun) == depdep_pos:
                                    if token.has_attr('lemma') and possible_prep.has_attr('lemma') and \
                                            possible_noun.has_attr('lemma'):
                                        collocation_string = deaccent(token['lemma'] + ' ' + possible_prep['lemma'] +
                                                                      ' ' + possible_noun['lemma']).lower()
                                        freq_dict[collocation_string] += 1
        print(freq_dict.most_common(5))
top_freq = freq_dict.most_common(20)
tableform = [('Collocation', 'Freq')] + top_freq
print(tabulate(tableform, headers='firstrow', tablefmt='pipe'))
