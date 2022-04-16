import pandas as pd
import csv

def rmdup(aa):
    str = ","
    filt = list(filter(None, aa.strip().split(",")))
    output = str.join(set(filt))
    return(output)

cell = pd.read_csv("allcohesin.CRMs.temp",sep="\t",header=None)
celluniq = cell[0].apply(rmdup)
celluniq.to_csv("allcohesin.CRMs.unique",header=None,index=False)



