# Ramos eucarioto e procarioto

Depois da montagem (ou do download de montagens prontas), o pipeline se divide conforme o tipo de organismo. A diferença principal está na **predição de genes**: eucariotos têm íntrons, repetições e genes espalhados, e as ferramentas de procarioto não lidam com isso.

## Antes de dividir

- **Usar montagens existentes sempre que possível**: [NCBI Datasets](https://github.com/ncbi/datasets). Montar genomas de muitas espécies a partir do SRA é caro; só montar quando não houver montagem disponível.
- **Avaliar a montagem**: [QUAST](https://github.com/ablab/quast) (contiguidade, Nx, GC). Ver [[Controle de qualidade]].

## Procarioto

| Etapa | Ferramenta | Observação |
|---|---|---|
| Completude e contaminação | [CheckM2](https://github.com/chklovski/CheckM2) | obrigatório: tamanho total muito acima do esperado para a espécie pode indicar contaminação |
| Predição de genes | [Prodigal](https://github.com/hyattpd/Prodigal) | rápido, sem íntrons |
| Anotação completa | [Bakta](https://github.com/oschwengers/bakta) ou [Prokka](https://github.com/tseemann/prokka) | já roda a predição de genes e gera CDS + proteínas |
| Pangenoma | [Panaroo](https://github.com/gtonkinhill/panaroo), [PPanGGOLiN](https://github.com/labgem/PPanGGOLiN) | genes do núcleo vs acessórios; útil quando há várias linhagens da mesma espécie |
| Filogenômica rápida | [GToTree](https://github.com/AstrobioMike/GToTree) | árvore de espécies com genes marcadores de cópia única |
| Transferência horizontal (HGT) | [HGTector](https://github.com/qiyunzhu/HGTector) | HGT é comum em procariotos e distorce árvores de genes |

## Eucarioto

| Etapa | Ferramenta | Observação |
|---|---|---|
| Completude | [BUSCO](https://gitlab.com/ezlab/busco) | também serve como medida da qualidade da anotação |
| Mascarar repetições | [RepeatModeler](https://github.com/Dfam-consortium/RepeatModeler) + [RepeatMasker](https://www.repeatmasker.org) | fazer antes da predição de genes (soft-masking) |
| Predição de genes | [BRAKER3](https://github.com/Gaius-Augustus/BRAKER) | melhor com RNA-seq e/ou proteínas de espécies próximas como evidência |
| Predição sem evidência | [Helixer](https://github.com/weberlab-hhu/Helixer) | deep learning, não precisa de RNA-seq |
| Proteína-alvo → genoma | [miniprot](https://github.com/lh3/miniprot) | alinha proteínas conhecidas ao genoma respeitando íntrons; ótimo para o modo direcionado |

## Saída comum aos dois ramos

Os dois ramos precisam entregar **proteoma + CDS (nucleotídeos)** de cada espécie. A CDS é necessária para as análises de seleção (dN/dS); só a proteína não basta. Daqui segue para [[Análises evolutivas]] e [[Módulo de vias e grafos]].
