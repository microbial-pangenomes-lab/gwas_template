# Snakemake workflow: Bacterial GWAS

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12685497.svg)](https://doi.org/10.5281/zenodo.12685497)
[![Documentation Status](https://readthedocs.org/projects/microgwas/badge/?version=latest)](https://microgwas.readthedocs.io/en/latest/?badge=latest)

A battery included snakemake pipeline to run bacterial GWAS on a set of assembled genomes.
Multiple phenotypes can be defined and used for the associations.

For each phenotype, the pipeline will run associations using 5 sets of genetic variants:

* individual unitigs
* gene presence/absence
* rare variants (i.e. gene burden test)
* gene cluster specific k-mers
* all unitigs combined (i.e. whole genome machine learning model)

For each set of genetic variants a number of downstream analyses will be run to provide
annotated results and functional enrichments.

It will additionally compute the heritability of each phenotype using
the lineage information and the whole set of unitigs.

It can also optionally compute a phylogenetic tree of all samples.

## Quick start

Make a copy of this repository (optionally you can first create a new repository by clicking on the "Use this template" button
from Github's interface), including the submodules:

    git clone --recursive https://github.com/microbial-pangenomes-lab/microGWAS.git microGWAS
    cd microGWAS

Save your phenotype table as a tab-separated file as `data/data.tsv`.
The first column should contain the sample names, then there should be two columns
listing the relative or absolute path to the assemblies (`fasta`, SAMPLE.fasta) and annotations (`gff`, SAMPLE.gff),
and subsequent columns should
contain the target phenotype(s). Additional columns are allowed and will be simply ignored.
An example file can be found in the `test` directory (`test/data.tsv`).

Edit the `params` section of the `config/config.yaml` file (at the top), and indicate the name
of the phenotypes to be used in the association(s) (i.e. edit the `targets` variable).
Also change the mlst scheme to be used to compute lineages and the name of the references to be used
for annotation of hits. For convenience the defaults for E. coli are placed as defaults, and those
for P. aeruginosa are commented.

Create a symbolic link to the directory in which the databases for eggnog-mapper have been placed:

    ln -s /fast-storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/ data/eggnog-mapper

Note: the above path would likely be different in your system. The best way to get these files is to install
`eggnog-mapper` using a `conda` environment and then use the `download_eggnog_data.py` command.

Create and activate a `conda` environment to run the bootstrapping script and the pipeline (named `microGWAS`, can be skipped if it's already present):

    conda env create -f environment.yml
    conda activate microGWAS

Then run the bootstrapping script to populate the input files for the pipeline and download the reference genomes
used for annotation of hits and the rare variants analyses. The following example works for E. coli (and downloads the references listed by default in `config/config.yaml`):

    bash bootstrap.sh Escherichia coli IAI39 GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1 

And the following works for P. aeruginosa (and matches the references commented in `config/config.yaml`):

    bash bootstrap.sh Pseudomonas aeruginosa UCBPP-PA14 GCF_000006765.1,GCF_000014625.1 

You are now ready to run the full pipeline! The following example runs all the analyses using 24 cores and `mamba` as the conda backend
to install each environment:

    snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree --cores 24 --verbose --use-conda --conda-frontend mamba
    
The following example instead uses "vanilla" `conda` and skips the generation of the phylogenetic tree:

    snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots --cores 24 --verbose --use-conda


## Testing

We have included a small dataset in order to test the pipeline in reasonable time
and resources. In its current state continuous integration (CI) in the cloud is not feasible
because certain rules require significant time and resources to complete (`annotate_reference`,
`get_snps`). Some workarounds might be added in the future to bypass those rules. In the meantime the
tests can be run on a decent laptop with 8 cores and at least ~10Gb RAM in a few hours.

The test dataset has been created from that [used in a mouse model of bloodstream infection]().

To run the tests, prepare a symbolic link to the eggnog-mapper
databases (as explained above), then do the following:

    cd test
    bash run_tests.sh

The script will prepare the input files, run the bootstrapping script, then run snakemake twice,
first in "dry" mode, and then "for real".

Please note that the only rule that is not tested is the one estimating lineages (`lineage_st`), as the
test dataset is a reduced part of the E. coli genome.

## TODO

- [x] Add the ability to use covariates in the associations
- [ ] manhattan_plot.py : handle cases in which the reference genome has more than one chromosome (either because it has plasmids or because it is a draft genome) ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/8))
- [ ] Easily switch to poppunk for lineage computation
- [ ] Combine all annotations in a series of webpages ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/6))
- [x] Add references to the tools used in the pipeline ([documentation issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/7))
- [x] Use random file names for things that go in `/tmp` to avoid conflicts
- [ ] Use `/tmp` directories (as implemented by snakemake) to be efficient in I/O heavy rules
- [ ] Delete everything but the necessary files upon completion of a rule
    - [x] snippy
    - [x] panaroo
- [x] Avoid rules that list each input file as it might eventually become too long (including the current use of the `data/fastas` and `data/gffs` directories)
- [ ] Run QC on phenotypic data/genomes as part of bootstrapping
- [ ] Use snakemake resources system to budget memory requirements ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/9))
- [x] Swap sift4g for [more modern alternatives](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-02948-3) ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/10))
- [x] Create a minimal test set that yields some hits and runs in reasonable time (~300 Ecoli dataset from BSI mouse model)
- [x] Also generate panfeed plots, and annotate its results
- [x] Harden panfeed rules against stochastic gzip file corruption ([fixed here](https://github.com/microbial-pangenomes-lab/microGWAS/pull/1))
- [ ] Swap `unitig-counter` for `bifrost` or `cuttlefish` ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/11))
- [ ] Heritability estimates using different distributions (i.e. for binary phenotypes the normal distribution is likely not appropriate?)
- [x] Add [abritamr](https://github.com/MDU-PHL/abritamr) to detect known AMR/VAGs - necessary for this pipeline???
- [x] Add txt file that describes outputs produced from running the pipeline (in progress)
- [X] Add documentation using something like read the docs

## Reference

    Burgaya, J., Damaris, B. F., Fiebig, J., & Galardini, M. (2024). microGWAS: A computational pipeline to perform large scale bacterial genome-wide association studies (p. 2024.07.08.602456). bioRxiv. https://doi.org/10.1101/2024.07.08.602456

## Used tools

- unitig-counter: [10.1371/journal.pgen.1007758](10.1371/journal.pgen.1007758) and [10.1128/mbio.01344-20](10.1128/mbio.01344-20)
- mlst: [https://doi.org/10.12688/wellcomeopenres.14826.1](https://doi.org/10.12688/wellcomeopenres.14826.1)
- abritamr: [10.1038/s41467-022-35713-4](10.1038/s41467-022-35713-4)
- mash: [10.1186/s13059-016-0997-x](10.1186/s13059-016-0997-x)
- panaroo: [10.1186/s13059-020-02090-4](10.1186/s13059-020-02090-4)
- fasttree: [10.1371/journal.pone.0009490](10.1371/journal.pone.0009490)
- snp-sites: [10.1099/mgen.0.000056](10.1099/mgen.0.000056)
- snippy: [https://github.com/tseemann/snippy](https://github.com/tseemann/snippy)
- bcftools: [10.1093/gigascience/giab008](10.1093/gigascience/giab008)
- limix: [10.1101/003905](10.1101/003905)
- ALBI: [10.1016/j.ajhg.2016.04.016](10.1016/j.ajhg.2016.04.016)
- sequence_unet: [10.1186/s13059-023-02948-3](10.1186/s13059-023-02948-3)
- pyseer: [10.1093/bioinformatics/bty539](10.1093/bioinformatics/bty539) and [10.1101/852426](10.1101/852426)
- bwa: [arXiv:1303.3997](https://arxiv.org/abs/1303.3997)
- bedtools: [10.1093/bioinformatics/btq033](10.1093/bioinformatics/btq033) and [10.1093/bioinformatics/btr539](10.1093/bioinformatics/btr539)
- eggnog-mapper: [10.1093/molbev/msx148](10.1093/molbev/msx148)
- panfeed: [10.1099/mgen.0.001129](10.1099/mgen.0.001129)

## Author

Marco Galardini (marco.galardini@twincore.de)
