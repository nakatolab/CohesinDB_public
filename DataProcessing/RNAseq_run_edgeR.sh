db=Ensembl
build=GRCh38
gtf=/work/Database/Ensembl/GRCh38/release103/gtf_chrUCSC/Homo_sapiens.GRCh38.103.chr.gtf

mkdir -p rsem

for i in `ls singleend |cut -f 4 -d "_" |sort |uniq`
do
	date
	echo $i
	mkdir -p rsem/$i
	controlnum=`ls singleend/*_${i}_NT*|wc -l`
	controlname=`ls singleend/*_${i}_NT* | cut -f 1 -d "."|cut -f 5 -d "_"|uniq`
	treatnum=`ls singleend/*_${i}_* | grep -v _${i}_NT_ |wc -l`
	treatname=`ls singleend/*_${i}_* | grep -v _${i}_NT_ | cut -f 5 -d "_"|uniq`		
	samplelist=`ls singleend/*_${i}_NT* | cut -f 1 -d "." | sed 's/singleend/STARsingle/g'; ls singleend/*_${i}_* | cut -f 1 -d "." | sed 's/singleend/STARsingle/g' | grep -v _${i}_NT_ `
	#samplelist=`ls singleend/*_${i}_* | cut -f 1 -d "." | sed 's/singleend/STARsingle/g'` # | tr -s "\n" " " `
	#echo $controlnum
	#echo $controlname
	#echo $treatnum
	#echo $treatname	
	#echo $samplelist
	#rsem_merge.sh "$samplelist" rsem/$i/Matrix $db $build $gtf "XXX"
	#edgeR.sh rsem/$i/Matrix $db $build $controlnum:$treatnum $controlname:$treatname 0.01
	echo =====================
done


for i in `ls pairend |cut -f 4 -d "_" |sort |uniq `
do
        date
        echo $i
        mkdir -p rsem/$i
        controlnum=`ls pairend/*_${i}_NT*| cut -f 1 -d "." |uniq|  wc -l`
        controlname=`ls pairend/*_${i}_NT* | cut -f 1 -d "."| cut -f 5 -d "_"|uniq`
        treatnum=`ls pairend/*_${i}_* | grep -v _${i}_NT_ | cut -f 1 -d "." |uniq|  wc -l`
        treatname=`ls pairend/*_${i}_* | grep -v _${i}_NT_ | cut -f 5 -d "_"|uniq`
        samplelist=`ls pairend/*_${i}_NT* | cut -f 1 -d "." |uniq| sed 's/pairend/STARpair/g'; ls pairend/*_${i}_* | cut -f 1 -d "." |uniq| sed 's/pairend/STARpair/g' | grep -v _${i}_NT_ `
        echo $controlnum
        echo $controlname
        echo $treatnum
        echo $treatname
        echo $samplelist
        rsem_merge.sh "$samplelist" rsem/$i/Matrix $db $build $gtf "XXX"
        edgeR.sh rsem/$i/Matrix $db $build $controlnum:$treatnum $controlname:$treatname 0.01
        echo =====================
done





