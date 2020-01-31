import os
from tabulate import tabulate
from bs4 import BeautifulSoup
from collections import Counter
from utility import deaccent, header, poser

original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)

file_count = 0
freq_dict = Counter()
head_pos = 'noun'
dependent_pos = 'noun'

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
                if poser(token) == dependent_pos:
                    head = header(tokens, token)
                    if type(head) is not str:
                        if poser(head) == head_pos:
                            if token.has_attr('lemma') and head.has_attr('lemma'):
                                dict_string = deaccent(token['lemma']).lower() + ' ' + deaccent(head['lemma']).lower()
                                freq_dict[dict_string] += 1
        print(freq_dict.most_common(5))
top_freq = freq_dict.most_common(20)
tableform = [('Collocation', 'Freq')] + top_freq
print(tabulate(tableform, headers='firstrow', tablefmt='pipe'))
