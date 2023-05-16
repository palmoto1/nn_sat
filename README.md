# NN-SAT
### Authors: August Johnson Palm & Ludvig Warpe

## Introduction
This repository contains the implementation of an experiment, which is a part of our Bachelor thesis. The aim of our study is to investigate how SAT solvers can be used to synthesize an artificial neural network.

To answer this we conducted this experiment, where we try to simulate a network by constructing propositional formulas in conjunction normal form (CNF), where this formula and assumptions of the dataset is used by a SAT solver to generate a model that correctly fits a dataset. Please refer to [this](https://github.com/palmoto1/nn_sat/blob/main/src/nn_sat.py) file to see our implementation.

The SAT solver used in *NN-SAT* is **Glucose**, created by [Gilles Audemard](http://www.cril.univ-artois.fr/~audemard/) & [Laurent Simon](https://www.labri.fr/perso/lsimon/).

## Method
### Dataset generation
Datasets used consisted of binary strings, which were randomly genrated. Given the inputs of $d$ (number of hidden layers), $\ell$ (hidden layer size), $n$ (string length), $|D|$ (dataset size) and $t$ (distribution threshold), the [generator](https://github.com/palmoto1/nn_sat/blob/main/src/data_set_generator.py) constructed a neural network represented as a graph were each neuron were given a randomized threshold value. We utilized Pythons built-in module [random](https://docs.python.org/3/library/random.html). The module implements pseudo-random number generators for different distributions.

### Evaluation
The [evaluation model](https://github.com/palmoto1/nn_sat/blob/main/src/evaluation.py) is a graph of neurons representing a network, where each corresponding neuron in the evaluation network will have the same thresholds and edges as the original model produced by the SAT solver. Using only the information in the weight variables, we can also derive the network depth and amounts of neurons per layer. Which is used when constructing the evaluation model, to ensure it to be uniform with the original model. Which is done by generating neurons from the information in the weight variables, and the connecting the neurons.


## Results
The experiment did successfully produce a model representing the synthesis of a feed-forward neural network able to fit a dataset. The length of the input-strings did not affect the models ability to correctly fit the dataset *(experiment 1)*. The performance was tested by measuring the relation between network depth and computational time *(experiment 2)*. The largest network synthesized in the time-limit of 10 minutes had the size of $18$ hidden layers and $8$ neurons per layer, i.e. $160$ neurons among the hidden layers. No correlation was found between number of activated neurons per layer and network depth *(experiment 3)*. Our model could also fit a dataset regardless if depth and layer size was decreased, even down to a network consisting of only one perceptron *(experiment 4)*.

For more information how they were conducted please refer to the experiments [source code](https://github.com/palmoto1/nn_sat/blob/main/src/experiment.py) and the folder [experiments](https://github.com/palmoto1/nn_sat/tree/main/experiments) to find the dataset and models used for each experiment.

## Download and Run
To use and run NN-SAT you need Python 3 as well as the [PySAT](https://pysathq.github.io/) API.


