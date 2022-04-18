import pandas as pd

#alist =['chr10-30311722-30311958', 'chr10-30322945-30323281', 'chr10-30324758-30324947', 'chr1-82973177-82973486', 'chr1-82978784-82979067', 'chr1-82979120-82979191','chr10-30325498-30325742','chr10-30329311-30329516', 'chr10-30337193-30337479', 'chr10-30338353-30338704', 'chr10-30344748-30345045', 'chr10-30348321-30349689', 'chr10-30310380-30310569']
#print(alist)

def merge(alist,glist=None):
    dfpre = []
    for i in alist:
        dfpre.append(i.split("-"))
    df = pd.DataFrame(dfpre)
    if glist:
        df['gene'] = glist
    df.sort_values(by=[0,1],inplace=True)
    dfcopy = df.copy()

    outlist = []
    for i in range(df.shape[0]):
        if i == 0 or df.iloc[i,0] != df.iloc[i-1,0]:
            outlist.append(str(df.iloc[i,0])+"-"+str(df.iloc[i,1])+"-"+str(df.iloc[i,2]))
            j = 1
        else:
            if int(df.iloc[i,1]) - int(df.iloc[i-1,2]) > 50000:
                outlist.append(str(df.iloc[i,0])+"-"+str(df.iloc[i,1])+"-"+str(df.iloc[i,2]))
                j = 1
            else:
                outlist.append("same")
                for k in range(j+1):
                    df.iloc[i-k,0:3] = [df.iloc[i,0],df.iloc[i-1,1],df.iloc[i,2]]
                j +=1

    df['peak'] = df[0]+"-"+df[1]+'-'+df[2]
    df['rawpeak'] = dfcopy[0]+"-"+dfcopy[1]+'-'+dfcopy[2]
    return(df)
