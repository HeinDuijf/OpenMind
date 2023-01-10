# Open mind

## To do 
-[ ] Opschonen: ongebruikte/oude folders en files verwijderen.
-[ ] Finalize "how to cite" and link in README
 
## Introduction
This project is associated with the paper titled *"When should one be open-minded?"* 
[link](). The paper investigates the conditions under which open-mindedness will be 
epistemically valuable. One of the novel features of the analysis is that it starts 
with some realistic assumptions: (1) people are not perfectly competent in forming their 
own opinions, (2) people are not perfectly capable of evaluating the claims put forward 
by others, and (3) people can only give consideration to a limited number of arguments 
or opinions.

This project contains code for computing the epistemic benefits of open-mindedness, 
and it contains code for creating the figures of the paper. 

Although the paper only focuses on a limited area of the full parameter space, one 
can use (or extend) the code to consider  other areas of the parameter space. 

## 1. Setup

To run the project, just run the main script:

```bash
python main.py
```

A folder `new_figures` with figures will be created, which correspond to the figures 
in the paper.

This project will require a Python environment:

```bash
python3 -m venv .venv # Or equivalent environment setup
source .venv/bin/activate  # Or equivalent environment setup
pip install -r requirements.txt
```

## 2. Project organization

### Accuracy calculations
The central calculations are in `accuracy_calculator.py`, which contains the 
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

## 3. How to cite
