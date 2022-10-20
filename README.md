# Elementary-Celullar-Automaton-Simulator

This program simulates the evolution of an elementary cellular automaton given an initial state and a number of generations.

# Introduction

 Elementary cellular automata have two possible values for each cell (0 or 1), and rules that depend only on nearest neighbor values. As a result, the evolution of an elementary cellular automaton can completely be described by a table specifying the state a given cell will have in the next generation based on the value of the cell to its left, the value the cell itself, and the value of the cell to its right. 

# Technologies

* Python
*	PyQt5
* Matplotlib
* Numpy
* SLY - Lex Yacc

# Setup

Via conda:
 Install  numpy, PyQt5, matplotlib and sly.
 
# Usage

 Just execute the program with the command "python simulador.py"
 
 # Features
 
 * Change the simulation speed
 * Play and Pause the simulation
 * Save the ECA evolution as a .png image
 * Save the initial condition as JSON
 * Change the simulation colors
 * Choose between three types of ECA graph
 * Generate an initial state using the regex input, expample: ( 0 1 ) * , ( 0 + 1 )
 * Generate a random initial state
 
 # ScreenShots
 
 ![rule122](/Imagenes/ECA_Simulator.png)
 
 ![rule126](/Imagenes/ECA_Simulator_2.png)
