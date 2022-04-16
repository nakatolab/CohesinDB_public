import pandas as pd

corrpair=pd.read_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/correlation/gene2cohesin.pair",
                   header=None,sep="\t")

degpair=pd.read_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/DEGs/gene2cohesin.pair",
                   header=None,sep="\t")

looppair=pd.read_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/loop/gene2cohesin.pair",
                    header=None,sep="\t")

print("set1 is co-expression")
set1 = set(corrpair[0] +"+"+ corrpair[1])

print("set2 is DEGs")
set2 = set(degpair[0]+"+"+ degpair[1])

print("set3 is loop")
set3 = set(looppair[0]+"+"+ looppair[1])

print("set1 & set2 & set3")
triple =  set2 & set3
print(len(triple))
pd.Series(list(triple)).to_csv("/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/triple-evidenced.pair",
                               header=None,sep="\t",index=None)

print("set1 & set2")
print(len(set1 & set2))
print("set1 & set3")
print(len(set1 & set3))
print("set2 & set3")
print(len(set2 & set3))

print("set1")
print(len(set1))
print("set2")
print(len(set2))
print("set3")
print(len(set3))






