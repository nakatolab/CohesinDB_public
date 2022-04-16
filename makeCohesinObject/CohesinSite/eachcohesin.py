import pandas as pd
ref = pd.read_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/allgene.idconverter",
                  sep="\t",header=None)
pair = pd.read_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/triple-evidenced.pair.tsv",
                   sep="\t",header=None)
cohesin =  pd.read_csv("/work3/WANG_cohesinDB/Curated/annotation_real/allcohesin.pos",
                        sep="\t",header=None)

pair.columns = ["gene",'cohesin']
cohesin_agg = pair.groupby(by="cohesin").gene.agg([('count', 'count'), ('gene', ','.join)])

count=1
genelist = []
for i in cohesin[3]:
    if count % 100000 == 0:
        print(count)
    count += 1

    try:
        genelist.append(cohesin_agg.loc[i,'gene'])
    except:
         genelist.append(".")

outGeneID = pd.Series(genelist)
outGeneID.to_csv("/work3/WANG_cohesinDB/Curated/annotation_real/allcohesin.targetGeneID",
                 sep="\t",header=None,index=None)


ref.index = ref[1]
namelist=[]
count=1

for i in pair['gene']:
    if count % 100000 == 0:
        print(count)
    count += 1
    
    namelist.append(ref.loc[i,0])

newDF = pd.concat([pair,pd.Series(namelist,name="geneName")],axis=1)
cohesin_aggName = newDF.groupby(by="cohesin").geneName.agg([('count', 'count'), ('geneName', ','.join)])

count=1
namelist = []
for i in cohesin[3]:
    if count % 100000 == 0:
        print(count)
    count += 1

    try:
        namelist.append(cohesin_aggName.loc[i,'geneName'])
    except:
        namelist.append(".")

outGeneName = pd.Series(namelist)
outGeneName.to_csv("/work3/WANG_cohesinDB/Curated/annotation_real/allcohesin.targetGeneName",
                 sep="\t",header=None,index=None)
