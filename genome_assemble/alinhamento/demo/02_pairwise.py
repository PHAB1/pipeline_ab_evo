"""Alinhamento par a par: global (Needleman-Wunsch) vs local (Smith-Waterman).

Rode a partir da pasta genome_assemble/, com o ambiente euk_align ativo:
    python alinhamento/demo/02_pairwise.py
"""
from Bio import Align
from Bio.Align import substitution_matrices

# ------------------------------------------------------------------ DNA
# Duas sequências parecidas: a segunda tem uma troca e um pedaço a menos.
seq1 = "GATTACAGATTACACCGT"
seq2 = "GATCACAGATTACA"

aligner = Align.PairwiseAligner()
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -2
aligner.extend_gap_score = -0.5

for modo in ("global", "local"):
    aligner.mode = modo
    melhor = aligner.align(seq1, seq2)[0]
    print(f"=== DNA, alinhamento {modo} (score = {melhor.score})")
    print(melhor)

# ------------------------------------------------------------- proteína
# Para proteínas usamos uma matriz de substituição (BLOSUM62):
# trocas entre aminoácidos parecidos (ex.: I por L) custam pouco.
hb_humano = "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"
pedaco = "LVVYPWTQRFFESFGDL"  # um trecho do meio da hemoglobina

prot = Align.PairwiseAligner()
prot.substitution_matrix = substitution_matrices.load("BLOSUM62")
prot.open_gap_score = -10
prot.extend_gap_score = -0.5

for modo in ("global", "local"):
    prot.mode = modo
    melhor = prot.align(hb_humano, pedaco)[0]
    contagem = melhor.counts()
    print(f"=== proteína, alinhamento {modo} (score = {melhor.score})")
    print(f"identidades={contagem.identities} trocas={contagem.mismatches} gaps={contagem.gaps}")
    print(melhor)
