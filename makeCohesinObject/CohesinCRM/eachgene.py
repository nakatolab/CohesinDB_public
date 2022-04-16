import pandas as pd
ref = pd.read_csv("allgene.idconverter",sep="\t",header=None)
pair = pd.read_csv("triple-evidenced.pair.tsv",sep="\t",header=None)

#如果想快点
#pair.groupby(by="gene").cohesin.agg([('count', 'count'), ('cohesin', ', '.join)])
cohesinlist= []
count = 1
for i in ref[1]:
    if count % 1000 == 0:
        print(count)
    count += 1
    
    genebool = pair[0] == i
    if sum(genebool)>0:
        eachtarget = list(pair[genebool][1])
        eachtarget_str = ','.join(eachtarget)
        cohesinlist.append(eachtarget_str)
    else:
        cohesinlist.append(".")

geneDF = ref[[1,0,2,4,5,3,7]]
whetherTarget = pd.Series(cohesinlist) != "."
outDF = pd.concat([geneDF,whetherTarget,pd.Series(cohesinlist)],axis=1)
outDF.to_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/GeneTripleCohesin.tsv",sep="\t",header=None,index=None)



