# Revisão de escopo: pipelines de evolução comparativa

Data da busca: 13/10/2026. Complementa [[Estado da arte]].

> [!warning] Limitação
> Esta é uma **revisão de escopo** feita por busca web (artigos, PMC, bioRxiv, GitHub, documentação), não uma revisão sistemática formal. Não houve busca em Scopus/Web of Science nem triagem por dois revisores. Serve para orientar o projeto e como ponto de partida para a revisão formal (ver "Próximos passos").

## Pergunta

Existe alguma ferramenta que faça o **ciclo completo** para o usuário: dados brutos (reads) ou sequências públicas → genes-alvo ou genoma inteiro → ortologia → filogenia → seleção → estrutura → presença/ausência confiável → comparação de vias/módulos, para **espécies não-modelo** escolhidas pelo usuário?

## Método

**Buscas realizadas** (termos principais):
1. gene of interest + positive selection + duplication + recombination pipeline
2. pipeline gene → orthologs in assemblies → positive selection → AlphaFold structure
3. reads (target capture, genome skimming, RNA-seq, WGS) → phylogenomic markers
4. conservation mapped onto structure (homologs + phylogeny)
5. automated positive selection pipelines (HyPhy, PAML)
6. Nextflow/Snakemake phylogenomics for non-model organisms
7. nf-core ortholog retrieval from public databases
8. immunoglobulin loci annotation in non-model genomes
9. integrated gene family evolution + selection + structure (2025–2026)
10. read-based target gene extraction (non-HybPiper)
11. targeted ortholog search + presence/absence profiles
12. gene loss vs assembly artifact
13. phylogenetic profiling modules (co-evolution)
14. reads/assemblies → pathway presence/absence
15. read-based gene presence/absence with coverage

**Critérios de inclusão**: ferramenta publicada (artigo ou preprint) ou com documentação pública, que automatize **duas ou mais** etapas do ciclo, ou uma etapa crítica para o nosso diferencial (ausência confiável, módulos, anticorpos).

## Matriz de cobertura

Legenda: ✅ faz · ◐ faz em parte · – não faz

Colunas:
- **Reads**: aceita reads brutas
- **BD**: busca sequências em bancos públicos
- **Alvo**: recupera genes-alvo específicos
- **Global**: ortologia genômica ampla
- **Árvore**: filogenia de gene e/ou espécie
- **Rec.**: reconciliação (duplicação/perda)
- **Sel.**: seleção (dN/dS)
- **Estr.**: mapeia resultados na estrutura
- **Aus.**: presença/ausência com ausência confiável
- **Vias**: comparação de vias/módulos
- **Livre**: espécies escolhidas pelo usuário (sem conjunto fixo)

