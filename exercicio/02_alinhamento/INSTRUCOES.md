# Exercício 2 — Alinhamento

Trabalhe em `pipeline_ab_evo/exercicio/02_alinhamento/`.  
Guarde scripts em `pipeline_ab_evo/exercicio/02_alinhamento/scripts/`, figuras em `pipeline_ab_evo/exercicio/02_alinhamento/figuras/` e respostas em `pipeline_ab_evo/exercicio/02_alinhamento/respostas.md`.

---

## Parte A — BLASTN

Você tem:

- **Query:** `pipeline_ab_evo/exercicio/02_alinhamento/dados/genes.fasta` (6 sequências)
- **Banco:** `pipeline_ab_evo/exercicio/02_alinhamento/dados/contigs.fasta`

| Gene (cabeçalho) | O que é |
|------------------|---------|
| `ACT1_levedura` | actina de levedura |
| `ACTB_humana` | actina humana (mRNA) |
| `COX3_levedura` | gene mitocondrial |
| `GAL1_levedura` | galactoquinase |
| `RDN18_levedura` | rRNA 18S |
| `artificial` | sequência inventada (controle negativo) |

### Passos

1. Crie o banco BLAST:

```bash
mkdir -p pipeline_ab_evo/exercicio/02_alinhamento/resultados/blast

makeblastdb \
  -in pipeline_ab_evo/exercicio/02_alinhamento/dados/contigs.fasta \
  -dbtype nucl \
  -out pipeline_ab_evo/exercicio/02_alinhamento/resultados/blast/contigs
```

2. Rode o `blastn` (use `-task blastn` para aceitar identidades um pouco menores):

```bash
blastn -task blastn \
  -query pipeline_ab_evo/exercicio/02_alinhamento/dados/genes.fasta \
  -db pipeline_ab_evo/exercicio/02_alinhamento/resultados/blast/contigs \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
  -evalue 1e-5 \
  -out pipeline_ab_evo/exercicio/02_alinhamento/resultados/blast/saida.tsv
```

3. Olhe `saida.tsv`. Colunas úteis:

| Coluna | Significado |
|--------|-------------|
| `qseqid` | gene da query |
| `sseqid` | contig do banco |
| `pident` | % de identidade |
| `qcovs` | % da query coberta |
| `evalue` | quanto menor, menos provável ser acaso |

Exemplo opcional: `bash exemplos/blastn_exemplo.sh` (a partir desta pasta).

### Questões (Parte A)

1. Quais genes tiveram hit? Qual **não** teve? Por quê?
2. Olhando `pident` e `qcovs`, qual hit parece o mais confiável? Por quê?

---

## Parte B — Alinhamento múltiplo (MAFFT + Biopython)

O arquivo `pipeline_ab_evo/exercicio/02_alinhamento/dados/hemoglobina_beta.fasta` tem a hemoglobina beta de **5 espécies**.

1. Leia e rode o exemplo:

```bash
cd pipeline_ab_evo/exercicio/02_alinhamento
python exemplos/msa_exemplo.py
```

2. Adapte (ou copie para `scripts/`) para alinhar com `mafft`, ler com Biopython, calcular distâncias, montar a árvore e salvar a figura em `figuras/`.

### Ferramentas (resumo)

- `mafft --auto arquivo.fasta` → alinhamento múltiplo (stdout)
- Biopython: `AlignIO.read`, `DistanceCalculator("identity")`, `DistanceTreeConstructor().nj`, `Phylo.draw` / `Phylo.draw_ascii`

### Questões (Parte B)

1. Quais duas espécies ficaram com distância **0** (sequências idênticas)? Isso faz sentido biologicamente?
2. Qual espécie ficou mais distante das demais na árvore? O que isso indica?
