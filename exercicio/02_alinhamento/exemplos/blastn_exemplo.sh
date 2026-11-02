#!/usr/bin/env bash
# Exemplo: blastn do gene ADE2 contra os contigs.
# Rode a partir de pipeline_ab_evo/exercicio/02_alinhamento/:
#   bash exemplos/blastn_exemplo.sh
set -euo pipefail

mkdir -p resultados/blast

makeblastdb \
  -in dados/contigs.fasta \
  -dbtype nucl \
  -out resultados/blast/contigs

blastn \
  -query exemplos/ade2.fasta \
  -db resultados/blast/contigs \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
  -evalue 1e-5 \
  -out resultados/blast/ade2_exemplo.tsv

echo "Resultado: resultados/blast/ade2_exemplo.tsv"
cat resultados/blast/ade2_exemplo.tsv
