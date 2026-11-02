"""Alinhamento múltiplo (MAFFT) + distâncias + árvore (Biopython).

Rode a partir de pipeline_ab_evo/exercicio/02_alinhamento/:
    python exemplos/msa_exemplo.py
"""
import subprocess
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

entrada = Path("dados/hemoglobina_beta.fasta")
saida_dir = Path("resultados/alinhamento")
fig_dir = Path("figuras")
saida_dir.mkdir(parents=True, exist_ok=True)
fig_dir.mkdir(parents=True, exist_ok=True)
alinhado = saida_dir / "hemoglobina_beta.aln.fasta"

# 1) MAFFT faz o alinhamento (Biopython só lê o resultado)
with open(alinhado, "w") as out:
    subprocess.run(["mafft", "--auto", "--quiet", str(entrada)], stdout=out, check=True)

msa = AlignIO.read(alinhado, "fasta")
print(f"=== alinhamento: {len(msa)} sequências, {msa.get_alignment_length()} colunas")
for rec in msa:
    print(f"{rec.id:<12} {rec.seq[:50]}...")

# 2) Distância = 1 - identidade
dm = DistanceCalculator("identity").get_distance(msa)
print("\n=== distâncias (0 = idênticas)")
print(dm)

# 3) Árvore Neighbor-Joining
arvore = DistanceTreeConstructor().nj(dm)
arvore.root_at_midpoint()
print("\n=== árvore")
Phylo.draw_ascii(arvore)

fig, ax = plt.subplots(figsize=(6, 4))
Phylo.draw(arvore, axes=ax, do_show=False)
fig.savefig(fig_dir / "hemoglobina_beta_arvore.png", dpi=150, bbox_inches="tight")
print(f"figura: {fig_dir / 'hemoglobina_beta_arvore.png'}")
