import os
from bs4 import BeautifulSoup

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 1
files_changed = 0
total_punc_change = 0
for file in indir:
    if file[-4:] == '.xml':
        punctuation_encountered = 0
        i = 0
        print(file)
        greek_file = open(file, 'r', encoding='utf-8')
        greek_text = BeautifulSoup(greek_file, 'xml')
        word_list = greek_text.find_all('word')
        while i < len(word_list):
            try:
                if word_list[i]['lemma'] == 'punc1':
                    j = 0
                    k = 0
                    all_punctuation = ''
                    try:
                        while word_list[i+j]['lemma'] == 'punc1':
                            all_punctuation += word_list[i+j]['form']
                            j += 1
                    except IndexError:
                        while k < j:
                            all_punctuation += word_list[i+k]['form']
                            k += 1
                    word_list[i-1]['presentation-after'] = all_punctuation
                    punctuation_encountered += 1
            except KeyError:
                pass
            i += 1
        for word_thing in greek_text.find_all('word'):
            try:
                if word_thing['lemma'] == 'punc1':
                    word_thing.decompose()
            except KeyError:
                pass
        greek_file.close()
        with open(file, 'w') as writefile:
            writefile.write(str(greek_text.prettify()))
        if punctuation_encountered > 0:
            files_changed += 1
        total_punc_change += punctuation_encountered
        print(punctuation_encountered, 'punctuations encountered.')
print(total_punc_change, 'encountered over', files_changed, 'files.')
