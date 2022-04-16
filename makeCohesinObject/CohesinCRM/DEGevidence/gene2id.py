import pandas as pd
import sys
ref = pd.read_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/DEGs/allgene.idconverter",
                 header=None,sep="\t")

inputname = sys.argv[1]
outname = sys.argv[2]

file = pd.read_csv(inputname,header=None,sep="\t")

genelist = []
for i in file[0]:
    a = i.split("///")
    genelist += a


genebool = []
for i in ref[0]:
    genebool.append(i in list(set(genelist)))

out = ref[genebool]

out.to_csv(outname,sep="\t",index=None,header=None)



