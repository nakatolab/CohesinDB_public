degdir=/work3/WANG_cohesinDB/Curated/dependent/RNA-seq/rsem

cut -f 1,2,9- /work3/WANG_cohesinDB/Curated/dependent/RNA-seq/rsem/compare1/Matrix.genes.TPM.GRCh38.txt |sed '1d' > allgene.idconverter

cd /work3/WANG_cohesinDB/Curated/allprocessed/CohesinDB_real_data
for i in `ls $degdir`
do
	file=$degdir/$i/Matrix.genes.count.GRCh38.edgeR.DEGs.tsv
	colnum=`head -1 $file| awk '{print NF}'|awk '{print $1-5}'`
	name=`ls *edgeR.tsv |cut -f 1-5 -d _|sort|uniq|grep -v _NT| grep _${i}_`
	echo $name
	cut -f 1,2,$colnum- $file |sed '1d' | awk '{print $2"\t"$1}'>/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/DEGs/eachfile/$name.genelist
done

cd /work3/WANG_cohesinDB/Curated/annotation_real/targetgene/DEGs 

microDir=/work3/WANG_cohesinDB/Curated/dependent/microarray/CohesinDB_microarray/DEGs
for m in `ls $microDir |grep -v JQ1`
do
	name=`echo $m | sed 's/.deg//g'`
	echo $name
	#python3 gene2id.py $microDir/$m ./eachfile/$name.genelist 
done

# python3 merge.py

#cat studyDF.tsv |sed 's/\t/,/g'|sed 's/\.,//g' | sed 's/,\.//g' > studyDFsum.tsv
#cat subunitDF.tsv | sed 's/\t/,/g'|sed 's/\.,//g' | sed 's/,\.//g' |\
#	sed 's/Auxin/Rad21/g'| sed 's/CTCF-CRISPR/CTCF/g'|sed 's/mutSA2/SA2/g'|\
#	sed 's/overSMC1/SMC1/g' |sed 's/Rad21-auxin/Rad21/g'|sed 's/Rad21-CRISPR/Rad21/g'|\
#	sed 's/Rad21mock/Rad21/g' | sed 's/Rad21mut/Rad21/g' | sed 's/SA1-AID/SA1/g'|\
#	sed 's/SA2-AID/SA2/g' | sed 's/SA2-CRISPR$/SA2$/g' | sed 's/SA2-CRISPR-heterozygous/SA2/g'|\
#	sed 's/SA2-CRISPR-homozygous/SA2/g'|sed 's/SA2KO/SA2/g'|sed 's/SA2-KO/SA2/g'|\
#	sed 's/shBORIS/BORIS/g' | sed 's/sh//g' | sed 's/si//g'| sed 's/-3h//g'|sed 's/-6h//g'|\
#	sed 's/-KO//g' |sed 's/mut//g' |sed 's/-CRISPR//g' |sed 's/-AID//g' > subunitDFsum.tsv
#
#python3 removedup.py studyDFsum.tsv studyDFsumUniq.temp
#python3 removedup.py subunitDFsum.tsv subunitDFsumUniq.temp
#
#cat studyDFsumUniq.temp| sed 's/"//g' | sed 's/^,//g' > studyDFsumUniq.tsv
#cat subunitDFsumUniq.temp| sed 's/"//g' | sed 's/^,//g' > subunitDFsumUniq.tsv
#rm *temp

paste allgene.idconverter whetherDFsum.tsv studyDFsumUniq.tsv subunitDFsumUniq.tsv |\
	awk -v OFS='\t' '{ if ($9>2) print $3,$5,$6,$4,$2,$1,$7,$8,"True",$9,$10,$11; else print $3,$5,$6,$4,$2,$1,$7,$8,"False",$9,$10,$11 }' > allgene.DEG.info

#awk -v OFS="\t" '{print $1,$2,$3,$1"-"$2"-"$3}' ../../allcohesin_merge200bp_twodata.bed > allcohesin.pos

awk '$10>1' allgene.DEG.info | cut -f 1-3,5-6 |\
       	bedtools slop -i stdin -g ~/database/genometable_all.txt -b 2000000 | \
	intersectBed -a stdin -b allcohesin.pos -loj |cut -f 4,9 > gene2cohesin.pair



