import pandas as pd
import os
import time
ref = pd.read_csv("allgene.idconverter",header=None,sep="\t")[1]
reflen = len(ref)

interactionDF = pd.DataFrame()
subunitDF = pd.DataFrame()
studyDF = pd.DataFrame()

for file in os.listdir("eachfile_uniqgene"):
    print(time.asctime())
    print(file)
    count = len(open(r"eachfile_uniqgene/"+file,'rU').readlines())
    print(count)
    if count > 0:
        interaction = file.split("_")[0]
        subunit = file.split(".")[0].split("_")[3]
        study = file.split("_")[1]

        fileDF = pd.read_csv("eachfile_uniqgene/"+file,header=None,sep="\t")[0]

        interactionlist = ["."] * reflen
        subunitlist = ["."] * reflen
        studylist = ["."] * reflen

        for i in fileDF:
            selectindex = ref[ ref == i ].index[0]
            interactionlist[selectindex] = interaction
            subunitlist[selectindex] = subunit
            studylist[selectindex] = study

        interactionDF = pd.concat([interactionDF,pd.Series(interactionlist)],axis=1)
        subunitDF = pd.concat([subunitDF,pd.Series(subunitlist)],axis=1)
        studyDF = pd.concat([studyDF,pd.Series(studylist)],axis=1)
    else:
        pass

interactionDF.to_csv("interactionDF.tsv",sep="\t",header=None,index=None)
subunitDF.to_csv("subunitDF.tsv",sep="\t",header=None,index=None)
studyDF.to_csv("studyDF.tsv",sep="\t",header=None,index=None)


