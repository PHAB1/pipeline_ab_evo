# Análises evolutivas

Entrada: proteoma + CDS de cada espécie (ver [[Ramos eucarioto e procarioto]]) ou genes-alvo extraídos no modo direcionado.

## Por que não basta comparar com o nr

BLAST/DIAMOND contra o nr dá **similaridade e anotação**, não evolução:

- o melhor hit muitas vezes não é o parente mais próximo (Koski & Golding, 2001), porque linhagens evoluem em taxas diferentes;
- não distingue **ortólogo** (mesmo gene em espécies diferentes) de **parálogo** (cópia por duplicação);
- o nr é redundante e enviesado para organismos-modelo.

O nr serve como ponto de partida para coletar homólogos; a análise evolutiva vem depois.

## Escala da análise e resolução

| Escala | Responde bem | Limitação |
|---|---|---|
| Um alvo em espécies escolhidas | história da proteína: seleção, sítios, perda/ganho | poucos sítios informativos; árvore do gene pode discordar da árvore de espécies |
| Muitos genes, muitas espécies (global) | árvore de espécies robusta, famílias gênicas | caro; dilui o sinal da proteína de interesse |
| Combinação | árvore do alvo lida **sobre** a árvore de espécies | é o objetivo do pipeline |

A **amostragem de táxons** (quais espécies entram) costuma pesar mais na resolução que o número de genes. Incluir sempre um **grupo externo** (outgroup) para enraizar a árvore.

## Etapas

