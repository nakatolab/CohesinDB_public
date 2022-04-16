#step1 define what is cohesin sites.
#2021nov使用allcohesin_merge200bp_twodata.bed

#cp ~/PanCancer/Sep2021/mergePeak/allcohesin.bed .
#cut -f 1-3 ~/PanCancer/Sep2021/mergePeak/PeakOccurrenceScore.csv |sed '1d' > allcohesin_merge200bp.bed
#cat ~/PanCancer/Sep2021/mergePeak/PeakOccurrenceScore.csv |sed '1d'|awk '($5+$8) > 1'|cut -f 1-3 > allcohesin_merge200bp_twodata.bed
#cp -r ~/PanCancer/Aug2021/peaks/allpeak/ . 
allcohesin=allcohesin_merge200bp_twodata.bed

#------------------------------------
#step2 id subunit cell
#for i in `ls allpeak`
#do
#	#echo $i
#	id=`echo $i | cut -f 2 -d _`
#        cell=`echo $i | cut -f 3 -d _`
#        subunit=`echo $i | cut -f 4 -d _`
	#mapBed -a $allcohesin -b allpeak/$i > $i.temp
        #cut -f 4 $i.temp |sed "s/[0-9]\+/$id/g" > $i.id.temp
        #cut -f 4 $i.temp |sed "s/[0-9]\+/$subunit/g" > $i.subunit.temp
        #cut -f 4 $i.temp |sed "s/[0-9]\+/$cell/g" > $i.cell.temp
#done

#paste *.id.temp -d , | sed 's/\.,//g' |sed 's/\.//g' > allcohesin.allid
#rm *.id.temp
#paste *.subunit.temp -d , | sed 's/\.,//g' |sed 's/\.//g' > allcohesin.allsubunit
#rm *.subunit.temp

#paste *.cell.temp  > allcell.temp
#cat allcell.temp |sed 's/\.//g' |awk '{print NF}' > allcell.presence
#cat allcell.temp |awk '{print NF}' > allcell.count
#paste allcell.count allcell.presence | awk '{print $2/$1}' > allcohesin.tissuespecific
#rm allcell.*

#paste *.cell.temp -d , | sed 's/\.,//g' |sed 's/\.//g' > allcohesin.allcell
#rm *.cell.temp
#rm *.temp

#python3 removedup.py
#cat allcohesin.allid.unique | sed 's/"//g' | sed 's/^,//g' > allcohesin.uniqueID
#cat allcohesin.allcell.unique | sed 's/"//g' | sed 's/^,//g' > allcohesin.uniqueCell
#cat allcohesin.allsubunit.unique | sed 's/"//g' | sed 's/^,//g' > allcohesin.uniqueSubunit
#rm allcohesin.all*

#------------------------------------
#step3 CTCF
#cp ~/PanCancer/Sep2021/focusCommon/CTCF/allCTCF.bed .
#intersectBed -a $allcohesin -b allCTCF.bed -c |\
#       awk -v OFS="\t" '{if ($4==0) print $1,$2,$3,"non-CTCF"; else print $1,$2,$3,"CTCF"}' \
#       | cut -f 4 > allcohesin.CTCFdep

#------------------------------------
#step4 Enhancers
#cp /work3/WANG_cohesinDB/Curated/annotation_demo/FantomEnhancer/F5.hg38.enhancers.bed .
#intersectBed -a $allcohesin -b F5.hg38.enhancers.bed  -c |\
#       awk -v OFS="\t" '{if ($4==0) print $1,$2,$3,"non-Enhancer"; else print $1,$2,$3,"Enhancer"}' \
#       | cut -f 4 > allcohesin.enhancers

#------------------------------------
#step5 Remap TFs
#intersectBed -a $allcohesin -b /work3/WANG_cohesinDB/TFbed/ReMap_hg38_CRMs.bed  -loj | \
#       cut -f 1-3,7 |awk -v OFS="\t" '{print $0,$1"-"$2"-"$3}'|\
#               awk '!i[$5]++'| cut -f 4 > allcohesin.CRMs.temp
#python3 removedup-CRM.py 
#sed 's/"//g' allcohesin.CRMs.unique > allcohesin.CRMs

#------------------------------------
#step6 Hubs
#hubdir=/work3/WANG_cohesinDB/Curated/target/HiC/hub/hubresult
#cat $hubdir/* > allhub.bed
#intersectBed -a $allcohesin -b allhub.bed  -c |\
#       awk -v OFS="\t" '{if ($4==0) print $1,$2,$3,"non-Hub"; else print $1,$2,$3,"Hub"}' \
#       | cut -f 4 > allcohesin.hub

#------------------------------------
#step7 TAD border
#TADdir=/work3/WANG_cohesinDB/Curated/target/HiC/TAD
#touch allborder.temp
#for i in `ls $TADdir`
#do
#	if [ -f $TADdir/$i/25000_blocks.bedpe ]
#	then
#		ls $TADdir/$i/25000_blocks.bedpe
#		sed '1,2d' $TADdir/$i/25000_blocks.bedpe | cut -f 1-3 |awk -v OFS="\t"  '{print "chr"$1,$2-25000,$2+25000}' >> allborder.temp
#		sed '1,2d' $TADdir/$i/25000_blocks.bedpe | cut -f 1-3 |awk -v OFS="\t"  '{print "chr"$1,$3-25000,$3+25000}' >> allborder.temp
#	else
#		echo not exit
#	fi
#done
#
#mv allborder.temp allborder.bed
#
cat allborder.bed ./April2022/border_postHiC.bed |\
	intersectBed -a $allcohesin -b stdin  -c |\
       awk -v OFS="\t" '{if ($4==0) print $1,$2,$3,"non-Boundary"; else print $1,$2,$3,"Boundary"}' \
       | cut -f 4 > allcohesin.boundary

