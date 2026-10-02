"""Alinhamento múltiplo (MAFFT) + matriz de identidade + árvore (Biopython).

Rode a partir da pasta genome_assemble/, com o ambiente euk_align ativo:
    python alinhamento/demo/03_msa_arvore.py
"""
import subprocess
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

entrada = Path("alinhamento/demo/hemoglobina_beta.fasta")
saida_dir = Path("results/alinhamento")
saida_dir.mkdir(parents=True, exist_ok=True)
alinhado = saida_dir / "hemoglobina_beta.aln.fasta"

# 1. MAFFT faz o alinhamento múltiplo (o Biopython só lê o resultado)
with open(alinhado, "w") as out:
    subprocess.run(["mafft", "--auto", "--quiet", str(entrada)], stdout=out, check=True)

msa = AlignIO.read(alinhado, "fasta")
print(f"=== alinhamento múltiplo: {len(msa)} sequências, {msa.get_alignment_length()} colunas")
for rec in msa:
    print(f"{rec.id:<12} {rec.seq[:60]}")

# 2. Distância = 1 - identidade (proporção de posições diferentes)
dm = DistanceCalculator("identity").get_distance(msa)
print("\n=== distâncias (0 = idênticas)")
print(dm)

# 3. Árvore por Neighbor-Joining a partir das distâncias
arvore = DistanceTreeConstructor().nj(dm)
arvore.root_at_midpoint()
print("\n=== árvore")
Phylo.draw_ascii(arvore)

fig, ax = plt.subplots(figsize=(6, 4))
Phylo.draw(arvore, axes=ax, do_show=False)
fig.savefig(saida_dir / "hemoglobina_beta_arvore.png", dpi=150, bbox_inches="tight")
print(f"figura: {saida_dir / 'hemoglobina_beta_arvore.png'}")
