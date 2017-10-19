
import sys
import csv
import numpy as np
import re

root = sys.path[1]
newline_count = 0
with open(root + '/Data/Text_8760_100_21.txt') as fp:
    text = fp.readlines()
    for i in text:
        l = re.findall(r'(\r)?\n', i)
        newline_count += len(l)
    print(len(text))
    print('newlinecount: %d' % newline_count)

with open(root + '/Data/Sequence_8760_100_21.csv') as fp:
    reader = csv.reader(fp)
    total = 0
    for i in reader:
        total += np.sum(np.array(i).astype(int))

    print(total)

