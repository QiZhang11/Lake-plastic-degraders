############HMMs annotation of metagenomes
#step1 Remove the redundant protein by CD-hit
cd-hit -i data.fa -o cd-data.fa -c 0.95 -aL 0.95 -aS 0.95 -d 0 

#step2 Diamond blastp
diamond makedb --in cd-data2.fa --db cd-data.fa.dmnd
diamond blastp --max-target-seqs 1 -p 4 -q uniprot.fa -d cd-data.prt.fa.dmnd -f 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore slen -o diamond.out --query-cover 60 --id 60 --evalue 1e-10

#step3 Extract the rows in the 60%-90% range of ident and the corresponding id (qseqid) to the new file
python3 get_hit_id.py
python get_seqs_by_id.py -f uniprot.fa -i id.txt -o hit.fasta
cd-hit -i hit.fasta -o cd-hit.fa -c 0.95 -aL 0.95 -aS 0.95 -d 0 

#step4 Multiple sequence alignment
mafft --auto  cd-hit.fa> mafft-pident7.fa

#step5 hmm model construction
hmmbuild ser90.hmm  mafft-pident7.fa

#step6 hmmsearch and calculate abundance in contigs
python mps_hmmsearch.py MAG_nucl.fa MAG_protein.fa ser90.hmm output_dir
python generate_hmmsearch_rpkm_scripts.py input.list map output_dir stat > run.sh
bash run.sh

############Metagenome assemblies and reconstruction of LPDMAGs
## Assembly
megahit -t 10 -m 0.5 --min-contig-len 500 --k-step 10 --k-min 27 \
-1 /02.paired_data/$sampleid_paired_1.clean.fastq.gz \\
-2 /02.paired_data/$sampleid_paired_2.clean.fastq.gz \
-o /assembly/$sampleid

# Binning
metawrap binning  -t 28 -m 1000 -l 1500 \
-o /binning/$sampleid_binning \
 -a /assembly/$sampleid.fa 
 --metabat2 --maxbin2 --concoct \
 /02.paired_data/$sampleid_*.fastq
 
 # refine
metawrap bin_refinement  \
-o /refine/$sampleid_refine \
 -t 10 \
 -A concoct_bins/ -B metabat2_bins/ -C maxbin2_bins/ \
 -c 50 -x 10 \

# dereplication LPDMAGs
dRep dereplicate drep_out -g 4856fna/*.fa --S_algorithm fastANI --clusterAlg centroid -sa 0.95 -nc 0.10 -cm larger -p 24

##checkm
checkm lineage_wf -t 200 -x fa -f checkm.qa.txt checkm_out/

# tRNA & rRNA identification
##  trna
for bacteria: for i in ${ID[@]};do tRNAscan-SE -B -Q -o /trna/${i}trna.out /bac_mag/${i}.fa;done
for archae: for i in ${ID[@]};do tRNAscan-SE -A -Q -o /trna/${i}trna.out /arc_mag/${i}.fa;done

##  rrna
for bacteria: for i in ${ID[@]};do barrnap --quiet -k bac /bac_mag/${i}.fa --outseq /rrna_hit/${i}hit.fa > /rrna_out/${i}rrna.out;done
for archae: for i in ${ID[@]};do barrnap --quiet -k arc /arc_mag/${i}.fa --outseq /rrna_hit/${i}hit.fa > /rrna_out/${i}rrna.out;done

# Phylogenetic analyse
phylophlan -i 4856faa -d phylophlan --diversity high --accurate --min_num_markers 100 -f /home/user/phylophlan.cfg -o phylophlan --nproc 40 --verbose 2>&1 | tee tree.log