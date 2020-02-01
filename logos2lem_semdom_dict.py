# Given the Logos Semantic Domains TSV, this return a dictionary {lemma: [every semantic domain it is a member of]}

import pickle
import pandas as pd
from utility import deaccent

sem_doms = pd.read_csv('bsl_hierarchy_data.tsv', sep='\t', header=0)
i = 0
sem_dom_dictionary = {}
while i < 8144:
    lemma = deaccent(sem_doms.at[i, 'lemma'][13:]).lower()
    print(i, lemma)
    if lemma in sem_dom_dictionary:
        for domain in sem_doms.at[i, 'hierarchy'].split(','):
            if domain in sem_dom_dictionary[lemma]:
                pass
            else:
                sem_dom_dictionary[lemma].append(domain)
    else:
        sem_dom_dictionary[lemma] = sem_doms.at[i, 'hierarchy'].split(',')
    i += 1
with open('by_lemma_dictionary.pickle', 'wb') as handle:
    pickle.dump(sem_dom_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
df = pd.DataFrame.from_dict(sem_dom_dictionary, orient='index')
df.to_csv('by_lemma.csv')
print(sem_dom_dictionary)
