# Exercício de alinhamento de sequências

Abra este arquivo **no GitHub** (no navegador) para ver o texto formatado. Os comandos você cola no terminal.

O exercício tem quatro partes, que aplicam o conteúdo de **[ALINHAMENTO.md](ALINHAMENTO.md)** aos dados da sua montagem:

1. Identificação de sequências com BLAST
2. Alinhamento par a par: global e local
3. Alinhamento múltiplo e filogenia do citocromo c
4. Um contig com divergência regional em relação à referência

Cada parte tem um script em `alinhamento/exercicio/scripts/` com trechos marcados como `TODO`. Complete os `TODO`s, rode e registre resultados e respostas em `alinhamento/exercicio/RESPOSTAS.md`. Os scripts de `alinhamento/demo/` têm tudo o que é preciso para completar os `TODO`s.

---

## 0. Preparação

```bash
git pull
conda env create -f envs/align.yml    # só na primeira vez
conda activate euk_align
mkdir -p results/blast

# banco BLAST com os contigs da sua montagem
makeblastdb \
  -in results/assembly/SRR35893457_megahit/final.contigs.fa \
  -dbtype nucl \
  -out results/blast/contigs
```

A parte 4 usa a referência S288C. Se você fez a seção 8 do tutorial de montagem, ela já está em `data/reference/S288C.fa`. Se não:

```bash
mkdir -p data/reference

# curl -L: segue redirecionamentos; -o: nome do arquivo de saída
curl -L -o data/reference/S288C.fna.gz \
  "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.fna.gz"
gunzip -c data/reference/S288C.fna.gz > data/reference/S288C.fa
```

Os nomes dos contigs (`k141_...`) da sua montagem podem ser diferentes dos de outra pessoa. O que importa é o tamanho, a cobertura (`multi`) e a identidade.

---

## Parte 1: Identificação de sequências com BLAST

O arquivo `alinhamento/exercicio/dados/desconhecidas.fasta` tem **6 sequências de DNA** (`seq_1` a `seq_6`). Cada uma corresponde a um item desta lista, em ordem alfabética e não na ordem das sequências:

- actina humana (gene *ACTB*)
- actina de levedura (gene *ACT1*)
- *COX3* (gene do DNA mitocondrial)
- *GAL1* (via da galactose)
- rRNA 18S (gene ribossomal, no rDNA)
- uma sequência artificial, que não existe na natureza

Identifique cada sequência usando apenas BLAST contra os seus contigs e a cobertura dos contigs, sem buscar as sequências em bancos externos.

**Script:** `alinhamento/exercicio/scripts/parte1_blast.py` (TODO 1 e 2)

```bash
# rode nos dois modos e compare
python alinhamento/exercicio/scripts/parte1_blast.py megablast
python alinhamento/exercicio/scripts/parte1_blast.py blastn
```

Para as sequências que continuarem sem identificação, use o BLAST **traduzido**. Exemplo com a `seq_5`:

```bash
# separa uma sequência num arquivo próprio (o seqkit não está no euk_align, então usamos Python)
python -c "
from Bio import SeqIO
SeqIO.write([r for r in SeqIO.parse('alinhamento/exercicio/dados/desconhecidas.fasta', 'fasta') if r.id == 'seq_5'], 'results/blast/seq_5.fasta', 'fasta')
"

# tblastx: traduz query e banco nos 6 quadros de leitura e compara as proteínas
tblastx \
  -query results/blast/seq_5.fasta \
  -db results/blast/contigs \
  -outfmt "6 qseqid sseqid pident length evalue bitscore" \
  -evalue 1e-10 | sort -k6,6gr | head
```

**Observações**

- O `multi` no cabeçalho do contig é a cobertura. Na sua montagem, ~60 corresponde a uma cópia por genoma.
- Um gene de outra espécie não é idêntico ao da levedura, mas a semelhança também não é aleatória.
- Uma sequência artificial não tem hit significativo em nenhum modo, nem traduzida.

**Questões**

1. Quantas sequências o `megablast` encontrou? E o `-task blastn`? Explique a diferença.
2. Qual sequência cai num contig com `multi` perto de 1000? E perto de 4000? O que isso indica sobre esses contigs?
3. Qual sequência não tem hit em nenhum modo?
4. Uma sequência cai no **mesmo contig** que outra, mas com identidade bem menor. No `tblastx`, a identidade sobe bastante. Por que a identidade em **aminoácidos** é maior que em **nucleotídeos**?
5. Complete a tabela de identificação em `RESPOSTAS.md`.
6. No `tblastx` da `seq_5` aparece um **segundo** contig com ~50% de identidade. O que ele pode ser?

```bash
git add -A
git commit -m "parte 1: identificação com BLAST"
git push
```

---

## Parte 2: Alinhamento par a par, global e local

`actina_modificada.fasta` é a actina de `actina_original.fasta` com **algumas substituições** e **uma deleção** de um aminoácido. As letras usadas nas substituições formam uma palavra, o que permite conferir o resultado.

