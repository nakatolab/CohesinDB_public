#scp -r oldjuicer  support@130.69.200.133:/mnt/NAS/WangDB/CohesinDB_processed_Post2021Dec
#scp -r newjuicer support@130.69.200.133:/mnt/NAS/WangDB/CohesinDB_processed_Post2021Dec

loopdir=/work3/WANG_cohesinDB/Post2021Dec10/Curated/HiC/hiclink/loops
for i in `ls $loopdir | grep -v call_loop.sh`
do
	ls $loopdir/$i/merged_loops.bedpe
	cp $loopdir/$i/merged_loops.bedpe processed/$i.loop
done

taddir=/work3/WANG_cohesinDB/Post2021Dec10/Curated/HiC/hiclink/TAD
for i in `ls $taddir | grep -v call_TAD.sh`
do
	wc -l  $taddir/$i/25000_blocks.bedpe
	cp $taddir/$i/25000_blocks.bedpe processed/$i.tad
done

scp -r processed/HiC_ENCSR637QCS_HCT116_MboI_Rad21-Auxin_NT_rep0.loop support@130.69.200.133:/mnt/NAS/WangDB/CohesinDB_processed_Post2021Dec/
scp -r processed/HiC_ENCSR637QCS_HCT116_MboI_Rad21-Auxin_NT_rep0.tad support@130.69.200.133:/mnt/NAS/WangDB/CohesinDB_processed_Post2021Dec/

scp /work3/WANG_cohesinDB/Post2021Dec10/Curated/HiC/hiclink/newjuicer/HiC_ENCSR637QCS_HCT116_MboI_Rad21-Auxin_NT_rep0.hic support@130.69.200.133:/mnt/NAS/WangDB/CohesinDB_processed_Post2021Dec/  

