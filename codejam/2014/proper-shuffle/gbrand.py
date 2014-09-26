import random

def goodShuffle( N ):
    list = range( N )
    for x in xrange( N ):
        i = random.randint( x, N - 1 )
        ( list[x], list[i] ) = ( list[i], list[x] )

    return list

def badShuffle( N ):
    list = range( N )
    for x in xrange( N ):
        i = random.randint( 0, N - 1 )
        ( list[x], list[i] ) = ( list[i], list[x] )

    return list
