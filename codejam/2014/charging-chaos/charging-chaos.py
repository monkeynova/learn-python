#!/usr/bin/env python

import sys

def bruteCaseSingle( bits, devices, outlets ):
    def flipBits( outlet ):
        def flipBit( bit ):
            if bit in bits:
                if outlet[bit] == "0":
                    return "1"
                else:
                    return "0"
            return outlet[bit]

        return "".join( map( flipBit, xrange( len( outlet ) ) ) )

    flipped = frozenset( map( flipBits, outlets ) )
        
    if devices == flipped:
        return True
    else:
        return False

def bruteCase( L, devices, outlets ):
    # print "Trying %d" % 2 ** L
    best = None
    bestBits = None
    for i in xrange( 2 ** L ):
        bits = frozenset( filter( lambda n: i & (1 << n) > 0, xrange( L ) ) )
        if bestBits is None or len( bestBits ) > len( bits ):
            # print "%d: %r" % ( i, bits )
            if bruteCaseSingle( bits, devices, outlets ):
                best = len( bits )
                bestBits = bits

    return best

def singleCase( caseNum ):
    config = sys.stdin.readline().split( " " )
    
    if len( config ) != 2:
        raise Exception( "first line of case %d doesn't have two entries" % caseNum )

    N = int( config[0] )
    L = int( config[1] )

    outlets = sys.stdin.readline().rstrip().split( " " )
    devices = sys.stdin.readline().rstrip().split( " " )

    if len( outlets ) != N:
        raise Exception( "second line of case %d doesn't have %d entries" % ( caseNum, N ) )

    if len( filter( lambda x: len( x ) != L, outlets ) ) > 0:
        raise Exception( "second line of case %d contains entries if size other than %d" % ( caseNum, L ) )

    if len( devices ) != N:
        raise Exception( "third line of case %d doesn't have %d entries" % ( caseNum, N ) )

    if len( filter( lambda x: len( x ) != L, devices ) ) > 0:
        raise Exception( "second line of case %d contains entries if size other than %d" % ( caseNum, L ) )

    best = bruteCase( L, frozenset( devices ), frozenset( outlets ) )

    if best is not None:
        print "Case #%d: %d" % ( caseNum, best )
    else:
        print "Case #%d: NOT POSSIBLE" % caseNum

def main():
    caseCount = int( sys.stdin.readline() )
    for case in xrange( caseCount ):
        singleCase( case + 1 )

main()
