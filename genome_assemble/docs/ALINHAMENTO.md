# Alinhamento de sequências: global, local, BLAST e múltiplo

Abra este arquivo **no GitHub** (no navegador) para ver o texto formatado. Os comandos você cola no terminal.

Objetivo: entender **o que é alinhar**, **quando usar cada tipo** de alinhamento e **como rodar** cada um (BLAST no terminal, o resto em Python com Biopython).

Todos os comandos são **na pasta do projeto** (a mesma do tutorial de montagem).

---

## 0. O que você vai usar

| Etapa | Ambiente conda | Ferramentas |
|-------|----------------|-------------|
| BLAST | `euk_align` | `makeblastdb`, `blastn`, `tblastx` |
| Alinhamento par a par | `euk_align` | Biopython (`PairwiseAligner`) |
| Alinhamento múltiplo + árvore | `euk_align` | `mafft` + Biopython (`AlignIO`, `Phylo`) |

Crie o ambiente (só uma vez):

```bash
conda env create -f envs/align.yml
conda activate euk_align

# confere se está tudo lá
blastn -version
mafft --version
python -c "import Bio; print(Bio.__version__)"
```

Se estiver em **Mac com chip M1/M2/M3** e o `conda env create` reclamar que não acha algum pacote, crie o ambiente na versão Intel (roda normal pelo Rosetta):

```bash
CONDA_SUBDIR=osx-64 conda env create -f envs/align.yml
conda activate euk_align
conda config --env --set subdir osx-64
```

---

## 1. O que é alinhar?

Alinhar é colocar duas (ou mais) sequências lado a lado, inserindo **gaps** (`-`) onde for preciso, para que as posições **equivalentes** fiquem na mesma coluna.

```text
GATTACAGATTACACCGT
|||.||||||||||
GATCACAGATTACA----
```

- `|` **match** (igual): ganha pontos
- `.` **mismatch** (troca): perde pontos
- `-` **gap** (inserção/deleção): perde pontos. Abrir um gap custa mais que estender um que já existe.

O programa testa as possibilidades e devolve o alinhamento de **maior score** (pontuação).

Em proteína, nem toda troca é igual: trocar leucina (L) por isoleucina (I), que são parecidas, quase não muda a proteína. Por isso usamos uma **matriz de substituição** (a mais comum é a **BLOSUM62**), que dá nota para cada par de aminoácidos.

---

## 2. Quando usar cada tipo

| Tipo | Pergunta que responde | Exemplo | Ferramenta |
|------|----------------------|---------|------------|
| **Global** (Needleman-Wunsch) | "Essas duas sequências, **de ponta a ponta**, são parecidas? Onde diferem?" | Comparar o mesmo gene de duas cepas | Biopython `mode = "global"` |
| **Local** (Smith-Waterman) | "Existe um **trecho** parecido entre elas?" | Achar um domínio ou fragmento dentro de uma proteína maior | Biopython `mode = "local"` |
| **BLAST** | "**Onde** está esta sequência num banco grande? **Quem** é ela?" | Achar um gene nos contigs da montagem; identificar uma sequência desconhecida | `blastn`, `blastp`, `tblastx`… |
| **Múltiplo** (MSA) | "O que é **conservado** entre várias sequências? Quem é parente de quem?" | Mesmo gene em várias espécies → árvore | `mafft` (+ Biopython para analisar) |

Regra prática:

- Sequências de **tamanho parecido** e você quer comparar **inteiras** → **global**
- Uma é **pedaço** da outra, ou só uma parte é parecida → **local**
- Uma sequência contra **milhares/milhões** (um genoma, o GenBank) → **BLAST** (é um alinhamento local, mas com atalhos para ser rápido)
- **Três ou mais** sequências → **múltiplo**

---

## 3. BLAST no terminal

### 3.1 Criar o banco (uma vez)

O BLAST não procura direto no FASTA: primeiro transforma o FASTA num banco indexado.

```bash
conda activate euk_align
mkdir -p results/blast

# makeblastdb: transforma um FASTA em banco de dados do BLAST
# -in: FASTA de entrada (aqui, os contigs da sua montagem)
# -dbtype nucl: banco de DNA (para proteína seria prot)
# -out: prefixo dos arquivos do banco
makeblastdb \
  -in results/assembly/SRR35893457_megahit/final.contigs.fa \
  -dbtype nucl \
  -out results/blast/contigs
```

### 3.2 Procurar uma sequência

