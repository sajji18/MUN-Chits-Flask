import pandas as pd
from list1 import *

hostcc=[]
'''["LMUN-IOSCO","IOSCO"],["LMUN-ECEJR","ECEJR"],["LMUN-UNGA","UNGA"],["LMUN-UNSC","UNSC"],["LMUN-UNCSW","UNCSW"],["LMUN-UEFA","UEFA"],["LMUN-IWC","IWC"],["LMUN-LOK_SABHA","LOK-SABHA"]'''

def addo(host_co,file_name,cmm):
    try:
        df=pd.read_csv(file_name)
        a=df.values.tolist()
        chits_po=True
        print("\n\n========"+host_co+"==========\n\n")
    except:
        print("\n\n+++++++++++"+host_co+"+++++++++++++++\n\n")
        chits_po=False
    if chits_po==True:
        for i in a:
            try:
                add_user(host_co,str(i[-1]),str(i[-2]))
                print(i)
            except:
                print("---------------")
                print(i[-4],i[-3],i[-2],i[-1])
                print("---------------")
    else:
        pass



'''
for h in hostcc:
    addo(h[0],str(h[0])+".csv",h[1])'''



