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
dependent1_pos = 'adj'
dependent2_pos = 'adj'

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
                    adj_list = []
                    for possible_adj in give_dependents(tokens, token):
                        if poser(possible_adj) == 'adj':
                            if possible_adj.has_attr('lemma'):
                                adj_list.append(deaccent(possible_adj['lemma']).lower())
                    if len(adj_list) > 1:
                        adj_list.reverse()
                        collocation_string = deaccent(token['lemma']).lower()
                        for adjective in adj_list:
                            collocation_string = adjective + ' ' + collocation_string
                        freq_dict[collocation_string] += 1
        print(freq_dict.most_common(5))
top_freq = freq_dict.most_common(20)
tableform = [('Collocation', 'Freq')] + top_freq
print(tabulate(tableform, headers='firstrow', tablefmt='pipe'))
