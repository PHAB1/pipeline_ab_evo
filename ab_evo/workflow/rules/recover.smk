def reads(w):
    if config["qc"]:
        return {
            "r1": f"results/qc/{w.sample}_1.fastq.gz",
            "r2": f"results/qc/{w.sample}_2.fastq.gz",
        }
    return {"r1": SAMPLES.loc[w.sample, "r1"], "r2": SAMPLES.loc[w.sample, "r2"]}


rule fastp:
    input:
        r1=lambda w: SAMPLES.loc[w.sample, "r1"],
        r2=lambda w: SAMPLES.loc[w.sample, "r2"],
    output:
        r1="results/qc/{sample}_1.fastq.gz",
        r2="results/qc/{sample}_2.fastq.gz",
        html="results/qc/{sample}.fastp.html",
        json="results/qc/{sample}.fastp.json",
    threads: config["threads"]
    conda:
        "../envs/fastp.yml"
    log:
        "logs/fastp/{sample}.log",
    shell:
        "fastp -i {input.r1} -I {input.r2} -o {output.r1} -O {output.r2} "
        "-h {output.html} -j {output.json} -w {threads} 2> {log}"


rule hybpiper_assemble:
    input:
        unpack(reads),
        targets=rules.build_targets.output.targets,
    output:
        done="results/hybpiper/{sample}/genes_with_seqs.txt",
    threads: config["threads"]
    conda:
        "../envs/hybpiper.yml"
    log:
        "logs/hybpiper/{sample}.log",
    shell:
        "hybpiper assemble -t_aa {input.targets} -r {input.r1} {input.r2} "
        "--prefix {wildcards.sample} --diamond --cpu {threads} "
        "--output_folder results/hybpiper > {log} 2>&1"
