# Exercício de alinhamento de sequências

Guarde seus scripts em `alinhamento/exercicio/scripts/`, as figuras em `alinhamento/exercicio/figuras/` e as respostas em `alinhamento/exercicio/respostas.md`. Faça `git add`, `git commit` e `git push` ao fim de cada parte.

---

## Parte 1: Localizar genes na montagem com BLAST

O arquivo `alinhamento/exercicio/dados/genes.fasta` tem 6 sequências de DNA, cada uma com o nome no cabeçalho:

- `ACT1_levedura`: actina de levedura
- `ACTB_humana`: actina humana (mRNA)
- `COX3_levedura`: gene do DNA mitocondrial
- `GAL1_levedura`: galactoquinase, via da galactose
- `RDN18_levedura`: rRNA 18S, no rDNA
- `artificial`: sequência artificial, que não existe na natureza (controle negativo)

Localize cada gene nos contigs da sua montagem, `results/assembly/SRR35893457_megahit/final.contigs.fa`, e extraia do contig a sequência homóloga. O cabeçalho de cada contig tem `multi` (cobertura) e `len` (tamanho); na sua montagem, `multi` ~60 corresponde a uma cópia por genoma.

**Ferramentas**

- `makeblastdb` cria o banco a partir dos contigs:
  - `-in`: o FASTA dos contigs
  - `-dbtype nucl`: banco de nucleotídeos
  - `-out`: prefixo dos arquivos do banco; use `results/blast/contigs`
  
- `blastn` busca os genes no banco:
  - `-query`: `alinhamento/exercicio/dados/genes.fasta`
  - `-db`: `results/blast/contigs`
  - `-task`: `megablast` (padrão, só acha quase idêntico) ou `blastn` (mais sensível)
  - `-outfmt "6 ..."`: tabela; escolha as colunas, por exemplo `qseqid sseqid pident length qcovs evalue bitscore sstart send` (`sstart` e `send` são o início e o fim do hit no contig)
  - `-evalue`: limite de e-value (ex.: `1e-5`)
  - `-max_target_seqs`: quantos contigs reportar por gene
  
- `tblastx` tem as mesmas entradas do `blastn`, mas traduz a query e o banco nos 6 quadros de leitura e compara as proteínas.

- Biopython:
  - `SeqIO.parse` lê os FASTAs; `multi` e `len` estão em `rec.description`
  - `rec.seq[inicio:fim]` recorta um trecho (em Python a posição começa em 0)
  - `.reverse_complement()` dá a fita complementar reversa

Salve as saídas do BLAST em `results/blast/` e as sequências homólogas em `alinhamento/exercicio/homologos.fasta`.

**Questões**

1. Quantos genes o `megablast` encontra? E o `-task blastn`? Por que a diferença?
2. Por que a sequência `artificial` não tem hit?
3. Os contigs de `COX3_levedura` e `RDN18_levedura` têm `multi` perto de 1000 e de 4000. Por quê?

---

## Parte 2: Alinhamento par a par, global e local

`alinhamento/exercicio/dados/actina_modificada.fasta` é a actina de `alinhamento/exercicio/dados/actina_original.fasta` com algumas substituições e uma deleção de um aminoácido. As letras das substituições formam uma palavra.

**Ferramentas (Biopython)**

- `SeqIO.read` lê um FASTA com uma sequência só.

- `PairwiseAligner`:
  - `.mode`: `"global"` ou `"local"`
  - `.substitution_matrix`: `substitution_matrices.load("BLOSUM62")`
  - `.open_gap_score` e `.extend_gap_score`: penalidades de gap (ex.: `-10` e `-0.5`)
  - `.align(seq1, seq2)[0]`: o melhor alinhamento; `aln[0]` e `aln[1]` são as duas linhas com gaps, `aln.score` é o score e `aln.aligned` dá as posições alinhadas

O modelo está em `alinhamento/demo/02_pairwise.py`.

**Questões**

1. Alinhe as duas actinas. Que palavra as substituições formam?
2. Em que posição está o aminoácido deletado?
3. Alinhe `alinhamento/exercicio/dados/fragmento.fasta` com a actina original nos modos global e local. Qual modo serve para achar onde o fragmento está? Por quê?

---

## Parte 3: Alinhamento múltiplo e filogenia do citocromo c

`alinhamento/exercicio/dados/citocromo_c.fasta` tem o citocromo c de 9 organismos, identificados só por letras (`Organismo_A` a `Organismo_I`). Os organismos são, em ordem alfabética:

> Arabidopsis (planta), atum, camundongo, cavalo, chimpanzé, galinha, humano, levedura, mosca-da-fruta

Informações para a atribuição:

1. Duas espécies da lista têm citocromo c idêntico.
2. Excluindo esse par, o organismo mais próximo dele é o roedor.
3. O mais próximo do roedor é o cavalo.
4. Entre os vertebrados, o peixe é o mais distante dos mamíferos.
5. A planta é a mais distante de todos e tem a sequência mais longa.
6. Para os demais, use a árvore e o que se sabe sobre a evolução desses grupos.

**Ferramentas**

- `mafft` faz o alinhamento múltiplo:
  - entrada: `alinhamento/exercicio/dados/citocromo_c.fasta`
  - `--auto`: escolhe a estratégia sozinho
  - a saída vai para a tela (stdout); redirecione para `results/alinhamento/citocromo_c.aln.fasta`
  
- Biopython:
  - `AlignIO.read(arquivo, "fasta")` lê o alinhamento; `msa[:, i]` devolve a coluna `i`
  - `DistanceCalculator("identity").get_distance(msa)`: matriz de distâncias
  - `DistanceTreeConstructor().nj(matriz)`: árvore Neighbor-Joining
  - `arvore.root_at_midpoint()`: enraíza no ponto médio
  - `Phylo.draw_ascii(arvore)` e `Phylo.draw(...)` desenham a árvore; salve a figura em `alinhamento/exercicio/figuras/`

O modelo está em `alinhamento/demo/03_msa_arvore.py`.

**Questões**

1. Qual par de organismos tem a menor distância? E a maior?
2. Atribua cada sequência a um organismo.
3. No alinhamento, localize o motivo `C x x C H` (C, duas letras quaisquer, C, H). Por que ele é igual em todos?

---