| Ferramenta | Reads | BD | Alvo | Global | Árvore | Rec. | Sel. | Estr. | Aus. | Vias | Livre |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [OrthoGarden](https://github.com/jacksonhturner/orthogarden) | ✅ | ◐ | – | ✅ | ✅ | – | – | – | – | – | ✅ |
| [NovelTree](https://github.com/Arcadia-Science/noveltree) | – | – | – | ✅ | ✅ | ✅ | – | – | – | – | ✅ |
| [Captus](https://edgardomortiz.github.io/captus.docs/) | ✅ | – | ✅ | – | ◐ | – | – | – | – | – | ✅ |
| [GeneMiner](https://github.com/sculab/GeneMiner) / Easy353 | ✅ | – | ✅ | – | – | – | – | – | – | – | ✅ |
| [HybPiper](https://github.com/mossmatters/HybPiper) / [aTRAM](https://github.com/juliema/aTRAM) | ✅ | – | ✅ | – | – | – | – | – | – | – | ✅ |
| [Read2Tree](https://github.com/DessimozLab/read2tree) | ✅ | ◐ | ✅ | – | ✅ | – | – | – | – | – | ✅ |
| [DGINN](https://github.com/leapicard/DGINN) | – | ✅ | ✅ | – | ✅ | ✅ | ✅ | – | – | – | ✅ |
| [FREEDA](https://github.com/DDudka9/freeda) | – | ✅ | ✅ | – | ✅ | – | ✅ | ✅ | – | – | – |
| [nf-core/reportho](https://github.com/nf-core/reportho) | – | ✅ | ✅ | – | ✅ | – | – | ◐ | – | – | – |
| [ConSurf](https://consurf.tau.ac.il/) | – | ✅ | ✅ | – | ◐ | – | – | ✅ | – | – | – |
| [PosiGene](https://github.com/gengit/PosiGene) | – | – | – | ✅ | ✅ | – | ✅ | – | – | – | ✅ |
| [PoSeiDon](https://github.com/rnajena/poseidon) / [AOC](https://joss.theoj.org/papers/10.21105/joss.09872) / [CAPHEINE](https://github.com/veg/CAPHEINE) / [VESPA](https://vespa-evol.readthedocs.io/) | – | – | – | – | ✅ | – | ✅ | – | – | – | ✅ |
| [fDOG](https://github.com/BIONF/fDOG) + [PhyloProfile](https://github.com/BIONF/PhyloProfile) | – | ◐ | ✅ | – | – | – | – | – | ◐ | – | ✅ |
| [PaGeSearch](https://pmc.ncbi.nlm.nih.gov/articles/PMC11216310/) | – | ◐ | ✅ | – | – | – | – | – | ◐ | ◐ | ◐ |
| [TOGA](https://github.com/hillerlab/TOGA) | – | – | – | ✅ | – | – | ◐ | – | ✅ | – | ◐ |
| [CLIME](https://www.gene-clime.org/) / [CladeOScope-GSA](https://pmc.ncbi.nlm.nih.gov/articles/PMC12898691/) | – | – | – | – | – | – | – | – | – | ✅ | – |
| [anvi'o](https://github.com/merenlab/anvio) / [kegg-pathways-completeness](https://github.com/EBI-Metagenomics/kegg-pathways-completeness-tool) | – | – | – | – | – | – | – | – | – | ◐ | ✅ |

Observações sobre a matriz:
- **OrthoGarden**: reads ou montagens → MEGAHIT → AUGUSTUS → OrthoFinder → IQ-TREE, em Nextflow, voltado a não-modelo. É praticamente o nosso **modo global** (sem seleção, estrutura ou vias).
- **DGINN**: a partir da CDS de um gene, busca homólogos no NCBI (nr/nt), atribui ortologia, faz alinhamento de códons, árvore, duplicação (Treerecs), recombinação (GARD) e seleção (HyPhy, PAML, Bio++). É praticamente o nosso **modo direcionado a partir de bancos**, sem estrutura nem reads.
- **FREEDA**: só o nome do gene → ortólogos em montagens não anotadas → seleção → resíduos mapeados na estrutura do AlphaFold, com interface gráfica para não especialistas. Mesmo argumento de "usuário que quer o ciclo completo", mas **restrito a um conjunto fixo de clados** (roedores, primatas, carnívoros, aves, moscas) e sem reads.
- **nf-core/reportho**: consenso de ortólogos de OMA, PANTHER, OrthoInspector e EggNOG para uma proteína, com alinhamento, árvore e estruturas do AlphaFold DB. Só espécies presentes nesses bancos.
- **Captus**: o mais completo para reads de vários tipos (captura, skimming, RNA-seq, WGS), com filtro de parálogos e alinhamento de códons; termina nos alinhamentos.
- **TOGA**: o único que classifica formalmente ausência real vs lacuna de montagem, mas exige montagem + alinhamento de genoma inteiro contra uma referência bem anotada (testado em mamíferos e aves).
- **CLIME / CladeOScope-GSA**: fazem a ideia central do módulo de vias, mas só sobre espécies e matrizes pré-calculadas.

## Anticorpos (validação biológica prevista)

| Ferramenta | O que faz |
|---|---|
| [IgDetective](https://github.com/Immunotools/IgDetective) ([artigo](https://pmc.ncbi.nlm.nih.gov/articles/PMC9248892/)) | anota genes V, D, J em montagens de genoma, inclusive em modo "cego" (sem referência), útil para espécies não-modelo |
| [Digger](https://williamdlees.github.io/digger/_build/html/index.html) | anotação detalhada de loci IG/TR (RSS, líder, funcional/ORF/pseudogene), mais dependente de referências |
| [Análise comparativa de loci imunes em 44 mamíferos](https://www.biorxiv.org/content/biorxiv/early/2025/04/06/2025.04.01.646651.full.pdf) (preprint 2025) | IgDetective modificado aplicado em escala para comparar loci entre espécies |
| AIRRflow / Immcantation | repertório expresso (AIRR-seq), não linhagem germinativa entre espécies |
| [ALIGaToR](https://pmc.ncbi.nlm.nih.gov/articles/PMC12190352/) (2025) | transfere anotações IMGT de uma montagem de referência para uma nova (V, D, J, C), detecta RSS, checa splicing e códons de parada; precisa de referência anotada |
| [CHfinder](https://www.biorxiv.org/content/10.1101/2020.05.21.108993v1.full.pdf) | rede neural que acha éxons de regiões constantes (IgM, IgD, IgT) em genomas de peixes; aplicado a 73 actinopterígios |

### Situação em vertebrados marinhos (busca complementar)

- Em peixes, os loci IG ainda são anotados **um a um, em grande parte à mão**: bacalhau do Atlântico ([2024](https://link.springer.com/article/10.1186/s12864-024-10571-0), integração manual no IGV), carpa-capim (IgT, 2025), IgNAR do tubarão-lixa ([2024](https://exa.ai/library/publication/t3mv8d8fvmz), com lacunas na montagem resolvidas realinhando reads). O artigo da carpa afirma que, entre mais de 30 mil espécies de teleósteos, o locus IgH foi anotado em poucas.
- **Organização diferente da de mamíferos**: tubarões e raias têm genes IG em **múltiplos clusters** (de ~10 a 100–200 miniloci V-D-J-C, cada um rearranjando internamente), e não no arranjo "translocon" de mamíferos. Teleósteos têm translocon, com IgT/Z antes de IgM/D, e cadeias leves em miniclusters. Ferramentas desenvolvidas e testadas em mamíferos (IgDetective, Digger) podem precisar de adaptação para clusters.
- Não foi encontrada uma comparação sistemática e automatizada de loci IG entre muitas espécies de vertebrados marinhos, equivalente à de 44 mamíferos.

Implicação para o pipeline: genes de imunoglobulina **não** são recuperados corretamente pelas etapas genéricas (Prodigal/BRAKER, HybPiper, OrthoFinder), porque os segmentos V/D/J são separados, repetitivos e com muitos parálogos parecidos. Validar com anticorpos exige um **módulo específico** (IgDetective/Digger sobre montagens) e montagens de boa qualidade nos loci IG. A busca não aprofundou se já existe comparação sistemática de loci IG em vertebrados marinhos (tubarões, raias, teleósteos); verificar na revisão formal.

## Análise de lacunas

Nenhuma ferramenta encontrada cobre o ciclo inteiro. As combinações mais próximas:
- **Gene-alvo**: DGINN (bancos → seleção) + FREEDA (seleção → estrutura). Juntos cobrem quase todo o modo direcionado, mas nenhum aceita reads nem espécies não-modelo arbitrárias com montagens próprias, e nenhum trata ausência.
- **Genoma inteiro**: OrthoGarden (reads → árvore) + NovelTree (reconciliação).
- **Vias**: CLIME / CladeOScope-GSA, presos a espécies pré-calculadas.

O que **parece** não existir (dentro desta busca):
1. Partir de **reads** (ou fontes mistas) de espécies não-modelo escolhidas pelo usuário até seleção + estrutura no mesmo fluxo.
2. **Ausência com nível de confiança a partir de reads** (genes-controle), alimentando uma matriz de presença/ausência.
3. **Módulos tipo CLIME sobre as espécies do próprio usuário**, em vez de espécies pré-calculadas.
4. Um módulo de **linhagem germinativa de anticorpos** integrado a análises evolutivas comparativas (seleção, estrutura) para espécies marinhas.

O que **não** é diferencial sozinho:
- "Ciclo completo para o usuário não especialista": o FREEDA já usa esse argumento.
- Encadear OrthoFinder + IQ-TREE + HyPhy: OrthoGarden, NovelTree, PosiGene, AOC já fazem.

## Implicações para o projeto

- O argumento do artigo deve ser **"espécies não-modelo a partir de reads, com ausência confiável e vias"**, não só "ciclo completo".
- No benchmark, comparar explicitamente com: DGINN e FREEDA (modo direcionado), OrthoGarden (modo global), Read2Tree e Captus (recuperação a partir de reads), CLIME (módulos).
- Reaproveitar em vez de reimplementar: avaliar chamar Captus ou GeneMiner para a recuperação a partir de reads, e AOC/HyPhy para seleção.

## Próximos passos (revisão formal)

1. **Bases**: PubMed, Scopus, Web of Science, bioRxiv; Google Scholar para literatura cinzenta.
2. **String de busca** (adaptar por base):
   `("pipeline" OR "workflow") AND ("phylogenomic*" OR "molecular evolution" OR "comparative genomic*") AND ("positive selection" OR "dN/dS" OR "gene loss" OR "presence/absence" OR "phylogenetic profil*" OR "pathway") AND ("non-model" OR "reads" OR "genome skimming" OR "target capture")`
3. **Busca por citações**: artigos que citam DGINN, FREEDA, OrthoGarden, NovelTree, Captus, Read2Tree, TOGA, CLIME, fDOG, IgDetective.
4. **Triagem** em duas etapas (título/resumo, depois texto completo), registrando exclusões, no formato PRISMA.
5. **Extração**: preencher esta matriz para cada ferramenta incluída.
