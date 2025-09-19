rule all:
  input: "results/final_table.rds"

runs = ["ERR188021","ERR188088","ERR188288","ERR188297","ERR188329","ERR188356"]

def getInput(wildcards):  
  files = []
  for s in runs:
    files = files + ["views/"+s+"/quant.sf"]
  return files

rule final_table:
  input: getInput
  output: "results/final_table.rds"
  shell: "Rscript -e 'rmarkdown::render(\"scripts/DEseq.Rmd\")'"

docker = "docker run --rm --platform linux/amd64 --user $(id -u):59560 \
          -v $(pwd):$(pwd) -w $(pwd)"
  
rule quantify:
  input: "views/{run}.bam"
  output: "views/{run}/quant.sf"
  params: 
    salmon = docker + "  hadrieng/salmon:0.13.1 salmon "
  shell: "{params.salmon} quant -t data/gencode.v48.transcripts.fa -l IU \
  -a {input} -o views/{wildcards.run}"
          
rule convert:
  input: "views/{run}.sam"
  output: "views/{run}.bam"
  params: 
    samtools = docker + " biocontainers/samtools:v1.9-4-deb_cv1 samtools "
  shell: "{params.samtools} view -S -b {input} > {output}"
    
rule mapping:
  input: "data/{run}_1.fastq.gz"
  output: "views/{run}.sam"
  params: 
    minimap2 = docker + " biocontainers/minimap2:v2.15dfsg-1-deb_cv1 minimap2 "
  shell: "{params.minimap2} -ax sr data/gencode.v48.transcripts.fa \
          {input} > {output}"
