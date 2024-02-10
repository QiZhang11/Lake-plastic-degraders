import os
import sys


def run1():
    f=open(file3)
    lines=f.readlines()
    f.close()
    salmon_dict={}
    sample_dict={}
    for line in lines[1:]:
        
        data = line.strip().split('\t')
        if data[0]=='*':
            continue
        contig_id=data[0]
        contig_len=float(data[1])
        reads_n=float(data[2])
        rpkm = reads_n*1000000/float(total_reads)*1000/contig_len
        salmon_dict[contig_id] = rpkm
        gene = contig_id.split("~")[0]
        if gene not in sample_dict:
            sample_dict[gene] = []
        sample_dict[gene].append(contig_id)

    w=open(outfile,'w+')
    w.write("Sample\tGene\tRPKM\n")
    for tax,contig_id_list in sample_dict.items():
        rpkm1=0
        for contig_id in contig_id_list:
            if contig_id in salmon_dict:
                rpkm1+=salmon_dict[contig_id]
        w.write('\t'.join([sample,tax,str(rpkm1)])+'\n')
    w.close()

file3=sys.argv[1]
outfile=sys.argv[2] 
total_reads=float(sys.argv[3])

sample=os.path.basename(outfile).split(".")[0]

"""
f=open(file3)
lines=f.readlines()
f.close()
salmon_dict={}
sample_dict={}
for line in lines[1:]:
    
    data = line.strip().split('\t')
    if data[0]=='*':
        continue
    contig_id=data[0]
    contig_len=float(data[1])
    reads_n=float(data[2])
    rpkm = reads_n*1000000/float(total_reads)*1000/contig_len
    salmon_dict[contig_id] = rpkm
    gene = contig_id.split("~")[0]
    if gene not in sample_dict:
        sample_dict[gene] = []
    sample_dict[gene].append(contig_id)

w=open(outfile,'w+')
w.write("Sample\tGene\tRPKM\n")
for tax,contig_id_list in sample_dict.items():
    rpkm1=0
    for contig_id in contig_id_list:
        if contig_id in salmon_dict:
            rpkm1+=salmon_dict[contig_id]
    w.write('\t'.join([sample,tax,str(rpkm1)])+'\n')
w.close()

sys.exit()
"""
f=open(file3)
lines=f.readlines()
f.close()

w=open(outfile,'w+')
w.write("Sample\tContig_ID\tStart\tEnd\tGene\tRPKM\n")
for line in lines[1:]:
    data = line.strip().split('\t')
    if data[0]=='*':
        continue
    contig_id=data[0].split("~")[1]
    start=data[0].split("~")[2]
    end=data[0].split("~")[3]
    gene=data[0].split("~")[0]
    contig_len=float(data[1])
    reads_n=float(data[2])
    if reads_n>0:
        rpkm = reads_n*1000000/float(total_reads)*1000/contig_len
        w.write('\t'.join([sample,contig_id,start,end,gene,str(rpkm)])+'\n')
w.close()
