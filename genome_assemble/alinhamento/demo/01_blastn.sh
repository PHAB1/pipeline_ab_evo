#!/usr/bin/env bash
# Demonstração do BLAST no terminal.
# Rode a partir da pasta genome_assemble/, com o ambiente euk_align ativo:
#   conda activate euk_align
#   bash alinhamento/demo/01_blastn.sh
set -euo pipefail

mkdir -p results/blast

# makeblastdb: transforma um FASTA em banco de dados do BLAST (só precisa uma vez)
# -in: FASTA de entrada (aqui, os contigs da sua montagem)
# -dbtype nucl: banco de DNA (para proteína seria prot)
# -out: prefixo dos arquivos do banco
makeblastdb \
  -in results/assembly/SRR35893457_megahit/final.contigs.fa \
  -dbtype nucl \
  -out results/blast/contigs

# blastn: procura a sequência (query) dentro do banco (db)
# saída padrão: legível para humanos, com o alinhamento desenhado
blastn \
  -query alinhamento/demo/ade2.fasta \
  -db results/blast/contigs \
  -max_target_seqs 3 \
  -out results/blast/ade2_vs_contigs.txt

# -outfmt 6: saída em tabela (uma linha por hit), boa para automatizar
# colunas escolhidas: query, contig, % identidade, tamanho do alinhamento,
# cobertura da query, e-value e bitscore
blastn \
  -query alinhamento/demo/ade2.fasta \
  -db results/blast/contigs \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
  -evalue 1e-10

echo "Alinhamento completo em: results/blast/ade2_vs_contigs.txt"
