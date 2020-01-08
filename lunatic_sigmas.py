import os

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL',
                           'Plaintext')
os.chdir(folder_path)
indir = os.listdir(folder_path)
end_characters = [' ', '.', ';', '·', '\n', ',']
new_doc = ''
total_lunes = 0
file_count = 1
file_changes = 0

for file in indir:
    print(file, file_count)
    unread_doc = open(file, 'r', encoding='utf-8')
    doc = unread_doc.read()
    new_doc = ''
    i = 0
    lunates = 0
    for character in doc:
        if character == 'ϲ' or character == 'c':
            if doc[i+1] in end_characters:
                new_doc += 'ς'
            else:
                new_doc += 'σ'
            lunates += 1
        else:
            new_doc += character
        i += 1
    with open(file, 'w') as writefile:
        writefile.write(new_doc)
    file_count += 1
    total_lunes += lunates
    if lunates > 0:
        file_changes += 1
    print(lunates, 'lunate sigmas converted.')
print(total_lunes, 'total lunate sigmas converted.')
