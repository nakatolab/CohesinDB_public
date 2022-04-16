#!/bin/bash
cmdname=`basename $0`
function usage()
{
    echo "$cmdname" '[-d bamdir] [-p "bowtie2 param"] <fastq> <prefix> <build> <single|pair>' 1>&2
}

echo $cmdname $*

type=hiseq
bamdir=cram
db=UCSC
param=""
while getopts d:p: option
do
    case ${option} in
	d)
	    bamdir=${OPTARG}
	    ;;
        p)
            param=${OPTARG}
            ;;
	*)
	    usage
	    exit 1
	    ;;
    esac
done
shift $((OPTIND - 1))

if [ $# -ne 4 ]; then
  usage
  exit 1
fi

fastq=$1
prefix=$2
build=$3
singlepair=$4
post="-bowtie2"`echo $param | tr -d ' '`

if test ! -e $bamdir; then mkdir $bamdir; fi
if test ! -e log; then mkdir log; fi

Ddir=`database.sh`
#bowtie2="singularity exec --bind /work /work/SingularityImages/rnakato_bowtie2.img bowtie2"
bowtie2="bowtie2"

file=$bamdir/$prefix$post-$build.sort.bam
#file=$bamdir/$prefix$post-$build.sort.cram

if test -e "$file" && test 1000 -lt `wc -c < $file` ; then
    echo "$file already exist. quit"
    exit 0
fi

ex_hiseq(){
    if test $build = "scer"; then
	index=$Ddir/bowtie2-indexes/S_cerevisiae
    elif test $build = "pombe"; then
	index=$Ddir/bowtie2-indexes/S_pombe
    else
	index=$Ddir/bowtie2-indexes/$db-$build
    fi
    genome=$index.fa

    $bowtie2 --version
    if [ "$singlepair" == "pair" ]
    then
	fastq1=`echo $fastq |sed 's/.fastq.gz/_1.fastq.gz/g'`
	fastq2=`echo $fastq |sed 's/.fastq.gz/_2.fastq.gz/g'`
	echo $fastq1
	echo $fastq2
    	command="$bowtie2 $param -p64 -x $index -1 $fastq1 -2 $fastq2 | samtools view -C - -T $genome -@ 64 | samtools sort -O bam -@ 64 > $file"
    elif [ "$singlepair" == "single" ]
    then
	echo $fastq
	command="$bowtie2 $param -p64 -x $index $fastq | samtools view -C - -T $genome -@ 64 | samtools sort -O bam -@ 64 > $file"
    fi
    echo $command
    eval $command

    if test ! -e $file.crai; then samtools index $file; fi
}

log=log/bowtie2-$prefix$post-$build
ex_hiseq >& $log
