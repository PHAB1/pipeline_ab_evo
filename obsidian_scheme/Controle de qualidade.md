# Controle de qualidade

Primeira etapa depois de obter as reads (FASTQ), públicas via [SRA Toolkit](https://github.com/ncbi/sra-tools) ou do próprio usuário. As ferramentas dependem da tecnologia de sequenciamento.

## Illumina (reads curtas)

| Etapa | Ferramenta | Observação |
|---|---|---|
| Adaptadores, qualidade, relatório por amostra | [fastp](https://github.com/OpenGene/fastp) | faz tudo numa passada e já gera relatório HTML/JSON |

## Nanopore (reads longas)

| Etapa | Ferramenta | Observação |
|---|---|---|
| Remoção de adaptadores | [Porechop](https://github.com/rrwick/Porechop) | não é mais mantido; considerar [Porechop_ABI](https://github.com/bonsai-team/Porechop_ABI) |
| Filtragem por tamanho e qualidade | [Filtlong](https://github.com/rrwick/Filtlong) | útil para reduzir cobertura excessiva mantendo as melhores reads |
| Filtragem por tamanho e qualidade | [NanoFilt](https://github.com/wdecoster/nanofilt) | descontinuado pelo autor; o substituto é o [chopper](https://github.com/wdecoster/chopper) |

## Relatório consolidado

- [MultiQC](https://github.com/MultiQC/MultiQC): junta os relatórios de todas as amostras e ferramentas num só HTML.

## Saída

Reads limpas, que seguem para a montagem (modo global) ou para o enriquecimento alvo específico (modo direcionado). Ver [[Ramos eucarioto e procarioto]] e [[Análises evolutivas]].
