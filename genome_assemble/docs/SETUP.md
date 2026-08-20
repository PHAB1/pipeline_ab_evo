# Preparar o computador

Abra este arquivo **no GitHub** (no navegador) para ver o texto formatado.

Este fluxo roda em **Linux**. No Windows, use o **WSL** (Windows Subsystem for Linux). O genoma da levedura é pequeno, então um PC de iniciação científica dá conta — só precisa de espaço em disco e um pouco de RAM livre.

Antes de começar, confira se há **pelo menos 10 a 15 GB livres**. Os FASTQs, os arquivos temporários do MEGAHIT e o cache do SRA Toolkit ocupam espaço.

---

## Windows: instalar o WSL

1. Abra o **PowerShell como administrador** (botão direito no menu Iniciar → *Windows PowerShell (Admin)* ou *Terminal (Admin)*).
2. Rode:

```powershell
wsl --install
```

3. **Reinicie** o computador quando o Windows pedir.
4. Na primeira abertura do Ubuntu, escolha um nome de usuário e uma senha (a senha não aparece enquanto você digita — isso é normal).
5. Atualize os pacotes:

```bash
sudo apt update && sudo apt upgrade -y
```

Pronto: a partir daqui, todos os comandos deste repositório são no terminal do Ubuntu (WSL), não no PowerShell.

### Se o PC tiver pouca RAM (4 GB)

O Windows + WSL + Chrome + MEGAHIT juntos pesam. Na hora da montagem:

- feche o navegador e outros programas
- se mesmo assim travar, use um computador do laboratório

---

## Instalar o Miniconda (Linux ou WSL)

O Conda cria ambientes isolados com as ferramentas de bioinformática, sem bagunçar o sistema.

```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Aceite a licença, confirme o local padrão e, no final, responda **yes** para inicializar o conda.

Feche e abra o terminal. Você deve ver `(base)` no início da linha. Confira:

```bash
conda --version
```

Se o comando não for encontrado:

```bash
source ~/miniconda3/etc/profile.d/conda.sh
conda init bash
```

Feche e abra o terminal de novo.

---

## Clonar este repositório

```bash
cd ~
git clone https://github.com/SEU_USUARIO/SEU_REPO.git
cd SEU_REPO
```

Troque `SEU_USUARIO/SEU_REPO` pelo link que você recebeu. Se preferir SSH e já tiver chave configurada:

```bash
git clone git@github.com:SEU_USUARIO/SEU_REPO.git
```

---

## Criar os ambientes conda

Na pasta do repositório:

```bash
conda env create -f envs/preprocess.yml
conda env create -f envs/assemble.yml
```

A primeira vez demora (baixa os programas). Quando terminar:

```bash
conda activate euk_preprocess
fasterq-dump --version
fastp --version
fastqc --version

conda activate euk_assemble
megahit --version
quast.py --version
```

Se `conda activate` reclamar, rode `conda init bash`, reabra o terminal e tente de novo.

---

## Espaço em disco e cache do SRA

O SRA Toolkit às vezes guarda cache em `~/.ncbi`. Se o disco encher no meio do download, apague o cache antigo e tente de novo:

```bash
du -sh ~/.ncbi data results 2>/dev/null
```

Com **10 a 15 GB livres** você costuma ficar tranquila nesta amostra.

---

Quando o setup estiver ok, vá para o **[tutorial](TUTORIAL.md)**.
