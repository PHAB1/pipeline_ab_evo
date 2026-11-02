# Exercícios

Material de treino separado do pipeline `ab_evo`.

| Exercício | Pasta | O que é |
|-----------|--------|---------|
| **1 — Montagem de genoma** | [`pipeline_ab_evo/exercicio/01_montagem_genoma/`](01_montagem_genoma/) | SRA → QC → trim → MEGAHIT → QUAST (e IGV) |
| **2 — Alinhamento** | [`pipeline_ab_evo/exercicio/02_alinhamento/`](02_alinhamento/) | BLASTN + alinhamento múltiplo (MAFFT/Biopython) |

Ambiente do exercício 2 (uma vez):

```bash
conda env create -f pipeline_ab_evo/exercicio/envs/align.yml
conda activate euk_align
```

Os caminhos nestes textos começam em `pipeline_ab_evo/` (raiz deste repositório).
