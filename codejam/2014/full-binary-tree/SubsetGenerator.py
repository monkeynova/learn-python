class SubsetGenerator:
    def __init__( self, n ):
        self.n = n
        self.size = 0
        self.subiter = None

    def __iter__( self ):
        return self

    def next( self ):
        if self.subiter is not None:
            try:
                return self.subiter.next()
            except StopIteration:
                self.subiter = None

        self.size += 1
        if self.size > self.n:
            raise StopIteration

        self.subiter = SubsetGeneratorSize( self.n, self.size )
        return self.subiter.next()

class SubsetGeneratorSize:
    def __init__( self, n, size, skip = -1 ):
        self.n = n
        self.cur = skip
        self.size = size
        self.skip = skip
        self.subiter = None

    def __iter__( self ):
        return self

    def next( self ):
        if self.subiter is not None:
            try:
                next = [ self.cur ]
                next.extend( self.subiter.next() )
                return next
            except StopIteration:
                self.subiter = None

        self.cur += 1
        if self.cur >= self.n:
            raise StopIteration

        if self.size == 1:
            return [ self.cur ]

        self.subiter = SubsetGeneratorSize( self.n, self.size - 1, self.cur )

        next = [ self.cur ]
        next.extend( self.subiter.next() )
        return next
