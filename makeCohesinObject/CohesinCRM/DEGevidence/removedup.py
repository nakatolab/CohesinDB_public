import pandas as pd
import csv
import sys
import csv

inputname = sys.argv[1]
outname = sys.argv[2]

def rmdup(aa):
    str = ","
    filt = list(filter(None, aa.strip().split(",")))
    output = str.join(set(filt))
    return(output)

cell = pd.read_csv(inputname,sep="\t",header=None)
celluniq = cell[0].apply(rmdup)
celluniq.to_csv(outname,header=None,index=False)



