# Tutorial: montagem de genoma (Illumina), passo a passo

Abra este arquivo **no GitHub** (no navegador) para ver o texto formatado. Os comandos você cola no terminal.

Organismo: *Saccharomyces cerevisiae* (levedura, ~12 Mb).  
Amostra: **SRR35893457** (Illumina paired-end, WGS).

Objetivo: baixar dados do SRA → QC → trim → montagem → avaliação → (opcional) alinhar na referência e abrir no IGV.

Todos os comandos abaixo são **na pasta do projeto** (a pasta em que você entrou depois do `git clone`). Confira:

```bash
ls
```

Deve aparecer `README.md`, `docs/` e `envs/`. Se não aparecer, entre na pasta do repositório com `cd`.

---

## 0. O que você vai usar

| Etapa | Ambiente conda | Ferramentas |
|-------|----------------|-------------|
| Download + QC + trim | `euk_preprocess` | `prefetch`, `fasterq-dump`, `fastqc`, `multiqc`, `fastp`, `seqkit` |
| Montagem + métricas | `euk_assemble` | `megahit`, `quast.py`, `seqkit` |
| Alinhamento (IGV) | `euk_assemble` | `bwa`, `minimap2`, `samtools` |

São **dois** ambientes para evitar conflito entre programas.

Neste tutorial usamos **1 thread** (`-t 1`, `-e 1`, `--thread 1`). É suficiente para esta amostra. Se o PC tiver vários núcleos e você quiser acelerar, pode subir esse número (ex.: `-t 8`).

---

## 1. Conferir os ambientes

Se ainda não criou os ambientes, veja [SETUP.md](SETUP.md) no GitHub.

```bash
# entra no ambiente de pré-processamento
conda activate euk_preprocess

# confere se as ferramentas estão instaladas
fasterq-dump --version
fastp --version
fastqc --version

# troca para o ambiente de montagem
conda activate euk_assemble
megahit --version
quast.py --version
which bwa
minimap2 --version
samtools --version
```

Se `bwa` / `minimap2` / `samtools` não aparecerem, atualize o ambiente (só precisa fazer uma vez):

```bash
conda env update -f envs/assemble.yml
```

---

## 2. Git no dia a dia

No começo da sessão, atualize o repositório:

```bash
git pull    # baixa commits novos do GitHub
git status  # mostra o que mudou na sua pasta
```

Depois de cada etapa:

```bash
git add -A                                      # separa as mudanças para o commit
git commit -m "terminei o download do SRA"      # grava um ponto na história (-m = mensagem)
git push                                        # envia o commit para o GitHub
```

Troque a mensagem do `-m` pelo que você acabou de fazer. FASTQ, `.sra` e pastas grandes de resultado **não** entram no git (já estão no `.gitignore`). Se aparecer `nothing to commit`, é isso mesmo — siga para a próxima etapa.

---

## 3. Baixar a amostra do SRA

```bash
conda activate euk_preprocess

# -p: cria as pastas se ainda não existirem
mkdir -p data/sra data/raw

# prefetch: baixa o arquivo SRA do NCBI
# -O: pasta de saída
prefetch SRR35893457 -O data/sra

# fasterq-dump: converte o SRA em FASTQ
# -O: pasta de saída
# -e 1: 1 thread
# --split-files: gera R1 (_1) e R2 (_2) separados
fasterq-dump data/sra/SRR35893457 -O data/raw -e 1 --split-files

# pigz: compacta os FASTQ (como gzip, para ocupar menos espaço)
# -p 1: 1 thread
pigz -p 1 data/raw/SRR35893457_1.fastq data/raw/SRR35893457_2.fastq

# ls: lista os arquivos; -lh = tamanho legível
ls -lh data/raw/
```

Esperado: `SRR35893457_1.fastq.gz` e `SRR35893457_2.fastq.gz`.

```bash
# seqkit stats: conta reads e mostra tamanho médio
seqkit stats data/raw/SRR35893457_*.fastq.gz
```

