build=hg38
index=/home/Database/bowtie-indexes/UCSC-$build
gt=/home/Database/UCSC/$build/genome_table

myMango_short_encode(){
	dir=$1
	fastq=`ls $dir/fastq |cut -f 1 -d '.'|sort|uniq`

	mango="Rscript /home/wang/software/mango/mango_multithreads_wang/mango_encode.R"
	mkdir -p $dir/mango

	for i in $fastq
	do
        	echo $i
        	echo step1 unzip------
        	#unpigz -p 40 -k $dir/fastq/${i}.pair_1.fastq.gz
        	#unpigz -p 40 -k $dir/fastq/${i}.pair_2.fastq.gz

        	echo step2 run mango------
        	$mango --fastq1 $dir/fastq/${i}.pair_1.fastq \
        	   --fastq2 $dir/fastq/${i}.pair_2.fastq \
        	   --prefix     $dir/mango/$i \
        	   --bowtieref $index \
        	   --bedtoolsgenome $gt \
        	   --chromexclude chrM,chrY \
        	   --stages 1:5 \
        	   --reportallpairs TRUE \
       		   --MACS_qvalue 0.05 --threads 50
	done
}

#myMango_short_encode ENCSR033GUP
#myMango_short_encode ENCSR299VMZ
#myMango_short_encode ENCSR312TUD
#myMango_short_encode ENCSR479MTN
#myMango_short_encode ENCSR527RXH
#myMango_short_encode ENCSR752QCX 
myMango_short_encode ENCSR000CAC
myMango_short_encode ENCSR000CAD

myMango_long_encode(){
        dir=$1
        fastq=`ls $dir/fastq |cut -f 1 -d '.'|sort|uniq`

        mango="Rscript /home/wang/software/mango/mango_multithreads_wang/mango_encode.R"
        mkdir -p $dir/mango

        for i in $fastq
        do
                echo $i
                echo step1 unzip------
                unpigz -p 40 -k $dir/fastq/${i}.pair_1.fastq.gz
                unpigz -p 40 -k $dir/fastq/${i}.pair_2.fastq.gz

                echo step2 run mango------
                $mango --fastq1 $dir/fastq/${i}.pair_1.fastq \
                   --fastq2 $dir/fastq/${i}.pair_2.fastq \
                   --prefix     $dir/mango/$i \
                   --bowtieref $index \
                   --bedtoolsgenome $gt \
                   --chromexclude chrM,chrY \
                   --stages 1:5 \
                   --reportallpairs TRUE \
                   --MACS_qvalue 0.05 --threads 50 \
		   --keepempty TRUE \
		   --shortreads FALSE \
		   --maxlength 1000
        done
}


#myMango_long_encode ENCSR981FNA
#myMango_long_encode ENCSR110JOO
#myMango_long_encode ENCSR672RHL
#myMango_long_encode ENCSR732QOH
#myMango_long_encode ENCSR587DSF
#myMango_long_encode ENCSR478BMT
#myMango_long_encode ENCSR381DCY
#myMango_long_encode ENCSR146FPM
#myMango_long_encode ENCSR386KHY
#myMango_long_encode ENCSR933UZH
#myMango_long_encode ENCSR991JXX
#myMango_long_encode ENCSR361AYD
#myMango_long_encode ENCSR314HAC
#myMango_long_encode ENCSR338WUS
#myMango_long_encode ENCSR404HWQ
#myMango_long_encode ENCSR113OIR
#myMango_long_encode ENCSR255XYX
#myMango_long_encode ENCSR778FXH
#myMango_long_encode ENCSR452NHL
#myMango_long_encode ENCSR833CMG
#myMango_long_encode ENCSR247RGI
#myMango_long_encode ENCSR668RDP
#myMango_long_encode ENCSR128RPG
#myMango_long_encode ENCSR658RQQ

