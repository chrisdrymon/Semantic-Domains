import pickle
import os
from bs4 import BeautifulSoup
from collections import Counter

original_folder = os.getcwd()
folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)

pos0_dict = {'a': 'adj', 'n': 'noun', 'v': 'verb', 'd': 'adv', 'c': 'conj', 'g': 'conj', 'r': 'adposition', 'b': 'conj',
             'p': 'pronoun', 'l': 'article', 'i': 'interjection', 'x': 'other', 'm': 'numeral', 'e': 'interjection'}
pos2_dict = {'s': 'singular', 'p': 'plural', 'd': 'dual'}
pos4_dict = {'i': 'indicative', 's': 'subjunctive', 'n': 'infinitive', 'm': 'imperative', 'p': 'participle',
             'o': 'optative'}
agdt2_rel_dict = {'obj': 'object'}
proiel_pos_dict = {'A': 'adj', 'D': 'adv', 'S': 'article', 'M': 'numeral', 'N': 'noun', 'C': 'conj', 'G': 'conj',
                   'P': 'pronoun', 'I': 'interjection', 'R': 'adposition', 'V': 'verb'}


# This returns the part-of-speech or the mood if the part-of-speech is a verb for a given word.
def poser(f_word):
    if f_word.has_attr('postag'):
        if len(f_word['postag']) > 0:
            pos0 = f_word['postag'][0]
            if pos0 in pos0_dict:
                f_pos = pos0_dict[pos0]
                if f_pos == 'verb':
                    if len(f_word['postag']) > 4:
                        pos4 = f_word['postag'][4]
                        if pos4 in pos4_dict:
                            f_pos = pos4_dict[pos4]
            else:
                f_pos = 'other'
        else:
            f_pos = 'other'
    elif f_word.has_attr('part-of-speech'):
        if len(f_word['part-of-speech']) > 0:
            pos0 = f_word['part-of-speech'][0]
            if pos0 in proiel_pos_dict:
                f_pos = proiel_pos_dict[pos0]
                if f_pos == 'verb':
                    if len(f_word['morphology']) > 3:
                        pos3 = f_word['morphology'][3]
                        if pos3 in pos4_dict:
                            f_pos = pos4_dict[pos3]
            else:
                f_pos = 'other'
        else:
            f_pos = 'other'
    else:
        f_pos = 'other'
    return f_pos


file_count = 0
pos_dict = Counter()

for file in indir:
    if file[-4:] == '.xml':
        file_count += 1
        print(file_count, file)
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        words = soup.find_all(['word', 'token'])
        for word in words:
            if word.has_attr('empty-token-sort') or word.has_attr('artificial'):
                pass
            else:
                pos = poser(word)
                if pos in pos_dict:
                    pos_dict[pos] += 1
                else:
                    pos_dict[pos] = 1
        print(pos_dict)

os.chdir(original_folder)
with open('all_pos_count.pickle', 'wb') as handle:
    pickle.dump(pos_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
