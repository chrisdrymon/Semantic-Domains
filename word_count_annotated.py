import os
from bs4 import BeautifulSoup

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 0
total_words = 0
total_tokens = 0
total_ws = 0
problem_files = []
for file in indir:
    if file[-4:] == '.xml':
        file_count += 1
        print(file_count, file)
        xml_file = open(file, 'r')
        open_text = BeautifulSoup(xml_file, 'lxml')

        words = open_text.find_all('word')
        tokens = open_text.find_all('token')
        ws = open_text.find_all('w')

        word_count = len(words)
        token_count = len(tokens)
        ws_count = len(ws)

        total_words += word_count
        total_tokens += token_count
        total_ws += ws_count

        total = total_words + total_tokens + total_ws
        totals = [total_words, total_tokens, total_ws]
        for item in totals:
            if item not in [0, total]:
                problem_files.append(file)

        print(word_count, 'words,', token_count, 'tokens,', ws_count, 'ws.')

print(total_words, 'words,', total_tokens, 'tokens,', total_ws, 'ws across', file_count, 'files.')
print(total_words+total_tokens+total_ws, 'total words.')
print(len(problem_files), 'problem files.')
