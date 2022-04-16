dir=/work3/WANG_cohesinDB/Curated/target/HiC/Needfastq/
juicer=~/software/juicer/juicer_tools_1.11.04_jcuda.0.8.jar
newjuicer=~/software/juicer/juicer_tools.2.13.05.jar

mkdir eachchr
mkdir allchr

for i in `ls $dir `
do
	echo $i
	for name in `ls $dir/$i/JuicerResults/`
	do
		echo $name
		file=$dir/$i/JuicerResults/$name/aligned/inter_30.hic
		for chrname in `seq 1 22` X
        	do
                	echo $chrname
                	#java -Xms512m -Xmx200g -jar $newjuicer eigenvector VC_SQRT $file $chrname BP 250000 eachchr/$name.PC1.txt.$chrname.tmp
			paste pos_hg38_chr$chrname.txt eachchr/$name.PC1.txt.$chrname.tmp > $name.PC1.txt.$chrname.pos.unjustify.tmp
			/work/miniconda3/bin/python ~/PanCancer/Feb2022/Chapter4-3D-chromatin/compartment/corrGD.py $name.PC1.txt.$chrname.pos.unjustify.tmp ~/PanCancer/Feb2022/Chapter4-3D-chromatin/compartment/geneDensity/hg38.gd250k.txt.txt $name.PC1.txt.$chrname.pos.tmp
        	done

		cat $name.PC1.txt*pos.tmp > allchr/$name.PC1.txt
        	rm $name.PC1.txt*pos.tmp
		rm $name.PC1.txt*pos.unjustify.tmp	
	done
done	

dir2=/work3/WANG_cohesinDB/Curated/target/HiC/UsableHg38
for i in `ls $dir2 |sed 's/.hic//g'`
do
	echo $i
	name=$i
	file=$dir2/$i.hic
	for chrname in `seq 1 22` X
	do
		echo $chrname
		#java -Xms512m -Xmx200g -jar $newjuicer eigenvector VC_SQRT $file $chrname BP 250000 eachchr/$name.PC1.txt.$chrname.tmp
		paste pos_hg38_chr$chrname.txt eachchr/$name.PC1.txt.$chrname.tmp > $name.PC1.txt.$chrname.pos.unjustify.tmp
		/work/miniconda3/bin/python ~/PanCancer/Feb2022/Chapter4-3D-chromatin/compartment/corrGD.py $name.PC1.txt.$chrname.pos.unjustify.tmp ~/PanCancer/Feb2022/Chapter4-3D-chromatin/compartment/geneDensity/hg38.gd250k.txt.txt $name.PC1.txt.$chrname.pos.tmp
	done

	cat $name.PC1.txt*pos.tmp > allchr/$name.PC1.txt
        rm $name.PC1.txt*pos.tmp
	rm $name.PC1.txt*pos.unjustify.tmp
done

for i in `ls $dir2 |sed 's/.hic//g' | grep -E 'HiC_GSE155380_RT112|HiC_GSE118716|HiC_GSE105028_H9' `
do
        echo $i
        name=$i
        file=$dir2/$i.hic
        for chrname in `seq 1 22` X
        do
                echo $chrname
                #java -Xms512m -Xmx200g -jar $newjuicer eigenvector VC_SQRT $file chr$chrname BP 250000 $eachchr/$name.PC1.txt.$chrname.tmp
		paste pos_hg38_chr$chrname.txt eachchr/$name.PC1.txt.$chrname.tmp > $name.PC1.txt.$chrname.pos.unjustify.tmp
		/work/miniconda3/bin/python ~/PanCancer/Feb2022/Chapter4-3D-chromatin/compartment/corrGD.py $name.PC1.txt.$chrname.pos.unjustify.tmp ~/PanCancer/Feb2022/Chapter4-3D-chromatin/compartment/geneDensity/hg38.gd250k.txt.txt $name.PC1.txt.$chrname.pos.tmp
        done		
	
	cat $name.PC1.txt*pos.tmp > allchr/$name.PC1.txt
        rm $name.PC1.txt*pos.tmp
	rm $name.PC1.txt*pos.unjustify.tmp
done




