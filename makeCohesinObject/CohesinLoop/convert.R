library(dplyr)

args=commandArgs(T)
input=args[1]
output=args[2]
print(input)
print(output)

df1 <- read.csv(input,sep='\t')
colnames(df1) <- c("text","feature")
df2 <- df1 %>% group_by(text) %>% summarise(feature = paste(feature, collapse = ","))
df3 <- as.data.frame(df2)
write.table(df3,output,sep="\t",quote=F,row.names=F,col.names=F)

