"""Junta as referências dos alvos e os genes-controle do BUSCO num arquivo de alvos do HybPiper.

Cabeçalho exigido pelo HybPiper: >Taxon-Gene (o gene é o que vem depois do último hífen).
Controles parecidos com algum alvo são descartados: o HybPiper distribui cada read para
o gene mais parecido, e dois genes homólogos disputariam as mesmas reads.
"""

import random
from collections import defaultdict

from Bio import Align, SeqIO
from Bio.Align import substitution_matrices


def make_aligner():
    al = Align.PairwiseAligner()
    al.mode = "local"
    al.substitution_matrix = substitution_matrices.load("BLOSUM62")
    al.open_gap_score = -11
    al.extend_gap_score = -1
    return al


def similar(al, a, b, min_score_per_res):
    """Score local normalizado pelo tamanho da menor sequência."""
    return al.score(a, b) / min(len(a), len(b)) >= min_score_per_res


def main(sm):
    p = sm.params
    rng = random.Random(p.random_seed)

    variants = defaultdict(list)
    for rec in SeqIO.parse(sm.input.busco, "fasta"):
        busco_id, n = rec.id.rsplit("_", 1)
        variants[busco_id].append((n, str(rec.seq)))

    seeds = [str(r.seq) for f in sm.input.seeds for r in SeqIO.parse(f, "fasta")]
    al = make_aligner()

    ids = sorted(variants)
    rng.shuffle(ids)
    controls, dropped = [], []
    for busco_id in ids:
        if len(controls) >= p.n_genes:
            break
        anc = variants[busco_id][0][1]
        if any(similar(al, anc, s, p.max_score_per_res) for s in seeds):
            dropped.append(busco_id)
            continue
        controls.append(busco_id)

    with open(sm.output.targets, "w") as out, open(sm.output.roles, "w") as roles:
        roles.write("gene\tpapel\n")
        for f, gene in zip(sm.input.refs, p.genes):
            for rec in SeqIO.parse(f, "fasta"):
                out.write(f">{rec.id}\n{rec.seq}\n")
            roles.write(f"{gene}\talvo\n")
        for busco_id in controls:
            for n, seq in variants[busco_id][: p.variants_per_gene]:
                out.write(f">var{n}-{busco_id}\n{seq}\n")
            roles.write(f"{busco_id}\tcontrole\n")
        for busco_id in dropped:
            roles.write(f"{busco_id}\tcontrole_descartado_parecido_com_alvo\n")


main(snakemake)  # noqa: F821
