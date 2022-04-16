touch allstudy.temp
touch allcell.temp
touch allsubunit.temp
touch allassay.temp

loopdir=/work3/WANG_cohesinDB/Curated/target/HiChIP/loops
for i in `ls $loopdir`
do
       if [ -f $loopdir/$i/merged_loops.bedpe ]
       then
                ls $loopdir/$i/merged_loops.bedpe
		study=`echo $i | cut -f 2 -d _`
		cell=`echo $i | cut -f 3 -d _`
		subunit=`echo $i | cut -f 4 -d _`
		assay="Hi-ChIP"

                sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
		       	awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$study'"}' >> allstudy.temp
       		sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$cell'"}' >> allcell.temp
		sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$subunit'"}' >> allsubunit.temp
		sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$assay'"}' >> allassay.temp
	else
                ls $loopdir/$i/merged_loops.bedpe
                echo not exit
       fi
done

loopdir=/work3/WANG_cohesinDB/Curated/target/HiC/loops
for i in `ls $loopdir`
do
       if [ -f $loopdir/$i/merged_loops.bedpe ]
       then
                ls $loopdir/$i/merged_loops.bedpe
                study=`echo $i | cut -f 2 -d _`
		cell=`echo $i | cut -f 3 -d _`
		subunit="Other"
		assay="Hi-C"

                sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$study'"}' >> allstudy.temp
		sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$cell'"}' >> allcell.temp
                sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$subunit'"}' >> allsubunit.temp
                sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$assay'"}' >> allassay.temp
       else
                ls $loopdir/$i/merged_loops.bedpe
                echo not exit
       fi
done

loopdir=/work3/WANG_cohesinDB/Post2021Dec10/Curated/HiC/hiclink/loops
for i in `ls $loopdir`
do
       if [ -f $loopdir/$i/merged_loops.bedpe ]
       then
	       	eachloop=$loopdir/$i/merged_loops.bedpe
		ls $eachloop
                study=`echo $i | cut -f 2 -d _`
                cell=`echo $i | cut -f 3 -d _`
                subunit="Other"
                assay="Hi-C"
		
		prefix=`sed '1,2d' $eachloop |head -1 |cut -f 1`
		if [[ $prefix == chr* ]]
		then
			sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        	awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$study'"}' >> allstudy.temp
                	sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        	awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$cell'"}' >> allcell.temp
                	sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        	awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$subunit'"}' >> allsubunit.temp
                	sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        	awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$assay'"}' >> allassay.temp
		else
			sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        	awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$study'"}' >> allstudy.temp
                	sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        	awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$cell'"}' >> allcell.temp
                	sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        	awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$subunit'"}' >> allsubunit.temp
                	sed '1,2d' $loopdir/$i/merged_loops.bedpe | cut -f 1-6 |\
                        	awk '{print "chr"$1"+"$2"+"$3"+""chr"$4"+"$5"+"$6"\t""'$assay'"}' >> allassay.temp
		fi
       else
                ls $loopdir/$i/merged_loops.bedpe
                echo not exit
       fi
done


chiadir=/work3/WANG_cohesinDB/Curated/allprocessed/CohesinDB_real_data
#for i in `ls $chiadir | grep ChIAPET |grep bedpe`
#do
#	wc -l $chiadir/$i
#	study=`echo $i | cut -f 2 -d _`
#	cut -f 1-6 $chiadir/$i | awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$study'"}' >> allstudy.temp
#done

for i in `ls $chiadir | grep ChIAPET |grep mango`
do
	wc -l $chiadir/$i
	study=`echo $i | cut -f 2 -d _`
        cell=`echo $i | cut -f 3 -d _`
        subunit=`echo $i | cut -f 4 -d _`
        assay="ChIA-PET"
	cut -f 1-6 $chiadir/$i | awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$study'"}' >> allstudy.temp
	cut -f 1-6 $chiadir/$i | awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$cell'"}' >> allcell.temp
	cut -f 1-6 $chiadir/$i | awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$subunit'"}' >> allsubunit.temp
	cut -f 1-6 $chiadir/$i | awk '{print $1"+"$2"+"$3"+"$4"+"$5"+"$6"\t""'$assay'"}' >> allassay.temp
done

Rscript convert.R allstudy.temp allstudy.unique
Rscript convert.R allcell.temp allcell.unique
Rscript convert.R allsubunit.temp allsubunit.unique
Rscript convert.R allassay.temp allassay.unique

cut -f 1 allstudy.unique | sed 's/+/\t/g' > allloop.pos
cut -f 2 allstudy.unique > allloop.study
cut -f 2 allcell.unique > allloop.cell
cut -f 2 allsubunit.unique > allloop.subunit
cut -f 2 allassay.unique > allloop.assay

python3 removedup.py allloop.study allloop.study.temp
python3 removedup.py allloop.cell allloop.cell.temp
python3 removedup.py allloop.subunit allloop.subunit.temp
python3 removedup.py allloop.assay allloop.assay.temp

paste allloop.pos allloop.assay.temp allloop.subunit.temp allloop.cell.temp allloop.study.temp |\
       	sed 's/"//g' | awk -v OFS="\t" '{print $0,(($5+$6)/2-($2+$3)/2)/1000}' |\
       sed '1iChrom1\tStart1\tEnd1\tChrom2\tStart2\tEnd2\tAssay\tSubunit\tCelltype\tStudy\tLooplength'	> allloop.final

rm *temp

