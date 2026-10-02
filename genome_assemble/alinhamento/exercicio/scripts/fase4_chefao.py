"""Fase 4 (chefão): o contig estranho.

Compara um contig inteiro com o genoma de referência (S288C) e desenha a
% de identidade ao longo do contig. Se o contig fosse "normal", seria uma
linha reta lá em cima...

Antes, crie o banco BLAST da referência (uma vez só):
    makeblastdb -in data/reference/S288C.fa -dbtype nucl -out results/blast/s288c

Rode a partir da pasta genome_assemble/, com o ambiente euk_align ativo:
    python alinhamento/exercicio/scripts/fase4_chefao.py NOME_DO_CONTIG
"""
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Bio import SeqIO

CONTIGS = "results/assembly/SRR35893457_megahit/final.contigs.fa"
DB_REF = "results/blast/s288c"
contig_id = sys.argv[1]

# TODO 10: pegue o contig `contig_id` de dentro do CONTIGS
# (dica: percorra SeqIO.parse e guarde o registro cujo rec.id seja igual a contig_id)
contig = None

cmd = ["blastn", "-task", "blastn", "-db", DB_REF, "-query", "-",
       "-outfmt", "6 qstart qend sseqid sstart send pident length bitscore",
       "-evalue", "1e-20"]
res = subprocess.run(cmd, input=f">{contig.id}\n{contig.seq}\n",
                     capture_output=True, text=True, check=True)
hits = [linha.split("\t") for linha in res.stdout.strip().splitlines()]

# O contig pode ter hits em vários cromossomos (genes parecidos espalhados).
# Ficamos com o cromossomo que soma o maior bitscore: é de lá que o contig veio.
total = defaultdict(float)
for h in hits:
    total[h[2]] += float(h[7])
cromossomo = max(total, key=total.get)

# TODO 11: monte a lista `blocos` com (qstart, qend, sstart, send, pident)
# só dos hits nesse cromossomo e com length >= 300; ordene por qstart.
# Lembre de converter os números (int para posições, float para pident).
blocos = []

print(f"{contig_id} ({len(contig)} pb) cai em {cromossomo}")
for qs, qe, ss, se, pid in blocos:
    print(f"  contig {qs:>6}-{qe:<6} -> referência {ss}-{se}  {pid:.1f}%")

# TODO 12: desenhe cada bloco como um traço horizontal na altura da sua % de identidade
# (dica: ax.hlines(pid, qs, qe, linewidth=6)) e salve em results/alinhamento/chefao.png
fig, ax = plt.subplots(figsize=(9, 3))
ax.set_xlabel(f"posição no {contig_id} (pb)")
ax.set_ylabel("% identidade com S288C")
ax.set_ylim(60, 101)
Path("results/alinhamento").mkdir(parents=True, exist_ok=True)
