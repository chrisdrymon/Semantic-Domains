import os
from tabulate import tabulate
from bs4 import BeautifulSoup
from collections import Counter

thing = Counter()
thing['four'] = 4
thing['nine'] = 9
thing['seven'] = 7

top = thing.most_common(2)

tot_row = [('name', 'number')]
newtot = tot_row + top
print(tabulate(newtot, headers='firstrow', tablefmt='pipe'))
