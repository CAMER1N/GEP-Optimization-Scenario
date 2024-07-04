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
An example of this would be the scenario (i,j,k,l,m) where each variable is a given set. 
Given sets are listed below:


## Parameters

The pre-determined parameters are defined within the given code/files:

1. Fixed operation cost \n
2. Additional cost to buy additional power
3. Demand for each time period
4. Gen 1 availability 
5. Gen 2 availability 
6. Fixed cost per unit capacity of generator j    


## Constaints

The pre-determined constraints are defined within the given code/files:

1. Demand Satisfaction Constraint
2. Availability Constraints

## Variables

The variables the solver will output are listed below:

1. x = installed capacity of generator j
2. y = operating level of generator j
3. y_purchased = Additional capacity purchased

## Objective