```bash
# blastn: DNA contra DNA
# -query: sequência que você quer achar
# -db: banco onde procurar
# -outfmt 6: saída em tabela (uma linha por hit)
# -evalue 1e-10: só mostra hits com e-value menor que 1e-10
blastn \
  -query alinhamento/demo/ade2.fasta \
  -db results/blast/contigs \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
  -evalue 1e-10
```

| Coluna | Significado |
|--------|-------------|
| `qseqid` | Nome da query (sua sequência) |
| `sseqid` | Nome do hit no banco (aqui, o contig) |
| `pident` | % de identidade no trecho alinhado |
| `length` | Tamanho do trecho alinhado |
| `qcovs` | % da query coberta pelo alinhamento |
| `evalue` | Quantos hits tão bons você esperaria **por acaso**. Quanto menor, melhor (`0.0` = praticamente impossível ser acaso) |
| `bitscore` | Score normalizado. Quanto maior, melhor |

Sem `-outfmt`, o BLAST mostra o alinhamento desenhado (bom para olhar; ruim para automatizar).

**Cuidado:** `pident` alto com `qcovs` baixo = só um pedacinho bateu. Olhe sempre os dois.

### 3.3 Sensibilidade: `-task`

O `blastn` tem modos diferentes. Por padrão ele usa o `megablast`, que é rápido, mas só acha sequências **quase idênticas**.

| `-task` | Acha o quê | Quando usar |
|---------|-----------|-------------|
| `megablast` (padrão) | ≳ 95% de identidade | Mesmo gene, mesma espécie |
| `dc-megablast` | Espécies próximas | Mesmo gene, espécie parecida |
| `blastn` | Mais divergente (~70%) | Quando o megablast não acha nada |

```bash
blastn -task blastn \
  -query alinhamento/demo/ade2.fasta \
  -db results/blast/contigs \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
  -evalue 1e-10
```

### 3.4 A família BLAST

| Programa | Query | Banco | Para quê |
|----------|-------|-------|----------|
| `blastn` | DNA | DNA | Achar gene/região num genoma |
| `blastp` | proteína | proteína | Achar proteínas parecidas |
| `blastx` | DNA (traduzido) | proteína | "Que proteína este trecho de DNA codifica?" |
| `tblastn` | proteína | DNA (traduzido) | Achar um gene num genoma a partir da proteína |
| `tblastx` | DNA (traduzido) | DNA (traduzido) | DNA muito divergente (espécies distantes) |

Por que traduzir ajuda? O código genético é redundante: várias trocas no DNA (principalmente na 3ª base do códon) **não mudam o aminoácido**. Duas espécies distantes podem ter DNA bem diferente e proteína quase igual.

---

## 4. Demonstração

Precisa da montagem pronta (`results/assembly/SRR35893457_megahit/final.contigs.fa`).

```bash
conda activate euk_align

# 1) BLAST: acha o gene ADE2 (levedura) nos contigs
bash alinhamento/demo/01_blastn.sh

# 2) Global vs local, com DNA e com proteína
python alinhamento/demo/02_pairwise.py

# 3) Alinhamento múltiplo da hemoglobina beta + árvore
python alinhamento/demo/03_msa_arvore.py
```

| Script | O que observar |
|--------|----------------|
| `01_blastn.sh` | Em qual contig o ADE2 caiu, com que identidade e cobertura. Abra `results/blast/ade2_vs_contigs.txt` para ver o alinhamento desenhado |
| `02_pairwise.py` | Com o pedaço de hemoglobina, o **global** espalha gaps pela sequência inteira (score baixo); o **local** acha só o trecho certo (score alto) |
| `03_msa_arvore.py` | Humano e chimpanzé têm hemoglobina beta idêntica. Figura em `results/alinhamento/hemoglobina_beta_arvore.png` |

### 4.1 Biopython em 10 linhas

```python
from Bio import Align
from Bio.Align import substitution_matrices

aligner = Align.PairwiseAligner()
aligner.mode = "local"                     # ou "global"
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
aligner.open_gap_score = -10               # abrir gap
aligner.extend_gap_score = -0.5            # estender gap

melhor = aligner.align("MVHLTPEEKSAVTALW", "LTPEEKSAV")[0]
print(melhor.score)
print(melhor)
```

Para alinhamento múltiplo, o Biopython **não alinha**: quem alinha é o `mafft`. O Biopython lê o resultado (`AlignIO.read`) e calcula distâncias e árvore (`Bio.Phylo`). Veja `alinhamento/demo/03_msa_arvore.py`.

---

## 5. Próximo passo

Exercício: **[EXERCICIO_ALINHAMENTO.md](EXERCICIO_ALINHAMENTO.md)**
