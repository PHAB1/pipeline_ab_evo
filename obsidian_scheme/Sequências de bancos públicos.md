# Sequências de bancos públicos

Além das reads (SRA ou do usuário), o pipeline pode receber sequências já prontas de bancos públicos. Isso é comum e útil: amplia a amostragem de espécies sem precisar sequenciar ou montar nada. Mas essas sequências precisam passar por **curadoria** antes de entrar nas análises.

## Fontes

| Fonte | O que oferece | Observação |
|---|---|---|
| [NCBI Datasets](https://github.com/ncbi/datasets) | genomas montados, proteomas, CDS | preferir montagens RefSeq; já entra no modo global |
| RefSeq | proteínas e CDS curadas, não redundantes por organismo | melhor opção do NCBI para comparação |
| [UniProt](https://www.uniprot.org) | Swiss-Prot (curado manualmente), TrEMBL (automático), UniRef90/50 (já agrupado por identidade) | Swiss-Prot é ótimo como referência do gene-alvo |
| [OrthoDB](https://www.orthodb.org), [OMA](https://omabrowser.org) | ortólogos já agrupados entre muitas espécies | bom para montar referências do modo direcionado |
| nr (NCBI) | o maior conjunto de proteínas | útil para descobrir homólogos; exige curadoria pesada (abaixo) |
| PDB, AlphaFold DB | estruturas | para a etapa estrutural |

## Problemas do nr e como lidar

| Problema | Efeito | Mitigação |
|---|---|---|
| Redundância (muitas cepas e isolados quase idênticos) | domina o alinhamento e a árvore, deixa tudo lento | agrupar por identidade com [MMseqs2](https://github.com/soedinglab/MMseqs2) ou [CD-HIT](https://github.com/weizhongli/cdhit), ou manter 1 representante por espécie |
| Uma entrada pode valer para várias espécies | o nr junta sequências **idênticas** de organismos diferentes numa entrada só | expandir os cabeçalhos e atribuir a taxonomia de cada um ([TaxonKit](https://github.com/shenwei356/taxonkit)) |
| Viés taxonômico | organismos-modelo super-representados distorcem conservação e perfis | amostrar por táxon, não pelos melhores hits |
| Anotação errada propagada | nomes como "hypothetical protein" ou nomes transferidos por homologia errada | confiar na sequência, não no nome; confirmar ortologia pela árvore |
| Sequências parciais, fragmentos, pseudogenes, erros de predição | alinhamento ruim, falsos indels | filtrar por tamanho e cobertura do alinhamento com a referência; remover "partial"; preferir RefSeq |
| Montagens contaminadas | proteína de bactéria atribuída a um eucarioto, por exemplo | conferir se a sequência cai no lugar esperado da árvore |
| Parálogos misturados nos hits | árvore com cópias diferentes do gene | passar pelo OrthoFinder junto com o resto ou montar árvore com ortólogos de referência |
| Só proteína, sem CDS | impossível calcular dN/dS | recuperar a CDS pelo acesso da proteína ([Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/)); marcar as que ficarem sem CDS |
| Tamanho (centenas de GB) | inviável baixar tudo | BLAST remoto, ou DIAMOND contra subconjuntos (UniRef90, RefSeq) |
| Muda o tempo todo | resultado não reproduzível | registrar data, versão e acessos usados |

## Misturar dados próprios com públicos

- **Presença/ausência**: um gene "ausente" num proteoma baixado pode ser só anotação diferente. Para comparar vias e módulos, o ideal é baixar os **genomas** e passar todos pela mesma anotação do pipeline (mesmo ramo procarioto/eucarioto), ou pelo menos confirmar ausências com miniprot no genoma.
- **Mesma qualidade mínima**: aplicar BUSCO/CheckM2 também aos genomas públicos.

## Etapa de curadoria no pipeline

1. **Entrada**: lista de acessos, lista de táxons ou busca pelo gene (nome ou sequência).
2. **Download**: NCBI Datasets / Entrez Direct / UniProt.
3. **Redundância**: MMseqs2 ou CD-HIT.
4. **Filtros**: tamanho, cobertura em relação à referência, remoção de parciais.
5. **Taxonomia**: TaxonKit; expandir entradas multi-espécie do nr.
6. **CDS**: recuperar a sequência de nucleotídeos quando existir.
7. **Tabela de proveniência**: fonte, acesso, táxon, data do download, se tem CDS.

Saída: sequências curadas que entram na ortologia / [[Análises evolutivas]], e referências de vários táxons para o modo direcionado (ver "Cuidados do modo direcionado" em [[Análises evolutivas]]).
