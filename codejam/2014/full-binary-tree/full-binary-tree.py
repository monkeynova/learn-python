#!/usr/bin/env python

import sys
import copy
import SubsetGenerator

class Graph:
    def __init__( self, count ):
        self.count = count
        self.nodes = frozenset( map( lambda x: x, xrange( self.count ) ) )
        self.removed = frozenset()
        self.edges = map( lambda x: [], xrange( self.count ) )

    def addEdge( self, edge ):
        self.edges[ edge[0] - 1 ].append( edge[1] - 1 )
        self.edges[ edge[1] - 1 ].append( edge[0] - 1 )

    def removeNode( self, node ):
        newgraph = Graph( self.count )
        newgraph.nodes = self.nodes - frozenset( [ node ] )
        newgraph.edges = copy.deepcopy( self.edges )
        newgraph.edges[ node ] = []
        for n in self.edges[ node ]:
            newgraph.edges[ n ].remove( node )
        newgraph.removed = self.removed | frozenset( [ node ] )
        return newgraph

    def isFull( self ):
        edgecount = [ [], [], [], [], [] ]

        for n in self.nodes:
            edgecount[ min( len( self.edges[ n ] ), 4 ) ].append( n )
            
        if len( edgecount[4] ) > 0:
            # Non-tree nodes
            return False

        if len( edgecount[2] ) != 1:
            # No single root
            return False

        if len( edgecount[0] ) != 0:
            # Singleton node
            return False

        root = edgecount[2][0]
        return self.dfsIsFull( root )

    def dfsReachableFull( self, node, parent ):
        match = frozenset( [ node ] )

        for subnode in self.edges[node]:
            if parent is None or subnode != parent:
                match = match | self.dfsReachableFull( subnode, node )

        return match
        
    def dfsIsFull( self, root ):
        return self.dfsReachableFull( root, None ) == self.nodes

    def findFull( self ):
        if len( self.nodes ) == 0:
            return self.removed

        if self.isFull():
            return self.removed

        #print "%sfindFull( %r )" % ( "  " * len( self.removed ), self.nodes )

        subsetgen = SubsetGenerator.SubsetGenerator( len( self.nodes ) )
        
        for subset in subsetgen:
            subG = self
            for node in subset:
                subG = subG.removeNode( node )
            if subG.isFull():
                return subset

        return None

def singleTest( testNum ):
    nodeCount = int( sys.stdin.readline() )
    graph = Graph( nodeCount )
    for edge in xrange( nodeCount - 1 ):
        edge = map( int, sys.stdin.readline().split() )
        if len( edge ) != 2:
            raise Exception( "Edge %r doesn't have two points" % edge )
        graph.addEdge( edge )

    removed = graph.findFull()

    print "Case #%d: %d" % ( testNum, len( removed ) )
    #print "Case #%d: %d # %r %r" % ( testNum, len( removed ), graph.edges, removed )

def main():
    testCount = int( sys.stdin.readline() )
    for test in xrange( testCount ):
        singleTest( test + 1 )

main()
