# Exercício: os mistérios do genoma

Abra este arquivo **no GitHub** (no navegador) para ver o texto formatado. Os comandos você cola no terminal.

Você virou detetive. Chegaram sequências misteriosas, uma mensagem escondida dentro de uma proteína, nove organismos sem nome e, no fim, um contig muito estranho na **sua** montagem.

Em cada fase tem um script em `alinhamento/exercicio/scripts/` com lacunas marcadas como `TODO`. Complete os `TODO`s, rode, e anote o que descobriu em `alinhamento/exercicio/RESPOSTAS.md`.

Antes de começar, leia **[ALINHAMENTO.md](ALINHAMENTO.md)**: tudo o que você precisa usar está lá e nos scripts de `alinhamento/demo/`.

---

## Pontuação

| Fase | Pontos | Bônus |
|------|--------|-------|
| 1. Detetive do BLAST | 60 | +15 |
| 2. A mensagem secreta | 30 | +10 |
| 3. Quem é quem? | 45 | +15 |
| 4. Chefão: o contig estranho | 50 | +10 |
| **Total** | **185** | **+50** |

| Pontos | Nível |
|--------|-------|
| até 90 | Estagiária de bancada |
| 91–150 | Detetive de genomas |
| 151–185 | Sherlock Holmes do DNA |
| 186+ | Darwin aprovaria |

---

## 0. Preparar

```bash
git pull
conda env create -f envs/align.yml    # só na primeira vez
conda activate euk_align
mkdir -p results/blast

# banco BLAST com os contigs da SUA montagem
makeblastdb \
  -in results/assembly/SRR35893457_megahit/final.contigs.fa \
  -dbtype nucl \
  -out results/blast/contigs
```

Para a fase 4 você vai precisar da referência S288C. Se já fez a seção 8 do tutorial de montagem, ela está em `data/reference/S288C.fa`. Se não:

```bash
mkdir -p data/reference

# curl -L: segue redirecionamentos; -o: nome do arquivo de saída
curl -L -o data/reference/S288C.fna.gz \
  "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.fna.gz"
gunzip -c data/reference/S288C.fna.gz > data/reference/S288C.fa
```

**Atenção:** os nomes dos contigs (`k141_...`) da sua montagem podem ser diferentes dos de outra pessoa. Isso é normal; o que importa é o tamanho, a cobertura (`multi`) e a identidade.

---

## Fase 1: Detetive do BLAST (60 pts)

Em `alinhamento/exercicio/dados/misterios.fasta` há **6 sequências de DNA** (`misterio_1` a `misterio_6`). Cada uma é **uma** destas (em ordem alfabética, **não** na ordem dos mistérios):

- actina humana (gene *ACTB*)
- actina da própria levedura (gene *ACT1*)
- *COX3* (gene do DNA mitocondrial)
- *GAL1* (via da galactose)
- rRNA 18S (gene ribossomal, fica no rDNA)
- uma sequência **inventada** (não existe na natureza)

Sua missão: descobrir quem é quem **só com BLAST e cobertura**, sem procurar as sequências na internet.

**Script:** `alinhamento/exercicio/scripts/fase1_detetive_blast.py` (TODO 1 e TODO 2)

```bash
# rode com os dois modos e compare
python alinhamento/exercicio/scripts/fase1_detetive_blast.py megablast
python alinhamento/exercicio/scripts/fase1_detetive_blast.py blastn
```

Para os mistérios que continuarem difíceis, tente o BLAST **traduzido** direto no terminal. Exemplo com o `misterio_5`:

```bash
# separa um mistério num arquivo só dele (seqkit não está no euk_align, então usamos Python)
python -c "
from Bio import SeqIO
SeqIO.write([r for r in SeqIO.parse('alinhamento/exercicio/dados/misterios.fasta', 'fasta') if r.id == 'misterio_5'], 'results/blast/misterio_5.fasta', 'fasta')
"

# tblastx: traduz query e banco nos 6 quadros de leitura e compara as proteínas
tblastx \
  -query results/blast/misterio_5.fasta \
  -db results/blast/contigs \
  -outfmt "6 qseqid sseqid pident length evalue bitscore" \
  -evalue 1e-10 | sort -k6,6gr | head
```

**Pistas**

- Lembra do `multi` na aula de montagem? ~60 é uma cópia por genoma. E se der **mil**? E **quatro mil**?
- Um gene de **outra espécie** não é idêntico, mas também não é aleatório.
- Uma sequência inventada não acha nada, **nem** com o modo mais sensível, **nem** traduzida.

**Perguntas** (responda em `RESPOSTAS.md`)

1. Quantos mistérios o `megablast` achou? E o `-task blastn`? Por que a diferença? (10)
2. Qual mistério cai num contig com `multi` perto de 1000? E perto de 4000? O que isso diz sobre esses contigs? (15)
3. Qual mistério não acha nada de jeito nenhum? (5)
4. Um mistério cai no **mesmo contig** que outro, mas com identidade bem menor. No `tblastx`, a identidade sobe muito. Por que a identidade em **aminoácidos** é maior que em **nucleotídeos**? (15)
5. Complete a tabela de identificação em `RESPOSTAS.md`. (15)

**Bônus (+15):** no `tblastx` do `misterio_5` aparece um **segundo** contig com ~50% de identidade. O que ele pode ser? (Dica: genes também têm "primos" dentro do mesmo genoma.)

