import pandas as pd
import csv
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

def rmdup(aa):
    str = ","
    filt = list(filter(None, aa.strip().split(",")))
    output = str.join(set(filt))
    return(output)

cell = pd.read_csv(infile,sep="\t",header=None)
celluniq = cell[0].apply(rmdup)
celluniq.to_csv(outfile,header=None,index=False)



