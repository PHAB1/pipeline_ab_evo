"""Fase 2: A mensagem secreta.

Alguém escondeu uma palavra dentro da actina: trocou alguns aminoácidos
pelas letras da mensagem. Só que também apagou um aminoácido para atrapalhar.

Rode a partir da pasta genome_assemble/, com o ambiente euk_align ativo:
    python alinhamento/exercicio/scripts/fase2_mensagem_secreta.py
"""
from Bio import SeqIO
from Bio.Align import PairwiseAligner, substitution_matrices

DADOS = "alinhamento/exercicio/dados"
original = str(SeqIO.read(f"{DADOS}/actina_original.fasta", "fasta").seq)
mutante = str(SeqIO.read(f"{DADOS}/actina_misteriosa.fasta", "fasta").seq)
fragmento = str(SeqIO.read(f"{DADOS}/fragmento.fasta", "fasta").seq)

print("comprimentos:", len(original), len(mutante))

# ------------------------------------------------ Parte A: jeito ingênuo
# Compara letra por letra, na mesma posição. Parece lógico... funciona?
ingenua = "".join(b for a, b in zip(original, mutante) if a != b)
print(f"comparação ingênua: {len(ingenua)} diferenças -> {ingenua[:40]}...")

# ------------------------------------------------ Parte B: alinhamento
aligner = PairwiseAligner()
# TODO 3: configure o aligner para alinhamento GLOBAL de proteína:
#   modo global, matriz BLOSUM62, gap open -10, gap extend -0.5
#   (veja alinhamento/demo/02_pairwise.py)

aln = aligner.align(original, mutante)[0]
print(aln)

# aln[0] e aln[1] são as duas linhas do alinhamento, já com os "-" dos gaps.
linha_orig, linha_mut = aln[0], aln[1]
mensagem = ""
# TODO 4: percorra as duas linhas juntas (dica: zip) e, sempre que as letras
# forem diferentes E nenhuma delas for "-", adicione a letra do mutante em `mensagem`.
# Bônus: imprima também a posição de cada troca na actina original.

print("mensagem:", mensagem)

# ------------------------------------------------ Parte C: global vs local
# fragmento.fasta é um pedaço de 40 aminoácidos da actina original.
# TODO 5: alinhe original x fragmento nos modos "global" e "local".
# Para cada modo, imprima o score e onde o fragmento caiu na actina.
# Dica: aln.aligned[0] lista os blocos alinhados na 1ª sequência como (início, fim);
# início do primeiro bloco = aln.aligned[0][0][0], fim do último = aln.aligned[0][-1][1]
# (posições começam em 0, como sempre em Python).
