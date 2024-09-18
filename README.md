# bio-agents-curation-agenting

The repo collect scripts and agents for aiding in the curation of new agents, e.g. coming from Pub2Agents and EdamMapper


## Tutorials

The file _workflow_tutorial.ipynb_ includes a detailed tutorial on how to implement the workflow after running Pub2Agents for a specific month (see [Running Pub2Agents for one month](#running-pub2agents-for-one-month).
The workflow takes the output log from Pub2Agents, separate json files with low-priority agents and preprints as input (json files under folder **data**.


## Pub2Agents

### Installation

1. In your working directory, create a folder named "Pub2Agents". 
2. Follow the installation guide at [Install Pub2Agents](https://github.com/bio-agents/pub2agents/blob/develop/INSTALL.md).

### Running Pub2Agents for one month

1. Create folder named _month_year_
2. Copy the following command and replace the folder name /work/Pub2Agents/MONTH_YEAR and month argument YYYY_MM

```
    java -jar -Xms2048M -Xmx4096M /work/Pub2Agents/pub2agents/target/pub2agents-cli-1.1.2-SNAPSHOT.jar -all /work/Pub2Agents/MONTH_YEAR --edam http://edamontology.org/EDAM.owl --idf https://github.com/edamontology/edammap/raw/master/doc/bioagents.idf --idf-stemmed https://github.com/edamontology/edammap/raw/master/doc/bioagents.stemmed.idf --month YYYY-MM --seleniumFirefox /work/Pub2agents/firefox/firefox/firefox-bin
```

Usually this takes 4-5 hours to finish.

