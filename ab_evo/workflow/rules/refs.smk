REFS = config["references"]


def target_param(gene, key, default=None):
    return config["targets"][gene].get(key, default)


rule fetch_refs:
    output:
        faa="results/referencias/{gene}.faa",
        seed="results/referencias/{gene}.semente.faa",
        tsv="results/referencias/{gene}.tsv",
    params:
        seed=lambda w: target_param(w.gene, "seed"),
        names=lambda w: target_param(w.gene, "names", [w.gene]),
        fasta=lambda w: target_param(w.gene, "fasta"),
        taxon=lambda w: target_param(w.gene, "taxon", REFS.get("taxon")),
        exclude=REFS.get("exclude_taxa", []),
        max_per_gene=REFS["max_per_gene"],
        min_per_gene=REFS["min_per_gene"],
        min_identity=REFS["min_identity"],
        min_seed_coverage=REFS["min_seed_coverage"],
    localrule: True
    conda:
        "../envs/python.yml"
    script:
        "../scripts/fetch_refs.py"


rule download_busco:
    output:
        variants=f"resources/busco/{LINEAGE}/ancestral_variants",
    params:
        lineage=LINEAGE,
    localrule: True
    conda:
        "../envs/python.yml"
    script:
        "../scripts/download_busco.py"


rule build_targets:
    input:
        refs=expand("results/referencias/{gene}.faa", gene=GENES),
        seeds=expand("results/referencias/{gene}.semente.faa", gene=GENES),
        busco=rules.download_busco.output.variants,
    output:
        targets="results/alvos/targets.faa",
        roles="results/alvos/papeis.tsv",
    params:
        genes=GENES,
        n_genes=config["controls"]["n_genes"],
        variants_per_gene=config["controls"]["variants_per_gene"],
        random_seed=config["controls"]["random_seed"],
        max_score_per_res=0.5,
    conda:
        "../envs/python.yml"
    script:
        "../scripts/build_targets.py"
