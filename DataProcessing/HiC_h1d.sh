dir=/work3/WANG_cohesinDB/Curated/target/HiC/Needfastq/
juicer=~/software/juicer/juicer_tools_1.11.04_jcuda.0.8.jar
gt=~/git/HiC1DmetricsLocal/MainCode/gd/hg38/genome_table

for i in `ls $dir`
do
	echo $i
	for name in `ls $dir/$i/JuicerResults/`
	do
		echo $name
		file=$dir/$i/JuicerResults/$name/aligned/inter_30.hic
		#h1d basic dump $file 25000 all --gt $gt --normalize VC_SQRT -o $name --datatype rawhic --maxchr 22 -n 30
		h1d one IS $name/25000 25000 all --maxchr 22 --prefix observed.VC_SQRT. -n 30 -o $name/Insulation
	done
done	

dir2=/work3/WANG_cohesinDB/Curated/target/HiC/UsableHg38
for i in `ls $dir2 |sed 's/.hic//g'`
do
	echo $i
	name=$i
	file=$dir2/$i.hic
	#h1d basic dump $file 25000 all --gt $gt --normalize VC_SQRT -o $name --datatype rawhic --maxchr 22 -n 30
	h1d one IS $name/25000 25000 all --maxchr 22 --prefix observed.VC_SQRT. -n 30 -o $name/Insulation
done





