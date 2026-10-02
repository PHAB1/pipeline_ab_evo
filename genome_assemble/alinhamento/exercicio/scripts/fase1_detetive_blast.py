"""Fase 1: Detetive do BLAST.

Roda o blastn de cada sequência misteriosa contra os SEUS contigs e monta
uma tabela com o melhor hit + o multi (cobertura) do contig.

Rode a partir da pasta genome_assemble/, com o ambiente euk_align ativo:
    python alinhamento/exercicio/scripts/fase1_detetive_blast.py megablast
    python alinhamento/exercicio/scripts/fase1_detetive_blast.py blastn
"""
import subprocess
import sys

from Bio import SeqIO

CONTIGS = "results/assembly/SRR35893457_megahit/final.contigs.fa"
DB = "results/blast/contigs"
MISTERIOS = "alinhamento/exercicio/dados/misterios.fasta"


def ler_multi(caminho):
    """Devolve um dicionário {contig: (multi, len)} a partir dos cabeçalhos do MEGAHIT.

    Exemplo de cabeçalho:  >k141_1020 flag=1 multi=62.0000 len=87622
    No Biopython:  rec.id          -> 'k141_1020'
                   rec.description -> 'k141_1020 flag=1 multi=62.0000 len=87622'
    """
    info = {}
    for rec in SeqIO.parse(caminho, "fasta"):
        # TODO 1: quebre rec.description em pedaços (dica: .split()),
        # pegue os valores de multi e len e guarde em info[rec.id] = (multi, len)
        # (multi como float, len como int)
        pass
    return info


def melhor_hit(seq_id, seq, task):
    """Roda o blastn de UMA sequência e devolve o melhor hit (ou None se não achar nada)."""
    cmd = [
        "blastn",
        "-task", task,
        "-db", DB,
        "-query", "-",  # "-" = a sequência vem pelo input, não de um arquivo
        "-outfmt", "6 sseqid pident length qcovs evalue bitscore",
        "-evalue", "1e-5",
        "-max_target_seqs", "5",
    ]
    res = subprocess.run(cmd, input=f">{seq_id}\n{seq}\n",
                         capture_output=True, text=True, check=True)

    # res.stdout é um texto com uma linha por hit e colunas separadas por TAB:
    # sseqid  pident  length  qcovs  evalue  bitscore
    # TODO 2: transforme res.stdout em uma lista de listas
    # (dica: .strip().splitlines() e depois .split("\t") em cada linha).
    # Se a lista estiver vazia, devolva None.
    # Senão, devolva a linha com MAIOR bitscore (última coluna; lembre de converter para float).
    return None


task = sys.argv[1] if len(sys.argv) > 1 else "megablast"
multi = ler_multi(CONTIGS)
if not multi:
    sys.exit("ler_multi() devolveu um dicionário vazio: complete o TODO 1.")

print(f"task = {task}")
print("misterio\tcontig\tpident\tqcovs\tevalue\tmulti\tlen_contig")
for rec in SeqIO.parse(MISTERIOS, "fasta"):
    hit = melhor_hit(rec.id, str(rec.seq), task)
    if hit is None:
        print(f"{rec.id}\tsem_hit")
        continue
    contig, pident, _, qcovs, evalue, _ = hit
    m, tamanho = multi[contig]
    print(f"{rec.id}\t{contig}\t{pident}\t{qcovs}\t{evalue}\t{m:.0f}\t{tamanho}")
