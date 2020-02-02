import os
from matplotlib import pyplot as plt
from tabulate import tabulate
from bs4 import BeautifulSoup
from collections import Counter

freq = {-1: 265, -2: 117, 1: 37, -3: 12, 2: 3, -4: 3, 3: 2, -5: 1, -12: 1}
x_axis = []
y_value = []
for key in freq.keys():
    x_axis.append(key)
    y_value.append(freq[key])
plt.bar(x_axis, y_value)
plt.show()
