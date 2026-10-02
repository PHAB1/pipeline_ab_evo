"""Fase 3: Quem é quem?

Nove organismos, nove sequências de citocromo c, nomes trocados por letras
(Organismo_A ... Organismo_I). Use alinhamento múltiplo + distâncias + árvore
para descobrir quem é quem.

Rode a partir da pasta genome_assemble/, com o ambiente euk_align ativo:
    python alinhamento/exercicio/scripts/fase3_quem_e_quem.py
"""
import subprocess
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

entrada = Path("alinhamento/exercicio/dados/citocromo_c.fasta")
saida_dir = Path("results/alinhamento")
saida_dir.mkdir(parents=True, exist_ok=True)
alinhado = saida_dir / "citocromo_c.aln.fasta"

# TODO 6: rode o MAFFT em `entrada` e grave o resultado em `alinhado`
# (copie e adapte do alinhamento/demo/03_msa_arvore.py)

msa = AlignIO.read(alinhado, "fasta")
print(f"{len(msa)} sequências, {msa.get_alignment_length()} colunas")
for rec in msa:
    print(f"{rec.id:<12} {rec.seq}")

dm = DistanceCalculator("identity").get_distance(msa)
print(dm)

nomes = dm.names
# dm[a, b] = distância entre os organismos a e b (0 = idênticos)
# TODO 7: monte uma lista com (distância, a, b) para TODOS os pares (sem repetir),
# ordene e imprima os 3 pares mais parecidos e o par mais distante.

# TODO 8: para cada organismo, calcule a distância MÉDIA até todos os outros.
# Quem fica longe de todo mundo?

# TODO 9: construa a árvore Neighbor-Joining, enraíze no ponto médio,
# desenhe com draw_ascii e salve a figura em results/alinhamento/citocromo_c_arvore.png
# (de novo, o demo 03 tem tudo)

# BÔNUS: quais colunas do alinhamento são IGUAIS nos 9 organismos?
# Dica: msa[:, i] devolve a coluna i como texto; set() remove repetidos.
# Imprima uma linha com a letra nas colunas conservadas e "." nas outras.
