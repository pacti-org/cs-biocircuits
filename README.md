# A Pacti case study on specification-based synthetic biology 

Run the `specification_based_synthetic_biology.ipynb` to get started with this case study.

## Short description:

A case study on modeling the specifications of a biological circuit and speed up the experimental design process by finding optimal components to use from a library of parts. In the case study, we first build a characterized library of parts as assume-guarantee contracts using existing experimental data from the literature.With the use of _Pacti_, we demonstrate how scientists may describe the desired top-level behavior as contracts and then computationally choose from a library of available parts to ensure that the components meet the top-level system specification. For the engineered bacteria case study, we find the specification of the sensors that meet the top-level criteria on fold-change of the circuit response. Finally, we also show how we can find the specifications of missing parts in a system. In synthetic biology, it is common to have parts in the system for which no characterization data is available. Using quotient operation on contracts, we can find the constraints that this missing part must satisfy to meet the desired top-level criteria.

<img src="https://github.com/FormalSystems/media/blob/main/case_studies/biocircuit_specifications/main_figure.png?raw=true" alt= "Biocircuit Specifications Case Study Overview" width="700"/>

