import pandas as pd
import csv
import sys
import os
import random
def shuff(test_list):
    return random.sample(test_list, len(test_list))

def tts(tup):
    st ="".join(tup)
    return st

from itertools import permutations
perm = permutations([ "R","V","z","7","9",'u',"Q","y","S","g","6","3"],8)
code=[]
for i in list(perm):
    code.append(tts(i))

c=[]
p=0
x=0
while x<=10000:
    x+=1
    p+=9989
    c.append(code[p])
df=pd.DataFrame(shuff(c),columns=["Delegate ID"])
df.to_csv('data9.csv',index=False)