Pyons Intro 

---

Main Components

- Inputs:  
  - Population   
  - Fitness Values   
- Outputs  
  - Next Generation/Population that will be created   
- Evolutionary Operations   
  - Duplication   
  - Crossover   
  - Mutation   
  - Random Replacement   
- Config Parameters  
  - Mutation Rate   
  - Crossover Rate   
  - Max epochs   
    - \# or None   
  - Indiv Count in population   
- Load / Save Results   
- Representation of Individuals (Indiv)  
  - Convert Indiv ←→ Genomes   
  - Valid values for each gene   
  - Serialize   
  - Deserialize  

---

Representation of Individuals 

- Need to have a way to convert object into genomes and then take genome and convert them back into original object  
- An individual should have a valid set of values for each gene   
- Need a way to Serialize and Deserialize to a file (JSON)   
- Default implementation provided will be a list individual and a network individual 

