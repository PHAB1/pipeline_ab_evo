# Estado da arte

Revisão mais completa, com matriz de cobertura e análise de lacunas: [[Revisão de escopo]].

Ferramentas publicadas que já fazem partes (às vezes grandes) do que o pipeline propõe. Antes de investir em código, fazer uma revisão sistemática a partir daqui e posicionar o pipeline em relação a cada uma.

## Busca direcionada de genes e presença/ausência

| Ferramenta | O que faz | Entrada exigida | Limitação para o nosso caso |
|---|---|---|---|
| [fDOG](https://github.com/BIONF/fDOG) + [PhyloProfile](https://github.com/BIONF/PhyloProfile) | a partir de uma proteína-semente, busca ortólogos em milhares de espécies (perfil HMM), compara arquitetura de domínios e gera o perfil de presença/ausência ([artigo](https://pmc.ncbi.nlm.nih.gov/articles/PMC12198962/)) | proteomas (e montagens, no modo fDOG-Assembly) | não trabalha direto com reads |
| [PaGeSearch](https://pmc.ncbi.nlm.nih.gov/articles/PMC11216310/) | acha os genes de uma via (Reactome) em genomas não anotados e filtra ortólogos prováveis | montagens; treinado para mamíferos, **peixes**, aves e plantas | precisa de montagem |
| [Read2Tree](https://github.com/DessimozLab/read2tree) | árvores direto das reads usando ortólogos do OMA | reads | foco em árvore, não em presença/ausência nem vias |
| [HybPiper](https://github.com/mossmatters/HybPiper), [aTRAM](https://github.com/juliema/aTRAM) | recupera genes-alvo das reads | reads + referências | sem chamada formal de ausência |
| [PAV-spotter](https://www.biorxiv.org/content/10.1101/2024.10.25.620064v4) | presença/ausência em dados de captura direcionada, sem genoma de referência | reads de captura | compara classes de amostras, não espécies |

## Ausência real vs artefato

| Ferramenta / abordagem | O que faz |
|---|---|
| [TOGA / TOGA2](https://github.com/hillerlab/TOGA) ([Science 2023](https://www.science.org/doi/10.1126/science.abn3107)) | classifica genes como intactos, **perdidos** ou **faltando** (lacunas de montagem); gera alinhamentos de códons. Precisa de montagem + alinhamento de genoma inteiro contra uma referência bem anotada |
| Cobertura normalizada por gene (pangenomas de arroz, mexilhão) | mapeia reads e chama presença pela cobertura do gene relativa à cobertura esperada do genoma; é a mesma lógica dos nossos genes-controle |
| [GenAPI](https://github.com/MigleSur/GenAPI) | presença/ausência em montagens fragmentadas de bactérias |

## Módulos de genes por coevolução (o "grafo de vias")

| Ferramenta | O que faz | Limitação |
|---|---|---|
| [CLIME](https://www.gene-clime.org/) ([artigo](https://pmc.ncbi.nlm.nih.gov/articles/PMC4171950/)) | recebe árvore de espécies + conjunto de genes + matriz de presença/ausência; divide o conjunto em **módulos evolutivos** e expande cada módulo com novos genes | matrizes pré-calculadas para 10 organismos-modelo; usar espécies próprias exige montar a matriz |
| [CladeOScope-GSA](https://pmc.ncbi.nlm.nih.gov/articles/PMC12898691/) | perfis filogenéticos normalizados em 1905 eucariotos; acha submódulos que coevoluem dentro de um conjunto de genes, por clado | web, centrado em genes humanos e espécies pré-calculadas |
| [STRING](https://string-db.org) | rede de associação com coocorrência, vizinhança, literatura etc. | uma espécie por vez |

## Completude de vias

| Ferramenta | O que faz |
|---|---|
| [kegg-pathways-completeness](https://github.com/EBI-Metagenomics/kegg-pathways-completeness-tool) | completude de módulos KEGG a partir de KOs, com os módulos já convertidos em grafos |
| [anvi'o](https://github.com/merenlab/anvio) | completude de módulos KEGG por genoma |
| [Prolipipe](https://peerj.com/articles/21453/) | presença/ausência de vias metabólicas em milhares de genomas bacterianos |
| Seq2Fun / ExpressAnalyst | reads de RNA-seq de espécies não-modelo direto para contagens por grupo de ortólogos, sem montagem |

## Onde ainda pode haver espaço

Cada ferramenta acima exige algo que espécies marinhas não-modelo muitas vezes não têm (proteoma, montagem boa, referência próxima bem anotada) ou fica presa a espécies pré-calculadas. A lacuna possível é **integrar** essas abordagens para as espécies do próprio usuário, a partir de reads ou fontes mistas, até módulos tipo CLIME. Isso é uma contribuição de integração e usabilidade, não um método novo, e precisa ser confirmada com uma revisão sistemática.
