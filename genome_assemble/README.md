# Montagem de genoma de novo (Illumina)

Neste repositório você treina, **passo a passo**, o fluxo clássico de montagem de genoma a partir de reads Illumina:

**SRA → QC → trim → montagem → avaliação**

Não é um pipeline automático. A ideia é você rodar cada comando, abrir os relatórios e ir entendendo o que cada etapa faz. No caminho, você também pratica Git e GitHub.

Abra o **README**, o [SETUP](docs/SETUP.md) e o [tutorial](docs/TUTORIAL.md) **pelo GitHub** (no navegador). Assim o Markdown aparece formatado. Os comandos você cola no terminal.

## Amostra de treino

| Campo | Valor |
|-------|--------|
| Organismo | *Saccharomyces cerevisiae* (levedura) |
| Run SRA | **SRR35893457** |
| Tecnologia | Illumina paired-end (WGS) |
| Por que esta? | Genoma ~12 Mb: download leve e montagem rápida, mesmo em PC comum |

## O que você precisa

- **Linux** ou **Windows com WSL** (veja [docs/SETUP.md](docs/SETUP.md))
- **Conda** (Miniconda)
- Cerca de **10 a 15 GB livres** no disco
- **4 GB de RAM** no mínimo (8 GB fica mais confortável)

Se o computador travar na montagem, use as máquinas do laboratório.

## Como começar

1. Instale o ambiente (WSL, se for Windows, e o Miniconda): **[docs/SETUP.md](docs/SETUP.md)**
2. Clone este repositório
3. Crie os dois ambientes conda:

```bash
conda env create -f envs/preprocess.yml   # SRA, FastQC, MultiQC, fastp
conda env create -f envs/assemble.yml     # MEGAHIT, QUAST
```

4. Siga o tutorial na ordem: **[docs/TUTORIAL.md](docs/TUTORIAL.md)**
5. Depois de cada etapa, faça `git add`, `git commit` e `git push` (está no tutorial)

## Estrutura

```text
envs/           Ambientes conda
docs/           Tutorial e instalação
data/raw/       FASTQ brutos (não vão para o GitHub)
data/trimmed/   FASTQ depois do fastp (não vão para o GitHub)
results/        QC, assembly, QUAST (arquivos grandes ficam de fora do git)
```
