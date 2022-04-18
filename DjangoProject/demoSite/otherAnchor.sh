infile=$1 ## col 1-6 loop, col 7 study, col 8-10 peak, row1 Name
outfile=$2

sed '1d' $infile | awk '$5<=$10 && $6>=$9'  | cut -f 1-3,8-10 > $outfile
sed '1d' $infile | awk '$2<=$10 && $3>=$9' | cut -f 4-6,8-10 >> $outfile
sed -i '1iConnected-chr\tConnected-start\tConnected-end\tInputRegion-chr\tInputRegion-start\tInputRegion-end' $outfile
