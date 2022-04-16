todir=/work3/WANG_cohesinDB/Curated/allprocessed/CohesinDB_real_data

#------------------------ChIP-seq------------------------#
#cd /work3/WANG_cohesinDB/Curated/target/ChIP-seq/singleend/macs
#for i in `ls *narrowPeak`
#do
#	echo $i
#	cp $i $todir
#done
#
#cd /work3/WANG_cohesinDB/Curated/target/ChIP-seq/singleend/parse2wigdir+
#for i in `ls *GR.100.bw`
#do
#	echo $i
#	cp $i $todir
#done
#
#cd /work3/WANG_cohesinDB/Curated/target/ChIP-seq/pairend/macs
#for i in `ls *narrowPeak`
#do
#        echo $i
#        cp $i $todir
#done
#
#cd /work3/WANG_cohesinDB/Curated/target/ChIP-seq/pairend/parse2wigdir+
#for i in `ls *GR.100.bw`
#do
#        echo $i
#        cp $i $todir
#done

#----------------------HiChIP-----------------------#
#cd /work3/WANG_cohesinDB/Curated/target/HiChIP/UsableHg38
#loopdir=/work3/WANG_cohesinDB/Curated/target/HiChIP/loops
#for i in `ls *.hic`
#do
#        echo $i
#        #cp $i $todir
#
#	name=`echo $i | sed 's/.hic//g'`
#	cp $loopdir/$name/merged_loops.bedpe $todir/$name.loop
#done
#
#cd /work3/WANG_cohesinDB/Curated/target/HiChIP/Needfastq
#for dir in `ls`
#do
#	cd /work3/WANG_cohesinDB/Curated/target/HiChIP/Needfastq/$dir/JuicerResults
#	echo $dir
#	for i in `ls`
#	do
#		echo $i
#		#cp $i/aligned/inter_30.hic $todir/$i.hic
#
#		cp $loopdir/$i/merged_loops.bedpe $todir/$i.loop
#	done
#done

#---------------------ChIA-PET------------------------#
#cd /work3/WANG_cohesinDB/Curated/target/ChIA
#for dir in `ls | grep -v Encode_Usable |grep -v ".sh"`
#do
#	echo $dir
#	cd /work3/WANG_cohesinDB/Curated/target/ChIA/$dir/mango
#	for i in `ls *fdr.mango`
#	do
#		echo $i
#		cp $i $todir
#		
#		name=`echo $i | sed 's/.mango//g'`
#		cat $i | awk '{print $1"\t"$2"\t"$3"\t"$4":"$5"-"$6","$7}'|sortBed > $todir/$name.longrange
#		bgzip $todir/$name.longrange
#		tabix -p bed $todir/$name.longrange.gz
#	done
#done

#cd /work3/WANG_cohesinDB/Curated/target/ChIA/Encode_Usable
#for i in `ls *bedpe.gz |sed 's/.gz//g'`
#do
#	echo $i
#	#gunzip -c $i.gz > $todir/$i
#	name=`echo $i | sed 's/.bedpe//g'`
#	cat $todir/$name.bedpe | awk '{print $1"\t"$2"\t"$3"\t"$4":"$5"-"$6","$7}'|sortBed > $todir/$name.longrange
#	bgzip $todir/$name.longrange
#	tabix -p bed $todir/$name.longrange.gz
#done

#RNA-seq 
#cd /work3/WANG_cohesinDB/Curated/dependent/RNA-seq/STARsingle
#for i in `ls *genes.results`
#do
#	echo $i
#	name=`echo $i | sed 's/.genes.results//g'`
#	cp $i $todir/$name.STAR.tsv
#	compare=`echo $i |cut -f 4 -d '_'`
#	cp /work3/WANG_cohesinDB/Curated/dependent/RNA-seq/rsem/$compare/Matrix.genes.count.GRCh38.edgeR.all.tsv $todir/$name.edgeR.tsv
#done

#cd /work3/WANG_cohesinDB/Curated/dependent/RNA-seq/STARpair
#for i in `ls *genes.results`
#do
#        echo $i
#	name=`echo $i | sed 's/.genes.results//g'`
#        cp $i $todir/$name.STAR.tsv
#        compare=`echo $i |cut -f 4 -d '_'`
#        cp /work3/WANG_cohesinDB/Curated/dependent/RNA-seq/rsem/$compare/Matrix.genes.count.GRCh38.edgeR.all.tsv $todir/$name.edgeR.tsv
#done

#Microarray
#cd /work3/WANG_cohesinDB/Curated/dependent/microarray/CohesinDB_microarray/rename
#for i in `ls`
#do
#	echo $i
#	cp $i $todir/$i
#done
#
##Hi-C
cd /work3/WANG_cohesinDB/Curated/target/HiC/UsableHg38
for i in `ls *.hic`
do
	#echo $i
	name=`echo $i | sed 's/.hic//g'`
	#cp $i $todir/$i
	#echo $name
	if [ -f /work3/WANG_cohesinDB/Curated/target/HiC/loops/$name/merged_loops.bedpe ]
	then
		echo exist
		cp /work3/WANG_cohesinDB/Curated/target/HiC/loops/$name/merged_loops.bedpe $todir/$name.loop
	else
		echo not exist
		echo too sparse matrix to call loops > $todir/$name.loop
	fi
	
	if [ -f /work3/WANG_cohesinDB/Curated/target/HiC/TAD/$name/25000_blocks.bedpe ]
        then
		echo exist
		cp /work3/WANG_cohesinDB/Curated/target/HiC/TAD/$name/25000_blocks.bedpe $todir/$name.tad
        else
		echo not exist
                echo too sparse matrix to call TADs > $todir/$name.tad
        fi

	#cp /work3/WANG_cohesinDB/Curated/target/HiC/loops/$name/merged_loops.bedpe $todir/$name.loop
	#cp /work3/WANG_cohesinDB/Curated/target/HiC/TAD/$name/25000_blocks.bedpe $todir/$name.tad	
done

cd /work3/WANG_cohesinDB/Curated/target/HiC/Needfastq
for dir in `ls`
do
       cd /work3/WANG_cohesinDB/Curated/target/HiC/Needfastq/$dir/JuicerResults
       #echo $dir
       for i in `ls | grep -v .sh`
       do
               #echo $i
               #cp $i/aligned/inter_30.hic $todir/$i.hic
	       name=$i
	       if [ -f /work3/WANG_cohesinDB/Curated/target/HiC/loops/$name/merged_loops.bedpe ]
	       then
		       echo exist
		       cp /work3/WANG_cohesinDB/Curated/target/HiC/loops/$name/merged_loops.bedpe $todir/$name.loop
	       else
		       echo not exist
		       echo too sparse matrix to call loops > $todir/$name.loop
	       fi

	       if [ -f /work3/WANG_cohesinDB/Curated/target/HiC/TAD/$name/25000_blocks.bedpe ]
               then
		       echo exist
		       cp /work3/WANG_cohesinDB/Curated/target/HiC/TAD/$name/25000_blocks.bedpe $todir/$name.tad
               else
		       echo not exist
		       echo too sparse matrix to call TADs > $todir/$name.tad
               fi
	       #cp /work3/WANG_cohesinDB/Curated/target/HiC/loops/$name/merged_loops.bedpe $todir/$name.loop
	       #cp /work3/WANG_cohesinDB/Curated/target/HiC/TAD/$name/25000_blocks.bedpe $todir/$name.tad
       done
done