### 1. Ortologia
- [OrthoFinder](https://github.com/davidemms/OrthoFinder): grupos de ortólogos, árvores de genes, árvore de espécies e eventos de duplicação.

### 2. Alinhamento
- [MAFFT](https://gitlab.com/sysimm/mafft) para proteínas.
- Alinhamento de códons para as análises de seleção: [MACSE](https://www.agap-ge2pop.org/macse/) ou [PAL2NAL](https://www.bork.embl.de/pal2nal/) (projeta o alinhamento de proteína na CDS).
- Limpeza de colunas mal alinhadas: [trimAl](https://github.com/inab/trimal) ou [ClipKIT](https://github.com/JLSteenwyk/ClipKIT).

### 3. Árvores
- Árvore de genes: [IQ-TREE 2](https://github.com/iqtree/iqtree2) (ModelFinder para escolher o modelo, UFBoot para suporte).
- Árvore de espécies: concatenação de ortólogos de cópia única no IQ-TREE, ou [ASTRAL/ASTER](https://github.com/chaoszhang/ASTER) a partir das árvores de genes (lida melhor com discordância entre genes).

### 4. Reconciliação árvore de gene × árvore de espécies
- [GeneRax](https://github.com/BenoitMorel/GeneRax): infere duplicações, perdas e transferências horizontais explicando por que a árvore do gene difere da de espécies.

### 5. Reconstrução de sequências ancestrais
- [IQ-TREE 2](https://github.com/iqtree/iqtree2) com `--ancestral`, ou [PAML](https://github.com/abacus-gene/paml).
- Infere a sequência mais provável em cada nó interno da árvore e permite mapear **em qual ramo cada mutação aconteceu**.

### 6. Seleção natural (precisa de CDS)
- [HyPhy](https://github.com/veg/hyphy):
  - **aBSREL**: quais ramos sofreram seleção positiva;
  - **MEME** / **FUBAR**: quais sítios estão sob seleção;
  - **RELAX**: seleção relaxada ou intensificada num grupo de espécies.
- [PAML](https://github.com/abacus-gene/paml) (`codeml`) como alternativa clássica.

### 7. Evolução de famílias gênicas
- [CAFE5](https://github.com/hahnlab/CAFE5): expansão e contração do número de cópias ao longo da árvore.

### 8. Estrutura
- Predição: [ESM](https://github.com/facebookresearch/esm), [LocalColabFold](https://github.com/YoshitakaMo/localcolabfold).
- Comparação: [Foldseek](https://github.com/steineggerlab/foldseek), [US-align](https://github.com/pylelab/USalign).
- Árvore estrutural: [FoldTree](https://github.com/DessimozLab/fold_tree). Útil em divergências profundas, quando a sequência já saturou; em comparações próximas a árvore de sequência tem mais resolução. Recebe **estruturas**, não sequências.
- Projetar na estrutura os sítios sob seleção (etapa 6) e as mutações por ramo (etapa 5).

## Inferir intermediários ("Z veio de X?")

Se X parece com Y, Z parece com Y, mas X não parece com Z, isso sugere que Y está "no meio", mas a filogenia **não diz que uma espécie atual veio de outra atual**. Todas são pontas da árvore; o que se infere são os **ancestrais comuns** (nós internos).

- Com a árvore **enraizada** (outgroup), dá para saber a ordem das divergências e a direção das mudanças.
- A **reconstrução ancestral** dá a sequência provável de cada ancestral e em qual ramo cada mutação surgiu.
- Similaridade ≠ parentesco: Y pode parecer "intermediário" só por evoluir mais devagar (ramo curto), mantendo o estado ancestral.

Casos em que "Z veio de X" faz sentido literalmente:
- **Transferência horizontal**: o gene de Z foi adquirido da linhagem de X (GeneRax, HGTector).
- **Duplicação**: Z é uma cópia (parálogo) de X no mesmo genoma (OrthoFinder, GeneRax).

## Cuidados do modo direcionado

No modo direcionado as reads são recrutadas direto contra a sequência de referência do gene-alvo, sem montar o genoma inteiro. Isso elimina o problema de montagem global, mas o resultado ainda pode enganar:

| Problema | Efeito | Mitigação |
|---|---|---|
| Cobertura baixa ou viés de GC | nenhuma read cai no gene por acaso: **falsa ausência** | estimar a cobertura esperada (tamanho do genoma × profundidade) e usar genes-controle (abaixo) |
| Referência distante da espécie | as reads não alinham: **falsa ausência** ou gene parcial | busca em nível de proteína (DIAMOND/BLASTX é mais sensível que nucleotídeo); várias referências de táxons diversos por gene; recrutamento iterativo (aTRAM) |
| Parálogos e pseudogenes | reads de outra cópia são recrutadas: **cópia errada ou sequência quimérica** | checagem de parálogos (HybPiper avisa); árvore do gene com ortólogos conhecidos |
| Contaminação | reads de outro organismo dão hit: **falsa presença** | conferir a taxonomia da sequência recuperada (DIAMOND contra o nr); sem contexto genômico isso é mais difícil que no modo global |
| Recuperação parcial | só os trechos conservados são recuperados | reportar a % do gene recuperada; genes muito parciais atrapalham alinhamento e dN/dS |

O HybPiper e o aTRAM ainda fazem uma **montagem local** com as reads recrutadas de cada gene. É uma montagem pequena e bem mais fácil, mas não é zero.

### Genes-controle

Incluir sempre, junto com os alvos, um conjunto de genes conservados de cópia única (ex.: genes do BUSCO do grupo). Eles medem se a amostra tem cobertura suficiente para confiar numa ausência:

| Genes-controle | Gene-alvo | Conclusão |
|---|---|---|
| recuperados, boa cobertura | completo | presente |
| recuperados, boa cobertura | parcial | presente, mas incompleto ou divergente |
| recuperados, boa cobertura | ausente | **provável ausência real** |
| poucos ou nenhum | ausente | **inconclusivo** (falta cobertura) |

### Entrada por nome do gene

Se o usuário passar só o nome, o pipeline precisa buscar as sequências de referência (ex.: UniProt, OrthoDB, OMA). Nomes de genes são ambíguos (sinônimos, parálogos com nomes parecidos, nomes diferentes entre grupos), então:
- buscar ortólogos de vários táxons, não uma sequência só;
- mostrar ao usuário o que foi encontrado para confirmação antes de rodar.

## Ferramentas que já fazem partes disso

Para comparar com o pipeline (benchmark):
- [Read2Tree](https://github.com/DessimozLab/read2tree): árvores direto das reads, sem montagem. Concorrente direto do modo direcionado.
- [HybPiper](https://github.com/mossmatters/HybPiper) e [aTRAM](https://github.com/juliema/aTRAM): extração de genes-alvo a partir das reads.
- [GToTree](https://github.com/AstrobioMike/GToTree), filogenômica com BUSCO, OrthoFinder: modo global.

## Ideias do DGINN para incorporar

O [DGINN](https://github.com/leapicard/DGINN) (Snakemake) faz quase a mesma parte evolutiva do modo direcionado, mas a partir de bancos do NCBI. Decisão por enquanto: **não integrar** (contêiner, versões antigas, nomes no formato `Genero_especie_GENE_Id`); usar as ideias e comparar com ele no benchmark. Retomar quando chegar nessa parte.

- **Recombinação antes da seleção**: recombinação dentro do gene gera falsos positivos de seleção positiva. Rodar o GARD ([HyPhy](https://github.com/veg/hyphy)) e, se houver, analisar cada bloco separadamente.
- **Entrar no meio do pipeline**: permitir começar com CDS de ortólogos, alinhamento ou árvore já prontos.
- **Vários métodos de seleção**: o DGINN roda BUSTED, MEME, PAML e Bio++ e resume tudo num arquivo. Na validação deles, os modelos de sítio do Bio++ com taxa constante deram o melhor equilíbrio entre resultado e tempo.
- **Filtro de sequências longas demais**: descartar as maiores que um fator × a mediana, ou acima do terceiro quartil + fator × IQR.
- **Validação com genes de história conhecida**: eles usaram 19 genes de primatas já estudados. Serve de modelo para o nosso benchmark.
