"""Baixa uma linhagem do BUSCO e extrai as sequências ancestrais (proteína)."""

import tarfile
import tempfile
import urllib.request
from pathlib import Path

BASE = "https://busco-data.ezlab.org/v5/data"


def main(sm):
    lineage = sm.params.lineage
    out = Path(sm.output.variants)
    out.parent.mkdir(parents=True, exist_ok=True)

    versions = urllib.request.urlopen(f"{BASE}/file_versions.tsv", timeout=60).read().decode()
    date = next(l.split("\t")[1] for l in versions.splitlines() if l.split("\t")[0] == lineage)

    with tempfile.TemporaryDirectory() as tmp:
        tgz = Path(tmp) / f"{lineage}.tar.gz"
        urllib.request.urlretrieve(f"{BASE}/lineages/{lineage}.{date}.tar.gz", tgz)
        with tarfile.open(tgz) as tar:
            for name in ("ancestral_variants", "dataset.cfg"):
                member = tar.getmember(f"{lineage}/{name}")
                with tar.extractfile(member) as src, open(out.parent / name, "wb") as dst:
                    dst.write(src.read())


main(snakemake)  # noqa: F821
