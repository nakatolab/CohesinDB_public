##awk -v OFS="\t" '{ if ($4=="+") print $3,$5-5000,$5+5000,$4,$2,$1,$8; else print $3,$6-5000,$6+5000,$4,$2,$1,$8  }' allgene.idconverter |\
##	awk -v OFS="\t" '{ if ($2<0) print $1,0,$3,$4,$5,$6,$7; else print $0 }' > allpromoter.bed

awk -v OFS="\t" '{print $3,$5,$6,$4,$2,$1,$8}' allgene.idconverter|\
	bedtools slop -i stdin -g ~/database/genometable_all.txt -b 5000 > allpromoter.bed

awk -v OFS="\t" '{print $1,$2,$3,$1"-"$2"-"$3}' ../../allcohesin_merge200bp_twodata.bed > allcohesin.pos


loopdir=/work3/WANG_cohesinDB/Curated/target/HiC/loops
for i in `ls $loopdir`
do
	file=$loopdir/$i/merged_loops.bedpe
	name=$i
	if [ -f $loopdir/$i/merged_loops.bedpe ]
        then
               ls $loopdir/$i/merged_loops.bedpe
	       sed '1,2d' $file |\
		       awk -v OFS="\t" '{print "chr"$1,$2,$3,"chr"$4,$5,$6}'| pairToBed -a stdin -b allpromoter.bed > $name.loop2gene.temp
	       awk '$5<=$9 && $6>=$8' $name.loop2gene.temp | cut -f 1-3,7- >> $name.anchor2gene.temp
               awk '$2<=$9 && $3>=$8' $name.loop2gene.temp | cut -f 4-6,7- >> $name.anchor2gene.temp
	       intersectBed -a $name.anchor2gene.temp -b allcohesin.pos -loj |\
		       cut -f 8,14 |sort|uniq > eachfile/$name.gene2cohesin
       else
               ls $loopdir/$i/merged_loops.bedpe
               echo not exit
       fi
done

loopdir=/work3/WANG_cohesinDB/Curated/target/HiChIP/loops
for i in `ls $loopdir`
do
        file=$loopdir/$i/merged_loops.bedpe
        name=$i
       if [ -f $loopdir/$i/merged_loops.bedpe ]
       then
               ls $loopdir/$i/merged_loops.bedpe
               sed '1,2d' $file |\
		       awk -v OFS="\t" '{print "chr"$1,$2,$3,"chr"$4,$5,$6}'| pairToBed -a stdin -b allpromoter.bed > $name.loop2gene.temp
	       awk '$5<=$9 && $6>=$8' $name.loop2gene.temp | cut -f 1-3,7- >> $name.anchor2gene.temp
               awk '$2<=$9 && $3>=$8' $name.loop2gene.temp | cut -f 4-6,7- >> $name.anchor2gene.temp
               intersectBed -a $name.anchor2gene.temp -b allcohesin.pos -loj |\
                       cut -f 8,14 |sort|uniq > eachfile/$name.gene2cohesin
       else
               ls $loopdir/$i/merged_loops.bedpe
               echo not exit
       fi
done

loopdir=/work3/WANG_cohesinDB/Curated/allprocessed/CohesinDB_real_data

for i in `ls $loopdir | grep ChIAPET_ | grep .mango`
do
	file=$loopdir/$i
	name=`echo $i | sed 's/.interactions.fdr.mango//g'`
	ls $file
        cut -f 1-6 $file| pairToBed -a stdin -b allpromoter.bed > $name.loop2gene.temp
        awk '$5<=$9 && $6>=$8' $name.loop2gene.temp | cut -f 1-3,7- >> $name.anchor2gene.temp
	awk '$2<=$9 && $3>=$8' $name.loop2gene.temp | cut -f 4-6,7- >> $name.anchor2gene.temp
	intersectBed -a $name.anchor2gene.temp -b allcohesin.pos -loj |\
		cut -f 8,14 |sort|uniq > eachfile/$name.gene2cohesin
done

#for i in `ls $loopdir | grep ChIAPET_ | grep .bedpe`
#do
#        file=$loopdir/$i
#        name=`echo $i | sed 's/.bedpe//g'`
#        ls $file
#        cut -f 1-6 $file| pairToBed -a stdin -b allpromoter.bed > $name.loop2gene.temp
#        cut -f 1-3,7- $name.loop2gene.temp >> $name.anchor2gene.temp
#        cut -f 1-3,7- $name.loop2gene.temp >> $name.anchor2gene.temp
#        intersectBed -v -a $name.anchor2gene.temp -b allpromoter.bed |\
#                intersectBed -a stdin -b allcohesin.pos -loj |\
#                cut -f 8,14 |sort|uniq > eachfile/$name.gene2cohesin
#done


rm *temp

intersectBed -a allpromoter.bed -b allcohesin.pos -loj |cut -f 5,11 |grep -v [.] |sort|uniq > eachfile/Direct_Direct_Direct_Other_Other_Other_Other.gene2cohesin

bash Post2021dec.sh
cp Post2021Dec/* eachfile 

cat eachfile/* | sort|uniq | grep -v [.] > gene2cohesin.pair
for f in `ls eachfile | sed 's/.gene2cohesin//g'`
do
	cut -f 1 eachfile/$f.gene2cohesin | sort | uniq > eachfile_uniqgene/$f.uniqgene
done

python3 merge_speedup.py

cat interactionDF.tsv | sed 's/\t/,/g'  |sed 's/\.,//g'| sed 's/,\.//g' > interactionDFsum.tsv
python3 removedup.py interactionDFsum.tsv interactionDFsumUniq.temp
cat interactionDFsumUniq.temp| sed 's/"//g' | sed 's/^,//g' > interactionDFsumUniq.tsv

awk '{ if ($1==".") print "False"; else print "True" }' interactionDFsumUniq.tsv > whetherLoop.tsv


cat studyDF.tsv | sed 's/\t/,/g'  |sed 's/\.,//g'| sed 's/,\.//g' > studyDFsum.tsv
python3 removedup.py studyDFsum.tsv studyDFsumUniq.temp
cat studyDFsumUniq.temp| sed 's/"//g' | sed 's/^,//g' > studyDFsumUniq.tsv

cat subunitDF.tsv | sed 's/\t/,/g'  |sed 's/\.,//g'| sed 's/,\.//g' |\
	sed 's/DdeI/Other/g'|sed 's/DpnII/Other/g' | sed 's/HindIII/Other/g' |\
	sed 's/MboI/Other/g' | sed 's/MseI/Other/g' | sed 's/NcoI/Other/g' |\
	sed 's/NcolI/Other/g' >subunitDFsum.tsv
python3 removedup.py subunitDFsum.tsv subunitDFsumUniq.temp
cat subunitDFsumUniq.temp| sed 's/"//g' | sed 's/^,//g' > subunitDFsumUniq.tsv

rm *temp
