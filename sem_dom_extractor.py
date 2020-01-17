import pickle
import pandas as pd
from utility import deaccent

sem_doms = pd.read_csv('bsl_hierarchy_data.tsv', sep='\t', header=0)
i = 0
sem_dom_dictionary = {}
while i < 8144:
    lemma = deaccent(sem_doms.at[i, 'lemma'][13:]).lower()
    print(i, lemma)
    for domain in sem_doms.at[i, 'hierarchy'].split(','):
        if domain in sem_dom_dictionary:
            if lemma in sem_dom_dictionary[domain]:
                pass
            else:
                sem_dom_dictionary[domain].append(lemma)
        else:
            sem_dom_dictionary[domain] = [lemma]
    i += 1
with open('by_domain_dictionary.pickle', 'wb') as handle:
    pickle.dump(sem_dom_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
