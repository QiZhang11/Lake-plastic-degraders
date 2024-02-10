import os
import sys


abun_input=os.path.abspath(sys.argv[1])#Contig/abundance/input.list
abun_outdir=os.path.abspath(sys.argv[2])#Contig/abundance/map
outdir=os.path.abspath(sys.argv[3])
suffix=sys.argv[4] #contigs.fa.stat
if not os.path.exists(outdir):
	os.makedirs(outdir)
d={}
f=open(abun_input)
lines=f.readlines()
f.close()
for line in lines:
	data =line.strip().split('\t')
	sample=data[0]
	total_reads=data[2]
	cmd=f'python cal_hmmsearch_rpkm.py {abun_outdir}/{sample}.{suffix} {outdir}/{sample} {total_reads}'
	print(cmd)