```bash
git add -A
git commit -m "fase 1: detetive do BLAST"
git push
```

---

## Fase 2: A mensagem secreta (30 pts)

Alguém pegou a actina (`actina_original.fasta`), trocou **alguns aminoácidos** pelas letras de uma palavra e salvou como `actina_misteriosa.fasta`. Para atrapalhar, também **apagou um aminoácido** em algum lugar.

**Script:** `alinhamento/exercicio/scripts/fase2_mensagem_secreta.py` (TODO 3, 4 e 5)

```bash
python alinhamento/exercicio/scripts/fase2_mensagem_secreta.py
```

**Perguntas**

1. A "comparação ingênua" (letra por letra) encontra quantas diferenças? Por que dá tão errado? (5)
2. Qual é a mensagem? Em que posições da actina original estão as letras? (15)
3. Em que posição está o aminoácido apagado? (5)
4. Alinhe o `fragmento.fasta` com a actina nos modos global e local. Compare os scores. Qual modo faz sentido para a pergunta "onde está esse pedaço?" e por quê? (5)

**Bônus (+10):** quem é a pessoa da mensagem e o que ela tem a ver com alinhamento de sequências de espécies diferentes?

```bash
git add -A
git commit -m "fase 2: mensagem secreta"
git push
```

---

## Fase 3: Quem é quem? (45 pts)

`citocromo_c.fasta` tem a proteína **citocromo c** de 9 organismos, renomeados de `Organismo_A` a `Organismo_I`. A lista (em ordem alfabética) é:

> Arabidopsis (planta), atum, camundongo, cavalo, chimpanzé, galinha, humano, levedura, mosca-da-fruta

**Script:** `alinhamento/exercicio/scripts/fase3_quem_e_quem.py` (TODO 6 a 9 e bônus)

```bash
python alinhamento/exercicio/scripts/fase3_quem_e_quem.py
```

**Pistas**

1. Duas espécies da lista são tão próximas que o citocromo c delas é **idêntico**.
2. Tirando esse par, o organismo mais parecido com ele é o **roedor**.
3. O mais parecido com o roedor é o **cavalo**.
4. Entre os vertebrados, o **peixe** é o mais distante dos mamíferos.
5. A **planta** é a mais distante de todos, e tem a sequência mais comprida.
6. Para o resto, use a árvore e o que você sabe de evolução.

**Perguntas**

1. Preencha a tabela de `Organismo_A` a `Organismo_I` em `RESPOSTAS.md` (5 pts cada). (45)
2. Dá para saber com certeza qual dos dois idênticos é qual? Por quê?

**Bônus (+15):**

- (+10) Quantas colunas são **iguais nos 9** organismos? Procure no resultado o padrão `C x x C H` (C, duas letras quaisquer, C, H). Pesquise: para que serve esse trecho no citocromo c?
- (+5) A árvore bate com o que você sabe da evolução desses organismos? Aponte um lugar onde ela **não** bate e pense por que uma árvore de **um gene só** pode errar.

```bash
git add -A
git commit -m "fase 3: quem é quem"
git push
```

---

## Fase 4: Chefão: o contig estranho (50 pts)

Na fase 1, um dos genes da levedura caiu nos seus contigs com identidade **bem mais baixa** do que deveria para a própria espécie. Estranho, não? Vamos olhar o contig **inteiro**.

```bash
# banco BLAST do genoma de referência (uma vez só)
makeblastdb -in data/reference/S288C.fa -dbtype nucl -out results/blast/s288c
```

**Script:** `alinhamento/exercicio/scripts/fase4_chefao.py` (TODO 10, 11 e 12)

```bash
# troque k141_XXX pelo contig em que esse gene caiu na fase 1
python alinhamento/exercicio/scripts/fase4_chefao.py k141_XXX
```

Abra a figura `results/alinhamento/chefao.png`.

**Perguntas**

1. Descreva a figura: a identidade com a S288C é igual ao longo do contig todo? (10)
2. Em que cromossomo e em que posições da S288C fica o trecho diferente? Descubra **quais genes** estão lá: procure essas coordenadas no [SGD](https://www.yeastgenome.org/) (JBrowse) ou no [NCBI Genome Data Viewer](https://www.ncbi.nlm.nih.gov/gdv/). Os cromossomos da referência têm nomes como `NC_001134.8`; o próprio arquivo diz qual é qual: `grep ">" data/reference/S288C.fa`. (15)
3. Se a cepa tivesse **perdido** esses genes, como seria a figura? E se fosse um erro de montagem? Por que nenhuma dessas explicações parece certa aqui? (10)
4. Proponha uma hipótese biológica para esse trecho tão diferente no meio de um cromossomo "normal". (15)

**Bônus (+10):** se você alinhasse as **reads** dessa cepa na S288C (como na seção 9 do tutorial, com `bwa`), essa região apareceria quase **sem cobertura**, como se os genes não existissem. Explique por quê, e por que a montagem *de novo* não tem esse problema.

```bash
git add -A
git commit -m "fase 4: chefão"
git push
```

---

## Para entregar

- Os 4 scripts completos em `alinhamento/exercicio/scripts/`
- `alinhamento/exercicio/RESPOSTAS.md` preenchido
- Tudo com `git push`
