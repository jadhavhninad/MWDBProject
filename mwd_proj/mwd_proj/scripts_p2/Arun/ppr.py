import os
import sys
import math

import numpy
import pandas

# Generalized matrix operations:

def __extractNodes(matrix):
    nodes = set()
    for colKey in matrix:
        nodes.add(colKey)
    for rowKey in matrix.T:
        nodes.add(rowKey)
    return nodes

def __makeSquare(matrix, keys, default=0.0):
    matrix = matrix.copy()
    
    def insertMissingColumns(matrix):
        for key in keys:
            if not key in matrix:
                matrix[key] = pandas.Series(default, index=matrix.index)
        return matrix

    matrix = insertMissingColumns(matrix) # insert missing columns
    matrix = insertMissingColumns(matrix.T).T # insert missing rows

    return matrix.fillna(default)

def __ensureRowsPositive(matrix):
    matrix = matrix.T
    for colKey in matrix:
        if matrix[colKey].sum() == 0.0:
            matrix[colKey] = pandas.Series(numpy.ones(len(matrix[colKey])), index=matrix.index)
    return matrix.T

def __normalizeRows(matrix):
    return matrix.div(matrix.sum(axis=1), axis=0)

def __euclideanNorm(series):
    return math.sqrt(series.dot(series))

# PageRank specific functionality:

def __startState(setActors,nodes):
    if len(nodes) == 0: raise ValueError("There must be at least one node.")
    startProb = 1.0 / float(len(setActors))
    seriesdict = {}
    for node in nodes:
	if node in setActors:
	  seriesdict[node] = startProb
	else:
	  seriesdict[node] = 0.0
    oldSeries = pandas.Series({node : startProb for node in nodes})
    returnSeries = pandas.Series(seriesdict)
    #print returnSeries
    return returnSeries

def __integrateRandomSurfer(setActors,nodes, transitionProbs, rsp):
    alpha = 1.0 / float(len(setActors)) * rsp
    temp = transitionProbs.copy().multiply(1.0 - rsp)
    #print temp
    return temp

def powerIteration(setActors,transitionWeights, rsp=0.15, epsilon=0.00001, maxIterations=1000):
    # Clerical work:
    transitionWeights = pandas.DataFrame(transitionWeights)
    nodes = __extractNodes(transitionWeights)
    #print(nodes)
    #print(setActors)
    transitionWeights = __makeSquare(transitionWeights, nodes, default=0.0)
    transitionWeights = __ensureRowsPositive(transitionWeights)
	
    # Setup:
    state = __startState(setActors,nodes)
    #print(state)
    transitionProbs = __normalizeRows(transitionWeights)
    #print(transitionProbs)
    transitionProbs = __integrateRandomSurfer(setActors, nodes, transitionProbs, rsp)
    #print(transitionProbs)
    
    # Power iteration:
    for iteration in range(maxIterations):
        oldState = state.copy()
	tpvector = state*rsp
	#print(tpvector)
        state = state.dot(transitionProbs) + tpvector
        delta = state - oldState
        if __euclideanNorm(delta) < epsilon: break

    return nodes,state