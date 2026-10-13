"""Busca referências de um gene-alvo no UniProt e filtra por similaridade com a semente.

Nomes de genes são ambíguos (ex.: "cdc2" também é sinônimo da POL3 de levedura),
então cada candidato precisa alinhar com a semente para entrar como referência.
"""

import csv
import re
import time
import urllib.parse
import urllib.request

from Bio import Align, SeqIO
from Bio.Align import substitution_matrices

UNIPROT = "https://rest.uniprot.org/uniprotkb"
FIELDS = "accession,gene_primary,organism_name,organism_id,reviewed,length,sequence"


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read().decode()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def fetch_seed(acc):
    lines = get(f"{UNIPROT}/{acc}.fasta").strip().splitlines()
    return "".join(lines[1:])


def search(names, taxon, exclude, reviewed, size=500):
    query = "(" + " OR ".join(f"gene_exact:{n}" for n in names) + ")"
    query += f" AND reviewed:{str(reviewed).lower()}"
    if taxon:
        query += f" AND taxonomy_id:{taxon}"
    for t in exclude:
        query += f" NOT taxonomy_id:{t}"
    url = f"{UNIPROT}/search?" + urllib.parse.urlencode(
        {"query": query, "format": "tsv", "fields": FIELDS, "size": size}
    )
    rows = list(csv.DictReader(get(url).splitlines(), delimiter="\t"))
    return rows


def make_aligner():
    al = Align.PairwiseAligner()
    al.mode = "local"
    al.substitution_matrix = substitution_matrices.load("BLOSUM62")
    al.open_gap_score = -11
    al.extend_gap_score = -1
    return al


def compare(al, seed, cand):
    """Identidade na região alinhada e fração da semente coberta."""
    aln = al.align(seed, cand)[0]
    matches = aligned = 0
    for (s0, s1), (c0, c1) in zip(*aln.aligned):
        matches += sum(a == b for a, b in zip(seed[s0:s1], cand[c0:c1]))
        aligned += s1 - s0
    ident = matches / aligned if aligned else 0.0
    return ident, aligned / len(seed)


def clean(text):
    return re.sub(r"[^A-Za-z0-9_]", "_", text)


def main(sm):
    gene = sm.wildcards.gene
    p = sm.params
    out_faa, out_tsv, out_seed = sm.output.faa, sm.output.tsv, sm.output.seed

    seed = fetch_seed(p.seed)
    with open(out_seed, "w") as fh:
        fh.write(f">{clean(p.seed)}-{gene}\n{seed}\n")

    if p.fasta:
        recs = list(SeqIO.parse(p.fasta, "fasta"))
        rows = [
            {"accession": r.id, "gene_primary": gene, "organism_name": r.description,
             "organism_id": r.id, "reviewed": "user", "sequence": str(r.seq)}
            for r in recs
        ]
    else:
        rows = search(p.names, p.taxon, p.exclude, reviewed=True)
        if len({r["organism_id"] for r in rows}) < p.min_per_gene:
            rows += search(p.names, p.taxon, p.exclude, reviewed=False)

    al = make_aligner()
    kept, seen_org, report = [], set(), []
    for r in rows:
        seq = r["sequence"].replace("*", "")
        ident, cov = compare(al, seed, seq)
        ratio = len(seq) / len(seed)
        if ident < p.min_identity:
            decision = "descartado: identidade baixa"
        elif cov < p.min_seed_coverage:
            decision = "descartado: cobertura baixa"
        elif ratio > 2:
            decision = "descartado: muito mais longo que a semente"
        elif r["organism_id"] in seen_org:
            decision = "descartado: espécie repetida"
        elif len(kept) >= p.max_per_gene:
            decision = "descartado: limite por gene"
        else:
            decision = "mantido"
            kept.append((r, seq))
            seen_org.add(r["organism_id"])
        report.append({
            "gene": gene, "accession": r["accession"], "nome": r["gene_primary"],
            "organismo": r["organism_name"], "revisado": r["reviewed"],
            "comprimento": len(seq), "identidade": round(ident, 3),
            "cobertura_semente": round(cov, 3), "decisao": decision,
        })

    fields = ["gene", "accession", "nome", "organismo", "revisado", "comprimento",
              "identidade", "cobertura_semente", "decisao"]
    with open(out_tsv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(report)

    if not kept:
        raise SystemExit(f"{gene}: nenhuma referência passou no filtro; veja {out_tsv}")

    with open(out_faa, "w") as fh:
        for r, seq in kept:
            fh.write(f">{clean(r['accession'])}-{gene}\n{seq}\n")


main(snakemake)  # noqa: F821
