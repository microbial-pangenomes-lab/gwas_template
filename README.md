# Snakemake workflow: Bacterial GWAS

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

    git clone --recursive https://github.com/microbial-pangenomes-lab/gwas_template.git MyGWAS
    cd MyGWAS

Save your phenotype table as a tab-separated file as `data/data.tsv`.
The first column should contain the sample names, and subsequent columns should
contain the target phenotype(s). Additional columns are allowed and will be simply ignored.

Edit the `params` section of the `config/config.yaml` file (at the top), and indicate the name
of the phenotypes to be used in the association(s) (i.e. edit the `targets` variable).
Also change the mlst scheme to be used to compute lineages and the name of the references to be used
for annotation of hits. For convenience the defaults for E. coli are placed as defaults, and those
for P. aeruginosa are commented.

Create a symbolic links to a copy of the Uniref50 protein fasta file, changing the following command
to the actual PATH to that file on your system:

    ln -s /storage/datasets/uniprot/uniref50.fasta data/uniref50.fasta

Tip: the file [can be downloaded from this page](https://www.uniprot.org/help/downloads) ([direct link to the file](https://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz))

Also create a symbolic link to the directory in which the databases for eggnog-mapper have been placed:

    ln -s /fast-storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/ data/eggnog-mapper

Note: the above path would likely be different in your system. The best way to get these files is to install
`eggnog-mapper` using a `conda` environment and then use the `download_eggnog_data.py` command.

Place your genome assemblies in the `data/gffs` and `data/fastas` directories. The files should be named
`SAMPLE.gff` and `SAMPLE.fasta`, respectively, and the sample names should match those in the phenotype file
(i.e. `data/data.tsv`).

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

    snakemake -p annotate_summary panfeed map_back heritability enrichment qq_plots tree --cores 24 --use-conda --conda-frontend mamba
    
The following example instead uses "vanilla" `conda` and skips the generation of the phylogenetic tree:

    snakemake -p annotate_summary panfeed map_back heritability enrichment qq_plots --cores 24 --use-conda

## Outputs

TBD

## TODO

- [ ] Add the ability to use covariates in the associations
- [ ] manhattan_plot.py : handle cases in which the reference genome has more than one chromosome (either because it has plasmids or because it is a draft genome)
- [ ] Easily switch to poppunk for lineage computation
- [ ] Combine all annotations in a series of webpages
- [ ] Add references to the tools used in the pipeline
- [ ] Use random file names for things that go in `/tmp` to avoid conflicts
- [ ] Use `/tmp` directories (as implemented by snakemake) to be efficient in I/O heavy rules
- [ ] Delete everything but the necessary files upon completion of a rule
- [ ] Avoid rules that list each input file as it might eventually become too long (including the current use of the `data/fastas` and `data/gffs` directories)
- [ ] Run QC on phenotypic data/genomes as part of bootstrapping
- [ ] Use snakemake resources system to budget memory requirements
- [ ] Swap sift4g for [more modern alternatives](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-02948-3)
- [ ] Create a minimal test set that yields some hits and runs in reasonable time
- [ ] Also generate panfeed plots
- [ ] Harden panfeed rules against stochastic gzip file corruption
- [ ] Swap `unitig-counter` for `bifrost`
- [ ] Heritability estimates using different distributions (i.e. for binary phenotypes the normal distribution is likely not appropriate?)

## Reference

TBD

## Author

Marco Galardini (marco.galardini@twincore.de)
