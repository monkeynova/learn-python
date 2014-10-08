#!/usr/bin/env python

import Graph
import TAP

clique = Graph.Graph( 7 )
for i in xrange( 7 ):
    for j in xrange( i + 1, 7 ):
        clique.addEdge( i, j )

parentsBfs = []
parentsDfs = []
for i in xrange( 7 ):
    parentsBfs.append( None )
    parentsDfs.append( None )

def onBfs( x, y ):
    parentsBfs[x] = y

def onDfs( x, y ):
    parentsDfs[x] = y

clique.bfs( onBfs )
clique.dfs( onDfs )

TAP.isval( parentsBfs, [ 0, 0, 0, 0, 0, 0, 0 ] )
TAP.isval( parentsDfs, [ 0, 0, 1, 2, 3, 4, 5 ] )
