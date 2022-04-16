#Use double-evidence in the final version
python overlap.py
sed 's/+/\t/g'  triple-evidenced.pair > triple-evidenced.pair.tsv

python eachgene.py

cut -f 9- /work3/WANG_cohesinDB/Curated/annotation_real/targetgene/DEGs/allgene.DEG.info > DEG.info 
cut -f 9-12 /work3/WANG_cohesinDB/Curated/annotation_real/targetgene/correlation/allgene.corr.info > Correlation.info

paste /work3/WANG_cohesinDB/Curated/annotation_real/targetgene/loop/whetherLoop.tsv \
	/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/loop/interactionDFsumUniq.tsv \
	/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/loop/studyDFsumUniq.tsv \
	/work3/WANG_cohesinDB/Curated/annotation_real/targetgene/loop/subunitDFsumUniq.tsv > Interaction.info

paste GeneTripleCohesin.tsv Interaction.info DEG.info Correlation.info |\
	sed '1iID\tSymbol\tChrom\tStart\tEnd\tStrand\tGeneType\tTriple-Whether\tTriple-RegulatoryCohesin\tInteraction-Whether\tInteraction-Type\tInteraction-Study\tInteraction-Subunit\tDEG-Whether\tDEG-NunmerOfStudy\tDEG-Study\tDEG-Subunit\tCorraltion-Whether\tCorrelation-Rho\tCorrelation-FDR\tCorrelation-Subunit'> allgene.final 




