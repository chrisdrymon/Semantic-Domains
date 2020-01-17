import os
from bs4 import BeautifulSoup

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 0
total_count_words = 0
total_count_tokens = 0
total_blank_words = 0
total_blank_tokens = 0
problem_files = []
for file in indir:
    if file[-4:] == '.xml':
        file_count += 1
        print(file_count, file)
        xml_file = open(file, 'r')
        open_text = BeautifulSoup(xml_file, 'xml')
        blank_words = 0
        blank_tokens = 0
        word_count = 0
        token_count = 0
        words = open_text.find_all('word')
        tokens = open_text.find_all('token')
        for word in words:
            if word.has_attr('artificial'):
                blank_words += 1
            else:
                word_count += 1
        for token in tokens:
            if token.has_attr('empty-token-sort'):
                blank_tokens += 1
            else:
                token_count += 1
        if word_count > 0:
            total_count_words += word_count
            total_blank_words += blank_words
            print(word_count, 'words,', blank_words, 'blank words.')
        if token_count > 0:
            total_count_tokens += token_count
            total_blank_tokens += blank_tokens
            print(token_count, 'tokens,', blank_tokens, 'blank tokens.')
print(total_count_words, 'words,', total_count_tokens, 'tokens.')
print(total_blank_words, 'blank words,', total_blank_tokens, 'blank tokens.')
print(total_count_words + total_count_tokens, 'total words in', file_count, 'files.')
