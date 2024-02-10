# coding:utf-8

import click

from Bio import SeqIO


@click.command()
@click.option('-f', '--fastafile', help='Input a fasta file', required=True)
@click.option('-i', '--idfile', help='Input an idlist', required=True)
@click.option('-o', '--outfile', help='Input the name of result file', default='result_out.fa')
def main(fastafile="FA.fa", idfile="ID.txt", outfile="result_out.fa"):
    with open(idfile) as id_handle:
        wanted = set(line.rstrip("\n").split(None, 1)[0] for line in id_handle)

    print("Found %i unique identifiers in %s" % (len(wanted), idfile))

    records = (r for r in SeqIO.parse(fastafile, "fasta") if r.id in wanted)

    count = SeqIO.write(records, outfile, "fasta")

    print("Saved %i records from %s to %s" % (count, fastafile, outfile))

    if count < len(wanted):
        print("Warning %i IDs not found in %s" % (len(wanted) - count, fastafile))


if __name__ == '__main__':
    main()