O download depende da internet e pode falhar. Se falhar, rode o `prefetch` de novo. Veja [Problemas comuns](#9-problemas-comuns).

```bash
git add -A
git commit -m "download do SRA"
git push
```

---

## 4. QC das reads brutas (FastQC + MultiQC)

```bash
conda activate euk_preprocess
mkdir -p results/qc/raw

# fastqc: relatório de qualidade das reads
# -o: pasta de saída
# -t 1: 1 thread
fastqc data/raw/SRR35893457_1.fastq.gz data/raw/SRR35893457_2.fastq.gz \
  -o results/qc/raw -t 1

# multiqc: junta os relatórios FastQC num HTML só
# -o: pasta de saída
# -n: nome do arquivo HTML
multiqc results/qc/raw -o results/qc/raw -n multiqc_raw.html
```

Abra no navegador:

- `results/qc/raw/*_fastqc.html`
- `results/qc/raw/multiqc_raw.html`

No WSL, para abrir a pasta no Explorer:

```bash
# wslpath -w: converte o caminho Linux para o formato do Windows
explorer.exe "$(wslpath -w results/qc/raw)"
```

**O que olhar:** qualidade por base (Phred), presença de adaptadores, conteúdo GC, *overrepresented sequences*.

```bash
git add -A
git commit -m "QC das reads brutas"
git push
```

---

## 5. Trim / filtro com fastp

```bash
conda activate euk_preprocess
mkdir -p data/trimmed results/qc/trimmed

# fastp: remove adaptadores e reads ruins
# -i / -I: FASTQ de entrada (R1 e R2)
# -o / -O: FASTQ de saída já filtrados
# --detect_adapter_for_pe: detecta adaptadores em paired-end
# --qualified_quality_phred 20: bases com Phred < 20 contam como ruins
# --length_required 50: descarta reads menores que 50 bases
# --thread 1: 1 thread
# --html / --json: relatórios do fastp
fastp \
  -i data/raw/SRR35893457_1.fastq.gz \
  -I data/raw/SRR35893457_2.fastq.gz \
  -o data/trimmed/SRR35893457_1.trim.fastq.gz \
  -O data/trimmed/SRR35893457_2.trim.fastq.gz \
  --detect_adapter_for_pe \
  --qualified_quality_phred 20 \
  --length_required 50 \
  --thread 1 \
  --html results/qc/trimmed/fastp_SRR35893457.html \
  --json results/qc/trimmed/fastp_SRR35893457.json
```

QC depois do trim:

```bash
fastqc data/trimmed/SRR35893457_*.trim.fastq.gz -o results/qc/trimmed -t 1
multiqc results/qc/trimmed -o results/qc/trimmed -n multiqc_trimmed.html
seqkit stats data/trimmed/SRR35893457_*.trim.fastq.gz
```

Compare o relatório **antes** vs **depois** do fastp.

```bash
git add -A
git commit -m "trim com fastp"
git push
```

---

## 6. Montagem com MEGAHIT

Esta é a etapa mais pesada (usa mais RAM). Feche o navegador e outros programas grandes antes de rodar.

```bash
conda activate euk_assemble

# apaga uma montagem anterior, se existir
# (o MEGAHIT recusa se a pasta de saída já estiver lá)
rm -rf results/assembly/SRR35893457_megahit

# megahit: monta o genoma (junta as reads em contigs)
# -1 / -2: FASTQ R1 e R2 já trimados
# -o: pasta de saída
# -t 1: 1 thread
# -m 0.5: usa no máximo metade da RAM
# --min-contig-len 500: descarta contigs menores que 500 bases
megahit \
  -1 data/trimmed/SRR35893457_1.trim.fastq.gz \
  -2 data/trimmed/SRR35893457_2.trim.fastq.gz \
  -o results/assembly/SRR35893457_megahit \
  -t 1 \
  -m 0.5 \
  --min-contig-len 500
```

Pode demorar. Se aparecer erro, copie a mensagem.

```bash
ls -lh results/assembly/SRR35893457_megahit/final.contigs.fa
seqkit stats results/assembly/SRR35893457_megahit/final.contigs.fa
```

```bash
git add -A
git commit -m "montagem MEGAHIT"
git push
```

---

## 7. Avaliar a montagem com QUAST

```bash
conda activate euk_assemble

# quast.py: calcula métricas da montagem (N50, nº de contigs, etc.)
# -o: pasta do relatório
# -t 1: 1 thread
# --min-contig 500: avalia só contigs ≥ 500 bases
quast.py \
  results/assembly/SRR35893457_megahit/final.contigs.fa \
  -o results/quast/SRR35893457 \
  -t 1 \
  --min-contig 500
```

Relatório: `results/quast/SRR35893457/report.html` (também tem `report.txt`).

Como esta montagem é **de novo**, o QUAST recebe só os contigs — sem genoma de referência. Dá para avaliar se a montagem faz sentido (tamanho total perto de ~12 Mb, N50, número de contigs, GC). Com uma referência, o QUAST também apontaria inversões, translocações e quanto do genoma real foi coberto.

| Métrica | Significado |
|---------|-------------|
| `# contigs` | Quantos pedaços a montagem gerou |
| `Largest contig` | Maior contig |
| `Total length` | Tamanho total montado (~12 Mb esperado para levedura) |
| `N50` | Metade do genoma está em contigs ≥ N50 |
| `GC %` | Conteúdo GC (~38–40% típico em *S. cerevisiae*) |

Abra o `report.html` e interprete essas métricas. O fluxo principal termina aqui; a seção seguinte (IGV) é **opcional**, mas ajuda a *ver* o que a montagem fez.

```bash
git add -A
git commit -m "avaliação QUAST"
git push
```

---

## 8. Alinhar e abrir no IGV (opcional)

Na prática, em um projeto *de novo* você **não** teria o gabarito. Aqui temos a referência de *S. cerevisiae* (S288C), então dá para checar cobertura, gaps e (depois) SNPs — e também ver onde a montagem quebra.

Dois usos úteis:

| O quê | Ferramenta | Para quê no IGV |
|-------|------------|-----------------|
| **reads → referência** | `bwa` + `samtools` | Uso clássico: cobertura, gaps, SNPs |
| **contigs → referência** | `minimap2` + `samtools` | Continuidade / *breaks* da montagem |

### 8.1 Baixar a referência (S288C)

```bash
conda activate euk_assemble
mkdir -p data/reference results/align

# genoma de referência S288C (R64, NCBI RefSeq)
# -O: nome do arquivo de saída
wget -O data/reference/S288C.fna.gz \
  "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.fna.gz"

# descompacta para FASTA
gunzip -c data/reference/S288C.fna.gz > data/reference/S288C.fa
ls -lh data/reference/S288C.fa
```

### 8.2 Reads → referência → BAM (uso clássico do IGV)

```bash
# bwa index: indexa a referência (só precisa uma vez)
bwa index data/reference/S288C.fa

# bwa mem: alinha as reads trimadas na referência
# samtools sort: ordena e grava BAM
# -t 1 / -@ 1: 1 thread
bwa mem -t 1 data/reference/S288C.fa \
  data/trimmed/SRR35893457_1.trim.fastq.gz \
  data/trimmed/SRR35893457_2.trim.fastq.gz \
  | samtools sort -@ 1 -o results/align/reads_vs_ref.bam

# samtools index: cria o .bai (obrigatório no IGV)
samtools index results/align/reads_vs_ref.bam

ls -lh results/align/reads_vs_ref.bam*
```

### 8.3 Contigs → referência → BAM (continuidade / breaks)

```bash
# minimap2: alinha contigs longos na referência
# -ax asm5: preset para assembly vs referência próxima
# -t 1: 1 thread
minimap2 -ax asm5 -t 1 data/reference/S288C.fa \
  results/assembly/SRR35893457_megahit/final.contigs.fa \
  | samtools sort -@ 1 -o results/align/contigs_vs_ref.bam

samtools index results/align/contigs_vs_ref.bam
ls -lh results/align/contigs_vs_ref.bam*
```

### 8.4 Abrir no IGV

1. Baixe o [IGV](https://igv.org/doc/desktop/) (Desktop).
2. **Genomes → Load Genome from File…** → escolha `data/reference/S288C.fa`.
3. **File → Load from File…** → carregue `results/align/reads_vs_ref.bam`.
4. (Opcional) carregue também `results/align/contigs_vs_ref.bam` como outra trilha.

**O que olhar:**

- na trilha de **reads**: cobertura mais ou menos uniforme; buracos (gaps); regiões repetitivas com cobertura estranha
- na trilha de **contigs**: se os contigs “andam” contínuos ao longo do cromossomo ou se há quebras / saltos

No WSL, para achar a pasta no Explorer:

```bash
explorer.exe "$(wslpath -w results/align)"
```

```bash
git add -A
git commit -m "alinhamento para IGV"
git push
```

---

## 9. Checklist do que deve existir ao final

```text
data/raw/SRR35893457_{1,2}.fastq.gz
data/trimmed/SRR35893457_{1,2}.trim.fastq.gz
results/qc/raw/multiqc_raw.html
results/qc/trimmed/fastp_SRR35893457.html
results/qc/trimmed/multiqc_trimmed.html
results/assembly/SRR35893457_megahit/final.contigs.fa
results/quast/SRR35893457/report.html
```

Se fez a seção do IGV:

```text
data/reference/S288C.fa
results/align/reads_vs_ref.bam
results/align/reads_vs_ref.bam.bai
results/align/contigs_vs_ref.bam
results/align/contigs_vs_ref.bam.bai
```

---

## 10. Problemas comuns

| Problema | O que tentar |
|----------|--------------|
| `prefetch` / `fasterq-dump` falha | Rodar o `prefetch` de novo; conferir internet e espaço em disco |
| Disco cheio | Ver `du -sh ~/.ncbi data results`; apagar cache antigo do SRA se precisar |
| `conda activate` não funciona | `conda init bash`, fechar e abrir o terminal |
| MEGAHIT recusa a pasta de saída | `rm -rf results/assembly/SRR35893457_megahit` e rodar de novo |
| Pouca RAM na montagem | Fechar o navegador; usar máquina do laboratório; manter `-m 0.5` |
| `bwa` / `minimap2` / `samtools` não encontrados | `conda env update -f envs/assemble.yml` |

---

## Referência rápida da amostra

- **Run:** SRR35893457
- **Organismo:** *Saccharomyces cerevisiae*
- **Tipo:** Illumina WGS paired-end
- **Por que esta?** Genoma eucarioto pequeno, download leve (~0,5 GB), montagem rápida
