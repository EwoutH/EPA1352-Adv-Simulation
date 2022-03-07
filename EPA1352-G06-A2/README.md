# Assignment 2 EPA1352 readme

EPA1352 Group 6 

| Name    | Student Number |
|:-------:|:--------:|
| Ewout ter Hoeven  | 4493346 | 
| Zoë Huizing | 4660455 |
| Marlou Ceha | 4691539 |
| Christiaan Ouwehand | 4293053 |
| Timo Frazer | 4579992 |

## Introduction

The goal of this lab exercises is to analyse the transportation delays and its economic impact due to breakdown of bridges on the N1 from Chittagong to Dhaka in Bangladesh. For that, a Mesa module 0.9.0 with Python 3.10 will be used to generate trucks driving every 5 minutes from the beginning to the end of the road crossing bridges that could break under different probabilistic scenarios. To compare these results, a minimal stochastic model will be made.

## Structure
The directory structure is listed below:

```
├───data            Contains all the input and interim data
├───img             Contains images, including the delay histogram
├───minimal_model   Contains minimal model, created from scatch, including a benchmark and validation
├───model           Contains the Mesa model iterated upon, including experiments and a benchmark
├───notebooks       Contains the Jupyter notebooks for EDA and analysis of both models
├───report          Contains the report written
├───results         Contains the results with average delay times and validation data
```
As seen above, two models have been developed for this assignment, a Mesa model based on the given model and a model developed from scratch called the minimal model. The [report](report/Report-EPA1352-G06-A2.pdf) discusses the differences between the two.

## How to Use the MESA model 

The model will be run based on the [simulation_file_N1.csv](data/simulation_file_N1.csv) file. This can be changed in the [model.py](model/model.py) file. To do so change the data_path in the model class to the desired file.

The model itself is defined in [model.py](model/model.py) and the components used in the model are defined in the [components.py](model/components.py) file. The statistical distribution of delay times is defined in [triangular_function.py](model/triangular_function.py).

A few other files are available for conveniently interacting with the model:
 - The model can be visualised with [model_viz.py](model/model_viz.py) file.
 - To the run the different scenario's, [experiments.py](model/experiments.py) is used.
 - To test the performance of the Mesa model, [benchmark.py](model/benchmark.py).

## How to Use the self written model

The self-written model developed from scratch is defined in a single file, [minimal.py](minimal_model/minimal.py). Including imports, comments, whitelines and it's about 100 lines of code, making it relatively easy to comphrenend.

The delay time results were validated with [validation.py](minimal_model/validation.py) and the performance can be tested in [benchmarks.py](minimal_model/benchmark.py).
