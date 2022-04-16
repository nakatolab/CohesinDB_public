loopdir=/work3/WANG_cohesinDB/Post2021Dec10/Curated/HiC/hiclink/loops

for i in `ls $loopdir`
do
       file=$loopdir/$i/merged_loops.bedpe
       name=$i
       if [ -f $loopdir/$i/merged_loops.bedpe ]
       then
	       ls $loopdir/$i/merged_loops.bedpe
	       prefix=`sed '1,2d' $file |head -1 |cut -f 1`
	       if [[ $prefix == chr* ]]
	       then
		       sed '1,2d' $file |\
			       awk -v OFS="\t" '{print $1,$2,$3,$4,$5,$6}'|\
			       pairToBed -a stdin -b allpromoter.bed > $name.loop2gene.temp
		else
		       sed '1,2d' $file |\
		       	awk -v OFS="\t" '{print "chr"$1,$2,$3,"chr"$4,$5,$6}'|\
		       	pairToBed -a stdin -b allpromoter.bed > $name.loop2gene.temp
	       fi
	      awk '$5<=$9 && $6>=$8' $name.loop2gene.temp | cut -f 1-3,7- >> $name.anchor2gene.temp
              awk '$2<=$9 && $3>=$8' $name.loop2gene.temp | cut -f 4-6,7- >> $name.anchor2gene.temp
              intersectBed -a $name.anchor2gene.temp -b allcohesin.pos -loj |\
                      cut -f 8,14 |sort|uniq > Post2021Dec/$name.gene2cohesin
       else
               ls $loopdir/$i/merged_loops.bedpe
               echo not exit
       fi
done

rm *temp


