# Módulo de vias e grafos

Ideia: em vez de olhar um gene por vez, pegar **vários genes-alvo ao mesmo tempo**, verificar em que vias eles estão, agrupar em **módulos** e comparar esses módulos entre as espécies (quais vias estão conservadas, incompletas, perdidas ou "religadas").

## Entrada

- Lista de genes-alvo (proteínas FASTA), ou
- Uma via/módulo de interesse (ex.: IDs de módulos KEGG), que vira a lista de genes.

## Etapas

### 1. Encontrar os genes em cada espécie
- Ortólogos via [OrthoFinder](https://github.com/davidemms/OrthoFinder) (já roda em [[Análises evolutivas]]).
- Anotação funcional: [eggNOG-mapper](https://github.com/eggnogdb/eggnog-mapper) e [KofamScan](https://github.com/takaram/kofam_scan) (atribui KOs do KEGG).

### 2. Matriz de perfil filogenético
- Tabela espécie × gene com presença/ausência e número de cópias.
- Completude de módulos KEGG por espécie: [anvi'o](https://github.com/merenlab/anvio) (`anvi-estimate-metabolism`) ou [kegg-pathways-completeness](https://github.com/EBI-Metagenomics/kegg-pathways-completeness-tool).
- Visualização: [PhyloProfile](https://github.com/BIONF/PhyloProfile).
- Procariotos: [gapseq](https://github.com/jotech/gapseq) reconstrói vias metabólicas completas.

### 3. Construir o grafo
Nós = genes (grupos de ortólogos). Arestas podem vir de fontes diferentes, e vale manter cada tipo separado:

| Tipo de aresta | Significado | Fonte |
|---|---|---|
| Via conhecida | genes em reações adjacentes da mesma via | KEGG |
| Interação | interação física ou funcional conhecida | [STRING](https://string-db.org) |
| Coevolução de presença/ausência | genes que aparecem e somem juntos nas espécies | matriz da etapa 2, corrigindo pela árvore de espécies |
| Coevolução de taxa (ERC) | genes cujas taxas de evolução sobem e descem juntas nos mesmos ramos | árvores de genes + árvore de espécies; [RERconverge](https://github.com/nclark-lab/RERconverge) |
| Sintenia | genes vizinhos no genoma (operons em procariotos) | coordenadas da anotação |

Implementação: [NetworkX](https://github.com/networkx/networkx) ou [python-igraph](https://github.com/igraph/python-igraph).

### 4. Módulos
- Detecção de comunidades: Leiden ([leidenalg](https://github.com/vtraag/leidenalg)) ou MCL.
- Comparar os módulos encontrados com as vias KEGG: módulos que batem com vias conhecidas validam o método; módulos novos são hipóteses.

### 5. Comparar módulos entre espécies
- Completude de cada módulo por espécie, projetada na árvore de espécies: onde a via foi perdida ou ganha.
- Conservação da estrutura do módulo: mesmo conjunto de genes e mesmas conexões, ou genes substituídos (ex.: enzima trocada por outra não homóloga).
- Pressão seletiva por módulo: agregar os resultados do HyPhy (dN/dS) dos genes de cada módulo.
- Expansão/contração de famílias por módulo (CAFE5).

## O que já existe e o que seria novo

Já existem separadamente: perfis filogenéticos (PhyloProfile, STRING), completude de módulos KEGG (anvi'o), coevolução de taxas (ERC/RERconverge), pangenomas em grafo (Panaroo, PPanGGOLiN).

A ideia central (dividir um conjunto de genes em módulos que coevoluem, usando presença/ausência sobre a árvore) **já existe**: [CLIME](https://www.gene-clime.org/) e [CladeOScope-GSA](https://pmc.ncbi.nlm.nih.gov/articles/PMC12898691/). Ambos dependem de espécies e matrizes pré-calculadas, centradas em organismos-modelo.

O que ainda pode ser contribuição: aplicar essa análise às espécies do próprio usuário (montando a matriz a partir de reads ou fontes mistas, com ausência confiável) e combinar várias evidências de ligação no mesmo grafo. Ver [[Estado da arte]].

## Cuidados

- **Ausência de gene pode ser artefato**, por motivos diferentes em cada modo:
  - modo global: montagem incompleta ou anotação ruim. Usar BUSCO/CheckM2 para filtrar espécies com genomas ruins, e confirmar ausências com miniprot direto no genoma;
  - modo direcionado: cobertura baixa ou referência distante demais. Ver "Cuidados do modo direcionado" em [[Análises evolutivas]].
- **Presença/ausência sem correção filogenética** gera falsos positivos: espécies próximas compartilham genes por herança, não por função.
- Em eucariotos, sintenia é bem mais fraca que em procariotos.
