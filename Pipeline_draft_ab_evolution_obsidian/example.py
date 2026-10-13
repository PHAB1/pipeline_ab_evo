from Bio import SeqIO
from Bio import Align

human = SeqIO.read("/home/pbarros/Trabalhos/pipeline_ab_evo/genome_assemble/dados_de_teste/hbb_human.fasta", "fasta")
horse = SeqIO.read("/home/pbarros/Trabalhos/pipeline_ab_evo/genome_assemble/dados_de_teste/hbb_horse.fasta", "fasta")

aln = Align.PairwiseAligner()
aln.mode = "global"

result = aln.align(human.seq, horse.seq)[0]
print(result)
print("score:", result.score)