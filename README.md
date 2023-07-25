# A model of the epistemic value of open-mindedness

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7989054.svg)](https://doi.org/10.5281/zenodo.7989054)

This repository is associated with a paper on the epistemic value of 
open-mindedness (under review). The paper investigates the conditions under which 
open-mindedness will be epistemically valuable. One of the central features of the 
analysis is that it represents an agent's competence and evaluative capacities using 
*gradual scales*. Another novel feature is that it starts with three realistic 
assumptions:
1. people are not perfectly competent in forming their own opinions,
2. people are not perfectly capable of evaluating the claims put forward by others, and
3. people can only give consideration to a limited number of arguments or opinions.

This repository contains code for computing the epistemic benefits of open-mindedness, 
and for creating the figures of the paper. These results are visualized as heatmaps 
such as:

[![One of the exemplary figures of the epistemic value of open-mindedness](/img/Figure_heatmap_source_evaluation_n4.png  "One of the exemplary figures of the 
epistemic value of open-mindedness")](https://github.com/HeinDuijf/OpenMind)

Although the paper only focuses on a limited area of the full parameter space, one 
can use (or extend) the repository to consider other areas of the parameter space. 

## 1. Setup
To run the project, you first need to install the required packages

```commandline
pip install -r requirements.txt
```

## 2. Usage
To create the figures, just run the main script:
```commandline
python main.py
```
A folder `new_figures` with figures will be created, which correspond to the figures 
in the paper.

## 3. Organization of the repository

### Accuracy calculations
The central calculations can be found in `accuracy_calculator.py`, which contains the 
central class `Agent`. The key function of the class is `accuracy_open_mind`, 
which calculates the accuracy of an agent with given parameter settings. 

### Figures
The scripts for creating the figures are in the folder `generate_figures`. The 
script `plot_functions.py` contains the global plotting functions and 
configurations; each of the other scripts corresponds to one or multiple figures. 

### Find tipping point evaluation content
One of the figures requires us to compute the tipping point where open-mindedness 
becomes epistemically beneficial above a given content evaluative capacity. The 
script to compute this tipping point can be found in 
`find_tipping_evaluation_content.py` and the corresponding function. 

## 4. Licence and citation
This repository accompanies an academic paper (under review). In the meantime, 
please cite the code as follows:

[How to cite](CITATION.cff): 
- [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7989054.svg)](https://doi.org/10.5281/zenodo.7989054)
- Duijf, H. (2023). A model of the epistemic value of open-mindedness (v1.0.0). 
Zenodo. https://doi.org/10.5281/zenodo.7989054.

Released under the [MIT licence](LICENCE.md).
