class PriorityQueue:
    def __init__( self, cmp=None ):
        self.queue = []
        self.cmp = cmp or (lambda x, y: x < y)
        
    def _cmp( self, p1, p2 ):
        return self.cmp( self.queue[p1], self.queue[p2] )

    def _swap( self, p1, p2 ):
        self.queue[p1], self.queue[p2] = self.queue[p2], self.queue[p1]

    def _bubbleUp( self, pos ):
        while pos > 0:
            parent = int( (pos - 1) / 2 )
            if self._cmp( pos, parent ):
                self._swap( pos, parent )
                pos = parent
            else:
                pos = 0

    def _bubbleDown( self, pos ):
        end = len( self.queue ) - 1
        while pos <= (end - 1) / 2:
            child1 = 2 * pos + 1
            child2 = 2 * pos + 2
            
            if self._cmp( child1, pos ):
                if child2 <= end and self._cmp( child2, child1 ):
                    self._swap( child2, pos )
                    pos = child2
                else:
                    self._swap( child1, pos )
                    pos = child1
            elif child2 <= end and self._cmp( child2, pos ):
                self._swap( child2, pos )
                pos = child2
            else:
                pos = end

    def peek( self ):
        return self.queue[0]

    def pop( self ):
        end = len( self.queue ) - 1

        if end < 0:
            return None

        ret = self.queue[0]

        self.queue[0], self.queue[ end ] = self.queue[end], self.queue[0]
        self.queue.pop()

        self._bubbleDown( 0 )

        return ret

    def insert( self, val ):
        self.queue.append( val )
        self._bubbleUp( len( self.queue ) - 1 )

