import os
from bs4 import BeautifulSoup
from utility import deaccent

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 1
note_files_changed = 0
index_files_changed = 0
bibl_files_changed = 0
graph_files_changed = 0
interp_files_changed = 0
latin_graph_files_changed = 0
foreign_file_changes = 0
notes_total = 0
indices_total = 0
bibl_total = 0
graph_total = 0
interp_total = 0
latin_graph_total = 0
foreign_total = 0

greek_chars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
               'φ', 'χ', 'ψ', 'ω']

for file in indir:
    note_count = 0
    index_count = 0
    graph_count = 0
    bibl_count = 0
    interp_count = 0
    latin_graph_count = 0
    foreign_graph_count = 0
    if file[-4:] == '.xml':
        print(file_count, file)
        greek_file = open(file, 'r', encoding='utf-8')
        greek_text = BeautifulSoup(greek_file, 'lxml')
        if greek_text.author:
            author = greek_text.author.text
        else:
            author = 'Unknown'
        if greek_text.title.text == 'Machine readable text':
            title = greek_text.find_all('title')[1].text
        else:
            title = greek_text.title.text
        for notes in greek_text.find_all('note'):
            notes.decompose()
            note_count += 1
        for index_tag in greek_text.find_all('div', {'subtype': 'index'}):
            index_tag.decompose()
            index_count += 1
        for bibl_tag in greek_text.find_all('bibl'):
            bibl_tag.decompose()
            bibl_count += 1
        for interp_tag in greek_text.find_all('interpgrp'):
            interp_tag.decompose()
            interp_count += 1
        for paragraph in greek_text.find_all('p'):
            sim_graph = deaccent(paragraph.text)
            if any(letter in greek_chars for letter in sim_graph):
                pass
            else:
                paragraph.decompose()
                graph_count += 1
        just_text = greek_text.find_all('text')
        for item in just_text:
            for latin_paragraph in item.find_all(attrs={'lang': 'la'}):
                latin_paragraph.decompose()
                latin_graph_count += 1
            for latin_paragraph in item.find_all(attrs={'lang': 'lat'}):
                latin_paragraph.decompose()
                latin_graph_count += 1
            for foreign_graph in item.find_all(attrs={'xml:lang': 'la'}):
                foreign_graph.decompose()
                foreign_graph_count += 1
            for foreign_graph in item.find_all(attrs={'xml:lang': 'lat'}):
                foreign_graph.decompose()
                foreign_graph_count += 1
        file_count += 1
        print(note_count, 'notes extracted.')
        print(index_count, 'indexes extracted.')
        print(bibl_count, 'bibl tags extracted.')
        print(interp_count, 'interpreter groups extracted.')
        print(graph_count, 'paragraphs extracted.')
        greek_file.close()
        with open(file, 'w') as writefile:
            writefile.write(str(greek_text))
    if note_count > 0:
        note_files_changed += 1
    if index_count > 0:
        index_files_changed += 1
    if graph_count > 0:
        graph_files_changed += 1
    if bibl_count > 0:
        bibl_files_changed += 1
    if interp_count > 0:
        interp_files_changed += 1
    if latin_graph_count > 0:
        latin_graph_files_changed += 1
    if foreign_graph_count > 0:
        foreign_file_changes += 1
    notes_total += note_count
    indices_total += index_count
    graph_total += graph_count
    bibl_total += bibl_count
    interp_total += interp_count
    latin_graph_total += latin_graph_count
    foreign_total += foreign_graph_count
print(notes_total, 'notes across', note_files_changed, 'files.')
print(indices_total, 'indices across', index_files_changed, 'files.')
print(graph_total, 'graphs across', graph_files_changed, 'files.')
print(bibl_total, 'bibl tags across', bibl_files_changed, 'files.')
print(interp_total, 'interp groups across', interp_files_changed, 'files.')
print(latin_graph_total, 'latin paragraphs across', latin_graph_files_changed, 'files.')
print(foreign_total, 'foreign paragraphs across', foreign_file_changes, 'files.')
