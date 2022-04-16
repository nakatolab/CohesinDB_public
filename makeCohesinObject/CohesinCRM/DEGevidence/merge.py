import pandas as pd
import os
ref = pd.read_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/DEGs/allgene.idconverter",
                 header=None,sep="\t")

whetherDF = pd.DataFrame()
subunitDF = pd.DataFrame()
studyDF = pd.DataFrame()

for file in os.listdir("eachfile"):
    print(file)
    count = len(open(r"eachfile/"+file,'rU').readlines())
    print(count)
    if count > 0:
        subunit = file.split(".")[0].split("_")[4]
        study = file.split("_")[1]

        fileDF = pd.read_csv("eachfile/"+file,header=None,sep="\t")

        whetherlist = []
        subunitlist = []
        studylist = []
        for i in ref[1]:
            if i in list(fileDF[1]):
                whetherlist.append(1)
                subunitlist.append(subunit)
                studylist.append(study)
            else:
                whetherlist.append(0)
                subunitlist.append(".")
                studylist.append(".")

        whetherDF = pd.concat([whetherDF,pd.Series(whetherlist)],axis=1)
        subunitDF = pd.concat([subunitDF,pd.Series(subunitlist)],axis=1)
        studyDF = pd.concat([studyDF,pd.Series(studylist)],axis=1)
    else:
        pass

whetherDF.to_csv("whetherDF.tsv",sep="\t",header=None,index=None)
subunitDF.to_csv("subunitDF.tsv",sep="\t",header=None,index=None)
studyDF.to_csv("studyDF.tsv",sep="\t",header=None,index=None)

df = pd.read_csv("whetherDF.tsv",sep="\t",header=None)
dfsum = df.sum(axis=1)
dfsum.to_csv("whetherDFsum.tsv",sep="\t",header=None,index=None)