**Script:** `alinhamento/exercicio/scripts/parte2_pairwise.py` (TODO 3, 4 e 5)

```bash
python alinhamento/exercicio/scripts/parte2_pairwise.py
```

**Questões**

1. Quantas diferenças a comparação posição a posição, sem alinhar, encontra? Por que o resultado está errado?
2. Quais são as substituições (posição na actina original, aminoácido original e novo)? Que palavra elas formam?
3. Em que posição está o aminoácido deletado?
4. Alinhe `fragmento.fasta` com a actina nos modos global e local. Compare os scores. Qual modo é adequado para a pergunta "onde está esse trecho?" e por quê?
5. Por que faz sentido alinhar sequências de espécies diferentes? Relacione com a palavra encontrada.

```bash
git add -A
git commit -m "parte 2: alinhamento par a par"
git push
```

---

## Parte 3: Alinhamento múltiplo e filogenia do citocromo c

`citocromo_c.fasta` tem a proteína **citocromo c** de 9 organismos, identificados apenas por letras (`Organismo_A` a `Organismo_I`). Os organismos são, em ordem alfabética:

> Arabidopsis (planta), atum, camundongo, cavalo, chimpanzé, galinha, humano, levedura, mosca-da-fruta

**Script:** `alinhamento/exercicio/scripts/parte3_filogenia.py` (TODO 6 a 9 e colunas conservadas)

```bash
python alinhamento/exercicio/scripts/parte3_filogenia.py
```

**Informações para a atribuição**

1. Duas espécies da lista têm citocromo c **idêntico**.
2. Excluindo esse par, o organismo mais próximo dele é o **roedor**.
3. O mais próximo do roedor é o **cavalo**.
4. Entre os vertebrados, o **peixe** é o mais distante dos mamíferos.
5. A **planta** é a mais distante de todos e tem a sequência mais longa.
6. Para os demais, use a árvore e o que se sabe sobre a evolução desses grupos.

**Questões**

1. Atribua cada sequência (`Organismo_A` a `Organismo_I`) a um organismo na tabela de `RESPOSTAS.md`, justificando com as distâncias e a árvore.
2. É possível saber qual das duas sequências idênticas é de qual espécie? Por quê?
3. Quantas colunas são **iguais nos 9** organismos? Localize o motivo `C x x C H` (C, duas letras quaisquer, C, H). Qual é a função desse trecho no citocromo c?
4. A árvore é compatível com a evolução conhecida desses organismos? Aponte um ponto em que ela **não** é, e explique por que a árvore de **um único gene** pode divergir da árvore das espécies.

```bash
git add -A
git commit -m "parte 3: alinhamento múltiplo e filogenia"
git push
```

---

## Parte 4: Um contig com divergência regional

Na parte 1, um dos genes de levedura teve identidade **bem mais baixa** do que o esperado para a própria espécie. Nesta parte, você compara o **contig inteiro** em que ele caiu com a referência S288C.

```bash
# banco BLAST do genoma de referência (uma vez só)
makeblastdb -in data/reference/S288C.fa -dbtype nucl -out results/blast/s288c
```

**Script:** `alinhamento/exercicio/scripts/parte4_contig.py` (TODO 10, 11 e 12)

```bash
# troque k141_XXX pelo contig em que esse gene caiu na parte 1
python alinhamento/exercicio/scripts/parte4_contig.py k141_XXX
```

Abra a figura `results/alinhamento/contig_vs_s288c.png`.

**Questões**

1. Descreva a figura: a identidade com a S288C é uniforme ao longo do contig?
2. Em que cromossomo e em que posições da S288C fica o trecho divergente? Quais genes estão nele? Procure as coordenadas no [SGD](https://www.yeastgenome.org/) (JBrowse) ou no [NCBI Genome Data Viewer](https://www.ncbi.nlm.nih.gov/gdv/). Os cromossomos da referência têm nomes como `NC_001134.8`; para ver qual é qual: `grep ">" data/reference/S288C.fa`.
3. Se a cepa tivesse **perdido** esses genes, como seria a figura? E se fosse um erro de montagem? Por que essas explicações não se aplicam aqui?
4. Proponha uma hipótese biológica para um trecho tão divergente no meio de um cromossomo com identidade de 97–99% no restante.
5. Se você alinhasse as **reads** dessa cepa na S288C com o `bwa` (seção 9 do tutorial), essa região apareceria quase **sem cobertura**, como se os genes não existissem. Explique por quê, e por que a montagem *de novo* não tem esse problema.

```bash
git add -A
git commit -m "parte 4: contig com divergência regional"
git push
```

---

## Entrega

- Os 4 scripts completos em `alinhamento/exercicio/scripts/`
- `alinhamento/exercicio/RESPOSTAS.md` preenchido
- Tudo enviado com `git push`
