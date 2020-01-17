import pickle
import pandas as pd
import numpy as np
from utility import deaccent

list1 = ['jon', 'john', 'michael']
list2 = ['jon', 'george']
print(np.unique(list1 + list2))
