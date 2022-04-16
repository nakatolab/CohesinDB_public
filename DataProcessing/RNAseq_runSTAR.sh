db=Ensembl
build=GRCh38

for i in `ls pairend |cut -f 1 -d "."|sort|uniq`
do
	date
	echo $i
	./star_wang.sh -d STARpair paired $i "pairend/$i.pair_1.fastq.gz pairend/$i.pair_2.fastq.gz" $db $build reverse
done







db=Ensembl
build=GRCh38


#for i in `ls singleend |cut -f 1 -d "."|sort|uniq`
#do
#        date
#        echo $i
#        ./star_wang.sh -d STARsingle single $i singleend/$i.single.fastq.gz  $db $build reverse
#done


./star_wang.sh -d STARsingle single GROseq_GSE115603_MCF7_compare3_siRad21_EtOH_rep3 singleend/GROseq_GSE115603_MCF7_compare3_siRad21_EtOH_rep3.single.fastq.gz  $db $build reverse


