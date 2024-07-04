# Generation Expansion Planning (GEP) Problem

This project addresses a Generation Expansion Planning (GEP) problem using Python/Pyomo. Pyomo is a package used within Python to create optimzation models.
The goal is to develop an optimal plan for the expansion of generation capacity to meet future electricity demands at minimal cost, considering given constraints and factors.


# Installation

To get started with this project, you will need to have Python installed on your machine. Pyomo must also be downloaded.

Gurobi Solver must be installed as a solver for the created model.


# Documentation

## Generation Representation:

We assume all generators and outsourced energy are renewables in this scenario.

## Sets:

Sets in this code are seen as specific scenarios. We can combine these sets to form a 5D array, which represent all possible scenarios.
An example of this would be the scenario (i,j,k,l,m) where each digit is a given set. 
Given sets are listed below:


## Parameters:

The pre-determined parameters are defined within the given code/files:

Fixed operation cost /n
Additional cost to buy additional power
Demand for each time period
Gen 1 availability 
Gen 2 availability 
Fixed cost per unit capacity of generator j    


## Constaints

## Variables


