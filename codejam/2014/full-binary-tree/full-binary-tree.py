#!/usr/bin/env python

import sys
import copy
import SubsetGenerator

class Graph:
    def __init__( self, count ):
        self.count = count
        self.nodes = frozenset( map( lambda x: x, xrange( self.count ) ) )
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
        return newgraph


    def dfsFindTree( self, node, visited = frozenset( [] ) ):
        ret = frozenset( [ node ] )

        for otherNode in filter( lambda x: x not in visited, self.edges[ node ] ):
            ret = ret | self.dfsFindTree( otherNode, visited | frozenset( [ otherNode ] ) )

        return ret

    def findDisjointTrees( self ):
        trees = []
        for n in self.nodes:
            if len( filter( lambda x: n in x, trees ) ) == 0:
                trees.append( self.dfsFindTree( n ) )

        return trees

    def removeSingletons( self ):
        removed = frozenset( [] )
        build = self

        for n in self.nodes:
            if len( self.edges[ n ] ) == 0:
                removed = removed | n
                build = build.removeNode( n )

        return ( removed, build )

    def truncateChain( self ):
        for n in self.nodes:
            if len( self.edges[n] ) == 1: # Leave
                next = self.edges[n][0]
                if len( self.edges[next] ) == 2: # Not full
                    nextNext = filter( lambda x: x != n, self.edges[next] )[0]
                    if len( self.edges[nextNext] ) > 1: # Not a valid 3 node tree
                        return ( frozenset( [ n ] ), self.removeNode( n ) )

        return ( frozenset( [] ), self )

    def findForceRemove( self ):
        trees = self.findDisjointTrees()

        if len( trees ) > 1:
            raise Exception( "should purne tree" )

        removed = frozenset( [] )
        build = self
        more = True
        while more:
            more = False
            ( newRemoved, newBuild ) = build.removeSingletons()
            if len( newRemoved ) > 0:
                more = True
                removed = removed | newRemoved
                build = newBuild

        more = True
        while more:
            more = False
            ( newRemoved, newBuild ) = build.truncateChain()
            if len( newRemoved ) > 0:
                more = True
                removed = removed | newRemoved
                build = newBuild
            
        return ( removed, build )
            
    def isFull( self ):
        if len( self.nodes ) == 1:
            return True

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

    def growRoot( self, node, visited = frozenset() ):
        tree = frozenset( [ node ] )

        subtrees = filter( lambda x: x not in visited, self.edges[ node ] )
        if len( subtrees ) < 1:
            return tree

        newVisit = visited | tree

        subtrees = map( lambda x: self.growRoot( x, newVisit ), subtrees )

        subtrees = sorted( subtrees, key=lambda x: -len( x ) )

        if len( subtrees ) > 1:
            tree = tree | subtrees[0] | subtrees[1]
                
        return tree

    def findFullGrowRoot( self ):
        toRemove = None

        for n in self.nodes:
            tree = self.growRoot( n )
            #print "  growRoot( %d ) => %r" % ( n, tree )
            if tree is not None:
                newToRemove = self.nodes - tree
                if toRemove is None or len( newToRemove ) < len( toRemove ):
                    toRemove = newToRemove

        return toRemove


    def findFull( self ):
        #for n in self.nodes:
        #    print "%d: %r" % ( n, self.edges[n] )

        return self.findFullGrowRoot()
        
        if self.isFull():
            return []

        ( preRemove, subG ) = ( frozenset(), self )
        #( preRemove, subG ) = self.findForceRemove()

        #print "preRemove = %r" % preRemove

        if not subG.isFull():
            subsetgen = SubsetGenerator.SubsetGenerator( self.nodes - preRemove )
        
            for subset in subsetgen:
                subSubG = subG
                for node in subset:
                    subSubG = subSubG.removeNode( node )
                if subSubG.isFull():
                    return preRemove | frozenset( subset )

        return preRemove

def singleTest( testNum ):
    nodeCount = int( sys.stdin.readline() )
    graph = Graph( nodeCount )
    for edge in xrange( nodeCount - 1 ):
        edge = map( int, sys.stdin.readline().split() )
        if len( edge ) != 2:
            raise Exception( "Edge %r doesn't have two points" % edge )
        graph.addEdge( edge )

    sys.setrecursionlimit( 10000 )

    removed = graph.findFull()
    
    print "Case #%d: %d" % ( testNum, len( removed ) )
    #print "Case #%d: %d # %r %r" % ( testNum, len( removed ), graph.edges, removed )

def main():
    testCount = int( sys.stdin.readline() )
    for test in xrange( testCount ):
        singleTest( test + 1 )

main()
