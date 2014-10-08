class Graph:
    def __init__( self, nodeCount ):
        self.edges = []
        for i in xrange( nodeCount ):
            self.edges.append( [] )
        self.nodeCount = nodeCount

    def _debug( self ):
        for v in xrange( self.nodeCount ):
            print "  %d: %r" % ( v, self.edgeList( v ) )

    def addEdge( self, v1, v2 ):
        if v1 >= self.nodeCount:
            raise Exception( "bad node %d (>= %d)" % ( v1, self.nodeCount ) )
        if v2 >= self.nodeCount:
            raise Exception( "bad node %d (>= %d)" % ( v2, self.nodeCount ) )
        self.edges[v1].append( v2 )
        self.edges[v2].append( v1 )
        
    def nodeCount( self ):
        return self.nodeCount
    
    def edgeList( self, vertex ):
        return self.edges[ vertex ]

    def bfs( self, onNode ):
        parent = []
        for v in xrange( self.nodeCount ):
            parent.append( None )

        for v in xrange( self.nodeCount ):
            if parent[ v ] is None:
                queue = [ v ]
                parent[ v ] = v

                while len( queue ) > 0:
                    v = queue[ 0 ]
                    queue = queue[ 1: ]
                    onNode( v, parent[ v ] )
                    for dest in self.edgeList( v ):
                        if parent[ dest ] is None:
                            parent[ dest ] = v
                            queue.append( dest )

    def _dfsRecursive( self, v, onNodeStart, onNodeEnd, visited, parent ):
        visited[ v ] = parent

        if onNodeStart:
            onNodeStart( v, visited[v] )

        for dest in self.edgeList( v ):
            if visited[ dest ] is None:
                self._dfsRecursive( dest, onNodeStart, onNodeEnd, visited, v )
            
        if onNodeEnd:
            onNodeEnd( v, visited[ v ] )

    def dfs( self, onNodeStart, onNodeEnd=None ):
        visited = []
        for v in xrange( self.nodeCount ):
            visited.append( None )

        for v in xrange( self.nodeCount ):
            if visited[v] is None:
                self._dfsRecursive( v, onNodeStart, onNodeEnd, visited, v )