#------------------------------------
#step8 SNP
#cp /work3/WANG_cohesinDB/Curated/annotation_demo/SNP/snp.bed .
#intersectBed -a $allcohesin -b snp.bed  -loj | \
#       cut -f 1-3,7 |awk -v OFS="\t" '{print $0,$1"-"$2"-"$3}'|\
#       awk '!i[$5]++'| cut -f 4 > allcohesin.SNP

#---------------------------------------
#step9 loop anchor
#loopdir=/work3/WANG_cohesinDB/Curated/target/HiC/loops
#touch allloop.temp
#for i in `ls $loopdir`
#do
#	if [ -f $loopdir/$i/merged_loops.bedpe ]
#	then
#		ls $loopdir/$i/merged_loops.bedpe
#		sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-3 | awk -v OFS="\t" '{print "chr"$1,$2,$3}' >> allloop.temp
#		sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 4-6 | awk -v OFS="\t" '{print "chr"$1,$2,$3}' >> allloop.temp
#	else
#		ls $loopdir/$i/merged_loops.bedpe
#		echo not exit
#	fi
#done
#
#mv allloop.temp all_hicloop.bed
#
cat all_hicloop.bed ./April2022/loopanchor_postHiC.bed |\
	intersectBed -a $allcohesin -b stdin  -c |\
	awk -v OFS="\t" '{if ($4==0) print $1,$2,$3,"non-hicloop"; else print $1,$2,$3,"hicloop"}' \
	| cut -f 4 > allcohesin.hicloop

#
#loopdir=/work3/WANG_cohesinDB/Curated/target/HiChIP/loops
#touch allloop.temp
#for i in `ls $loopdir`
#do
#	if [ -f $loopdir/$i/merged_loops.bedpe ]
#        then
#                ls $loopdir/$i/merged_loops.bedpe
#                sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-3 | awk -v OFS="\t" '{print "chr"$1,$2,$3}' >> allloop.temp
#                sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 4-6 | awk -v OFS="\t" '{print "chr"$1,$2,$3}' >> allloop.temp
#        else
#                ls $loopdir/$i/merged_loops.bedpe
#                echo not exit
#        fi
#done
#mv allloop.temp all_hichiploop.bed
#
#intersectBed -a $allcohesin -b all_hichiploop.bed  -c |\
#       awk -v OFS="\t" '{if ($4==0) print $1,$2,$3,"non-hichiploop"; else print $1,$2,$3,"hichiploop"}' \
#       | cut -f 4 > allcohesin.hichiploop
#
#
#
#loopdir=/work3/WANG_cohesinDB/Curated/allprocessed/CohesinDB_real_data
#touch allloop.temp
#for i in `ls $loopdir/ChIAPET*bedpe`
#do
#	cut -f 1-3 $i >> allloop.temp
#	cut -f 4-6 $i >> allloop.temp
#done
#
#for i in `ls $loopdir/ChIAPET*mango`
#do
#        cut -f 1-3 $i >> allloop.temp
#        cut -f 4-6 $i >> allloop.temp
#done
#
#mv allloop.temp all_chialoop.bed
#
#intersectBed -a $allcohesin -b all_chialoop.bed  -c |\
#       awk -v OFS="\t" '{if ($4==0) print $1,$2,$3,"non-chialoop"; else print $1,$2,$3,"chialoop"}' \
#       | cut -f 4 > allcohesin.chialoop

#--------------------------------------
#step10 target gene
#awk -v OFS="\t" '{print $1,$2,$3,$1"-"$2"-"$3}' $allcohesin > allcohesin.pos
#python eachcohesin.py

#---------------------------------------
#step11 location
#cp location/allcohesin.location .

#-------------------------------
#step12 mutation
#intersectBed -a $allcohesin -b mutation/mutation_code.bed  -c |\
#	cut -f 4 > allcohesin.codingmutation

#intersectBed -a $allcohesin -b mutation/mutation_noncode.bed  -c |\
#        cut -f 4 > allcohesin.noncodingmutation

#-----------------------------------------
#merge all
paste $allcohesin allcohesin.uniqueID allcohesin.uniqueCell \
	allcohesin.tissuespecific allcohesin.uniqueSubunit allcohesin.CTCFdep allcohesin.location \
	allcohesin.boundary allcohesin.hub allcohesin.hicloop allcohesin.hichiploop allcohesin.chialoop \
        allcohesin.enhancers allcohesin.CRMs allcohesin.targetGeneName allcohesin.targetGeneID \
	allcohesin.SNP allcohesin.codingmutation allcohesin.noncodingmutation \
	./April2022/allcohesin.CTCFmotif ./April2022/allcohesin.SuperEnhancer ./April2022/allcohesin.ACompartPercent ./April2022/allcohesin.top2HMM |\
	sed '1iBasic-Chrom\tBasic-Start\tBasic-End\tBasic-Study\tBasic-CellType\tCategory-CellSpecificity\tCategory-Subunit\tCategory-CTCF\tCategory-Location\t3Dgenome-Boundary\t3Dgenome-Hub\t3Dgenome-HiCloop\t3Dgenome-HiChIPloop\t3Dgenome-ChIAloop\tCis-Enhancer\tCis-CobindTF\tCis-TargetGeneName\tCis-TargetGeneID\tFunction-SNP\tFunction-CodeMutation\tFunction-NoncodeMutation\tAddition-CTCFmotif\tAddition-SuperEnhancer\tAddition-CompartA\tAddition-top1HMMname\tAddition-top1HMMper\tAddition-top2HMMname\tAddition-top2HMMper' \
	> allcohesin.final