myMango_long_sra(){
        dir=$1
        fastq=`ls $dir/fastq |cut -f 1 -d '.'|sort|uniq`

        mango="Rscript /home/wang/software/mango/mango_multithreads_wang/mango_SRA.R"
        mkdir -p $dir/mango

        for i in $fastq
        do
                echo $i
                echo step1 unzip------
                #unpigz -p 40 -k $dir/fastq/${i}.pair_1.fastq.gz
                #unpigz -p 40 -k $dir/fastq/${i}.pair_2.fastq.gz

                echo step2 run mango------
                $mango --fastq1 $dir/fastq/${i}.pair_1.fastq \
                   --fastq2 $dir/fastq/${i}.pair_2.fastq \
                   --prefix     $dir/mango/$i \
                   --bowtieref $index \
                   --bedtoolsgenome $gt \
                   --chromexclude chrM,chrY \
                   --stages 1:5 \
                   --reportallpairs TRUE \
                   --MACS_qvalue 0.05 --threads 50 \
		   --keepempty TRUE \
                   --shortreads FALSE \
                   --maxlength 1000
        done
}

#myMango_long_sra GSE103148
#myMango_long_sra GSE115252
#myMango_long_sra GSE68977
#myMango_long_sra GSE69643

myMango_long_sra_linker(){
        dir=$1
	linker1=$2
	linker2=$3
        fastq=`ls $dir/fastq |cut -f 1 -d '.'|sort|uniq`

        mango="Rscript /home/wang/software/mango/mango_multithreads_wang/mango_SRA.R"
        mkdir -p $dir/mango

        for i in $fastq
        do
                echo $i
                echo step1 unzip------
                #unpigz -p 40 -k $dir/fastq/${i}.pair_1.fastq.gz
                #unpigz -p 40 -k $dir/fastq/${i}.pair_2.fastq.gz

                echo step2 run mango------
                $mango --fastq1 $dir/fastq/${i}.pair_1.fastq \
                   --fastq2 $dir/fastq/${i}.pair_2.fastq \
                   --prefix     $dir/mango/$i \
                   --bowtieref $index \
                   --bedtoolsgenome $gt \
                   --chromexclude chrM,chrY \
                   --stages 1:5 \
                   --reportallpairs TRUE \
                   --MACS_qvalue 0.05 --threads 50 \
		   --linkerA $linker1 --linkerB $linker2 \
                   --keepempty TRUE \
                   --shortreads FALSE \
                   --maxlength 1000
        done
}

#myMango_long_sra_linker GSE69643 ACGCGATATCTTATCTGACT AGTCAGATAAGATATCGCGT
#myMango_long_sra_linker GSE68977 ACGCGATATCTTATCTGACT AGTCAGATAAGATATCGCGT
#myMango_long_sra_linker GSE103148 ACGCGATATCTTATCTGACT AGTCAGATAAGATATCGCGT
#myMango_long_sra_linker GSE115252 ACGCGATATCTTATCTGACT AGTCAGATAAGATATCGCGT


myMangoSpecial(){
        dir=$1
        fastq=`ls $dir/fastq |cut -f 1 -d '.'|sort|uniq |grep -v rep2`

        mango="Rscript /home/wang/software/mango/mango_multithreads_wang/mango_encode2.R"
        mkdir -p $dir/mango

        for i in $fastq
        do
                echo $i
                echo step1 unzip------
                #unpigz -p 20 -k $dir/fastq/${i}.pair_1.fastq.gz
                #unpigz -p 20 -k $dir/fastq/${i}.pair_2.fastq.gz
		cat $dir/fastq/${i}.pair_1.fastq | paste - - - -|sort -t : -k2 -k3 -k4 -k5 -k6 -k7 -n --parallel=40|tr "\t" "\n"> $dir/fastq/${i}_sort.pair_1.fastq
		cat $dir/fastq/${i}.pair_2.fastq | paste - - - -|sort -t : -k2 -k3 -k4 -k5 -k6 -k7 -n --parallel=40|tr "\t" "\n"> $dir/fastq/${i}_sort.pair_2.fastq

                echo step2 run mango------
                $mango --fastq1 $dir/fastq/${i}_sort.pair_1.fastq \
                   --fastq2 $dir/fastq/${i}_sort.pair_2.fastq \
                   --prefix     $dir/mango/$i \
                   --bowtieref $index \
                   --bedtoolsgenome $gt \
                   --chromexclude chrM,chrY \
                   --stages 1:5 \
                   --reportallpairs TRUE \
                   --MACS_qvalue 0.05 --threads 40
        done
}



#myMangoSpecial ENCSR000FDB  # 这个rep1是特殊的读数名


