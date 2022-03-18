# Assignment 3 EPA1352 readme

EPA1352 Group 6 

| Name    | Student Number |
|:-------:|:--------:|
| Ewout ter Hoeven  | 4493346 | 
| Zoë Huizing | 4660455 |
| Marlou Ceha | 4691539 |
| Christiaan Ouwehand | 4293053 |
| Timo Frazer | 4579992 |

## Introduction

The goal of this lab assignment is investigating critical road infrastructure in Bangladesh. This is done by calculating the delay for trucks driving on the N1, N2, and their N-class side roads longer than 25 km.

## Structure
The directory structure is listed below:

```
├───data            Contains all the input and interim data
├───img             Contains images, including the delay histogram
├───model           Contains the Mesa model iterated upon, including experiments and a benchmark
├───notebooks       Contains the Jupyter notebooks for EDA and analysis of both models
├───report          Contains the report written
├───results         Contains the results with average delay times and validation data
```
As seen above, two models have been developed for this assignment, a Mesa model with NetworkX component needed for the shortest path algorithm in a multiple road network. The [report](report/Report-EPA1352-G06-A3.pdf) discusses the results of the travel time due to potential bridge delay. 

## How to Use the MESA model 

The model will be run based on the (data/A3_data_clean.csv) file. This can be changed in the [model.py](model/model.py) file. To do so change the data_path in the model class to the desired file.

The model itself is defined in [model.py](model/model.py) and the components used in the model are defined in the [components.py](model/components.py) file. In this file the network graph and shortest path algorythme is made. The statistical distribution of delay times is defined in [triangular_function.py](model/triangular_function.py).

A few other files are available for conveniently interacting with the model:
 - The model can be visualised with [model_viz.py](model/model_viz.py) file.
 - To the run the different scenario's, [experiments.py](model/experiments.py) is used.
 - Note: to run the moddel faster, all the print functions are commented.



# step 2: Running simulation with above generated data in MESA

The simulation is automatically run for all 5 scenarios with 10 replications each and the output is also saved in to a CSV defined in the model_run.py file.

The simulation run csv can be found in the experiment folder. 

# Step 3: Processing the output files in Jupyter Notebook to get results 

The results are visalized in a Jupyter Notebook called [notebooks/A3_analysis.ipynb]  