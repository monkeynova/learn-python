class SubsetGenerator:
    def __init__( self, iter ):
        self.n = len( iter )
        self.index = [ n for n in iter ]
        self.size = 0
        self.subiter = None

    def __iter__( self ):
        return self

    def subiterNext( self ):
        return map( lambda x: self.index[x], self.subiter.next() )

    def next( self ):
        if self.subiter is not None:
            try:
                return self.subiterNext()
            except StopIteration:
                self.subiter = None

        self.size += 1
        if self.size > self.n:
            raise StopIteration

        self.subiter = SubsetGeneratorSize( self.n, self.size )
        return self.subiterNext()

class SubsetGeneratorSize:
    def __init__( self, n, size, skip = -1 ):
        self.n = n
        self.cur = skip
        self.size = size
        self.skip = skip
        self.subiter = None

    def __iter__( self ):
        return self

    def subiterNext( self ):
        next = [ self.cur ]
        next.extend( self.subiter.next() )
        return next        

    def next( self ):
        if self.subiter is not None:
            try:
                return self.subiterNext()
            except StopIteration:
                self.subiter = None

        self.cur += 1
        if self.cur >= self.n:
            raise StopIteration

        if self.size == 1:
            return [ self.cur ]

        self.subiter = SubsetGeneratorSize( self.n, self.size - 1, self.cur )

        return self.subiterNext()
