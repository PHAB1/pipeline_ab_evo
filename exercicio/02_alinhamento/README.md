# Exercício 2 — Alinhamento

Objetivo: (1) procurar genes com **BLASTN** e (2) fazer **alinhamento múltiplo** com MAFFT + Biopython.

## Estrutura

```text
pipeline_ab_evo/exercicio/02_alinhamento/
├── README.md
├── INSTRUCOES.md
├── dados/
│   ├── genes.fasta              ← queries do BLAST
│   ├── contigs.fasta            ← banco do BLAST
│   └── hemoglobina_beta.fasta   ← sequências do MSA
├── exemplos/
│   ├── blastn_exemplo.sh
│   ├── ade2.fasta
│   └── msa_exemplo.py
├── scripts/                     ← seus scripts
├── figuras/                     ← figura da árvore
└── resultados/
    ├── blast/
    └── alinhamento/
```

## Como começar

\* Instalação do ambiente em: [`pipeline_ab_evo/exercicio/README.md`](../README.md).

```bash
conda activate euk_align
cd pipeline_ab_evo/exercicio/02_alinhamento
```

Siga: [INSTRUCOES.md](INSTRUCOES.md) (Parte A = BLASTN, Parte B = alinhamento múltiplo).
