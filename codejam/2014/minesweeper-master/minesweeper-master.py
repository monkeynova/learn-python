#!/usr/bin/env python

import sys

def singleTest( testNum ):
    row = map( int, sys.stdin.readline().split( " " ) )
    R = row[0]
    C = row[1]
    M = row[2]
    impossible = False

    grid = range( R )

    for i in xrange( R ):
        grid[i] = range( C )
        for j in xrange( C ):
            grid[i][j] = "."

    if R * C - 1 == M:
        for i in xrange( R ):
            grid[i] = range( C )
            for j in xrange( C ):
                grid[i][j] = "*"
        grid[0][0] = "c"
    else:
        x = 0
        y = 0

        for mine in xrange( M ):
            grid[x][y] = "*"

            x = x + 1
            y = y - 1
            if y < 0 or x >= R:
                if y >= 0:
                    x = x + y + 1
                    y = -1
                    
                y = min( x, C - 1 )
                x = x - y

            if False:
                impossible = True
                break
    
        if not impossible:
            grid[R-1][C-1] = "c"


    if impossible:
        print "Case #%d:\nImpossible" % testNum
    else:
        print "Case #%d:" % testNum
        for i in xrange( R ):
            print "%s" % "".join( grid[i] )

def main():
    testCount = int( sys.stdin.readline() )
    for i in xrange( testCount ):
        singleTest( i + 1 )

main()

def singleTestNoWorka( testNum ):
    row = map( int, sys.stdin.readline().split( " " ) )
    R = row[0]
    C = row[1]
    M = row[2]
    impossible = False

    grid = range( R )

    for i in xrange( R ):
        grid[i] = range( C )
        for j in xrange( C ):
            grid[i][j] = "."

    if R * C - 1 == M:
        for i in xrange( R ):
            grid[i] = range( C )
            for j in xrange( C ):
                grid[i][j] = "*"
        grid[0][0] = "c"
    else:
        fillRight = R * max( C - 2, 0 )
        # print "%d %d %d %d" % (M, R, fillRight, M % R)
        # if M > 0 and fillRight > M and M % R == R - 1:
        #    fillRight = M - 1

        fillTop = min( C, 2 ) * max( R - 2, 0 )
        if fillTop % 2 == 1 and C > 1:
            fillTop = fillTop - 1 

        if fillTop + fillRight >= M:
            x = C - 1
            y = 0
            for mine in xrange( min( fillRight, M ) ):
                grid[y][x] = "*"
                y = y + 1
                if y >= R:
                    x = x - 1
                    y = 0
                        
            x = min( 1, C - 1 )
            y = 0
            for mine in xrange( min( fillTop, max( M - fillRight, 0 ) ) ):
                grid[y][x] = "*"
                x = x - 1
                if x < 0:
                    y = y + 1
                    x = min( 1, C - 1 )
                    
            grid[R - 1][0] = "c"
        else:
            impossible = True
    

    if impossible:
        print "Case #%d:\nImpossible" % testNum
    else:
        print "Case #%d:" % testNum
        for i in xrange( R ):
            print "%s" % "".join( grid[i] )
