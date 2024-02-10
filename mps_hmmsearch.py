import os
import sys
import re
from Bio import SeqIO


def get_nucl_seq(name,start,end):
    ref_name,ref_start,ref_end = pos_dict[name]
    prot_len=end-start+1
    nucl_seq = seqs[ref_name]
    nucl_start=ref_start+start*3-2-1
    nucl_end=nucl_start+prot_len*3-1
    s=nucl_start-1
    e=nucl_end
    return nucl_seq[s:e],str(nucl_start),str(nucl_end)

nucl_file = sys.argv[1]
protein_file = sys.argv[2]
db = sys.argv[3]
outdir = sys.argv[4]
if not os.path.exists(outdir):
    os.makedirs(outdir)
cmd = f"hmmsearch --cpu 10 -E 1e-5 --domtblout {outdir}/hmmsearch.out {db} {protein_file}"
if not os.path.exists(f"{outdir}/hmmsearch.out"):
    os.system(cmd)

outfile = os.path.join(outdir,"map.fasta")
seqs = {}
for rec in SeqIO.parse(nucl_file,'fasta'):
    seqs[rec.id] = str(rec.seq)
pos_dict = {}
for rec in SeqIO.parse(protein_file,'fasta'):
    desc = rec.description
    data = desc.split("#")
    protein_id=data[0].strip()
    name = "_".join(data[0].split("_")[:-1])
    start=int(data[1].strip())
    end=int(data[2].strip())
    pos_dict[protein_id] = [name,start,end]

f=open(outdir+"/hmmsearch.out")
lines=f.readlines()
f.close()
w=open(outfile,'w+')
tmp1={}
for line in lines:
    if line.startswith("#"):
        continue
    if not line.strip():
        continue
    data = re.split(" +",line.strip())
    #print(data)
    name=data[0]
    gene=data[3]
    start=int(data[19])
    end=int(data[20].split(' ')[0])
    #print(start,end)
    contig_name='_'.join(name.split("_")[:-1])
    nucl_seq,nucl_start,nucl_end = get_nucl_seq(name,start,end)
    name11=contig_name+'~'+nucl_start+'~'+nucl_end
    if name11 not in tmp1:
        tmp1[name11]="'"
        w.write(">"+gene+'~'+contig_name+'~'+nucl_start+'~'+nucl_end+'\n'+nucl_seq+'\n')
    #break
w.close()
