#!/usr/bin/env python

import sys

def singleTest( testNum ):
    answer1 = int( sys.stdin.readline() )
    grid1 = []
    for i in xrange(4):
       row = map( int, sys.stdin.readline().split( " " ) )
       grid1.append( row )
    answer2 = int( sys.stdin.readline() )
    grid2 = []
    for i in xrange(4):
       row = map( int, sys.stdin.readline().split( " " ) )
       grid2.append( row )

    row1 = grid1[answer1 - 1]
    row2 = grid2[answer2 - 1]

    overlap = frozenset( row1 ) & frozenset( row2 )

    if ( len( overlap ) == 1 ):
        for val in overlap:
            print "Case #%d: %d" % (testNum, val)
    elif ( len( overlap ) == 0 ):
        print "Case #%d: Volunteer cheated!" % testNum
    else:
        print "Case #%d: Bad magician!" % testNum

def main():
    testcount = int( sys.stdin.readline() )
    for testNum in xrange( testcount ):
        singleTest( testNum + 1 )

main()
