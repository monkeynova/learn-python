#!/usr/bin/env python

import gbrand

def main():
    C = 1000000
    N = 5
    grid = []
    for i in xrange( N ):
        grid.append( [ 0 ] * N )
    
    for i in xrange( C ):
        list = gbrand.badShuffle( N )
        for j in xrange( N ):
            grid[j][list[j]] += 1 

    for i in xrange( len( grid ) ):
        for j in xrange( len( grid[i] ) ):
            grid[i][j] *= float( N ) / C
            grid[i][j] = int( grid[i][j] * 100 ) / 100.0
        print "%d: %r" % (i, grid[i] )
            

main()
