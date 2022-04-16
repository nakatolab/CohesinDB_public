import pandas as pd
import csv

def rmdup(aa):
    str = ","
    filt = list(filter(None, aa.strip().split(",")))
    output = str.join(set(filt))
    return(output)

cell = pd.read_csv("allcohesin.allcell",sep="\t",header=None)
celluniq = cell[0].apply(rmdup)
celluniq.to_csv("allcohesin.allcell.unique",header=None,index=False)

cell = pd.read_csv("allcohesin.allid",sep="\t",header=None)
celluniq = cell[0].apply(rmdup)
celluniq.to_csv("allcohesin.allid.unique",header=None,index=False)

cell = pd.read_csv("allcohesin.allsubunit",sep="\t",header=None)
celluniq = cell[0].apply(rmdup)
celluniq.to_csv("allcohesin.allsubunit.unique",header=None,index=False)


