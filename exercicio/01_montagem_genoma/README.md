# Exercício 1 — Montagem de genoma de novo (Illumina)

Treino **passo a passo** do fluxo clássico:

**SRA → QC → trim → montagem → avaliação** (e, se quiser, **QUAST com referência + IGV**)

Não é um pipeline automático: rode cada comando, abra os relatórios e entenda cada etapa. No caminho, pratica Git e GitHub.

Abra o [SETUP](docs/SETUP.md) e o [tutorial](docs/TUTORIAL.md) **pelo GitHub** (no navegador) para ver o Markdown formatado. Os comandos você cola no terminal.

## Amostra de treino

| Campo | Valor |
|-------|--------|
| Organismo | *Saccharomyces cerevisiae* (levedura) |
| Run SRA | **SRR35893457** |
| Tecnologia | Illumina paired-end (WGS) |
| Por que esta? | Genoma ~12 Mb: download leve e montagem rápida |

## O que você precisa

- **Linux** ou **Windows com WSL** (veja [docs/SETUP.md](docs/SETUP.md))
- **Conda** (Miniconda)
- Cerca de **10 a 15 GB livres** no disco
- **4 GB de RAM** no mínimo (8 GB fica mais confortável)

## Como começar

1. Instale o ambiente: **[docs/SETUP.md](docs/SETUP.md)**
2. Entre nesta pasta:

```bash
cd pipeline_ab_evo/exercicio/01_montagem_genoma
```

3. Crie os ambientes conda:

```bash
conda env create -f pipeline_ab_evo/exercicio/01_montagem_genoma/envs/preprocess.yml   # SRA, FastQC, MultiQC, fastp
conda env create -f pipeline_ab_evo/exercicio/01_montagem_genoma/envs/assemble.yml     # MEGAHIT, QUAST, bwa, minimap2, samtools
```

(Se você já estiver dentro de `pipeline_ab_evo/exercicio/01_montagem_genoma`, use `envs/preprocess.yml` e `envs/assemble.yml`.)

4. Siga o tutorial: **[docs/TUTORIAL.md](docs/TUTORIAL.md)**
5. Depois de cada etapa: `git add`, `git commit` e `git push`

Quando terminar, vá para o **[Exercício 2 — Alinhamento](../02_alinhamento/)** em `pipeline_ab_evo/exercicio/02_alinhamento/`.

## Estrutura

```text
pipeline_ab_evo/exercicio/01_montagem_genoma/
├── envs/           Ambientes conda
├── docs/           SETUP e tutorial
├── data/raw/       FASTQ brutos (não vão para o GitHub)
├── data/trimmed/   FASTQ depois do fastp
├── data/reference/ Genoma de referência para IGV
└── results/        QC, assembly, QUAST (pesados ficam fora do git)
```
