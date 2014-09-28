#!/usr/bin/env python

import sys

def maybeFlipBit( maybe, c ):
    if maybe:
        if c == "1":
            return "0"
        else:
            return "1"
    else:
        return c

def flipBits( bits, outlet ):
    return "".join( map( lambda x: maybeFlipBit( x in bits, outlet[x] ), xrange( len( outlet ) ) ) )

def updateOutlets( outlets, removeOutlet, newBits ):
    ret = []
    for o in outlets:
        if o != removeOutlet:
            ret.append( flipBits( newBits, o ) )

    return ret

def neededBits( device, outlet, usedbits ):
    newbits = frozenset( filter( lambda x: device[x] != outlet[x], xrange( len( device ) ) ) )
    if len( newbits & usedbits ) > 0:
        return None
    else:
        return newbits

def findBestBits( devices, outlets ):
    return nextDevice( devices, 0, outlets, frozenset() )

def nextDevice( devices, deviceNum, outlets, bits ):
    if deviceNum == len( devices ):
        return bits

    d = devices[ deviceNum ]
    bestBits = None

    for o in outlets:
        newBits = neededBits( d, o, bits )
        #print "%s (%s => %s): %r" % ( "  " * deviceNum, d, o, newBits )
        if newBits is not None:
            if len( newBits & bits ) > 0:
                raise Exception( "newBits returned already used bits" )
            newOutlets = updateOutlets( outlets, o, newBits )
            finalBits = nextDevice( devices, deviceNum + 1, newOutlets, bits | newBits )
            #print "%s %r" % ( "  " * deviceNum, finalBits )
            if finalBits is not None:
                if bestBits is None or len( finalBits ) < len( bestBits ):
                    bestBits = finalBits

    return bestBits



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

    best = findBestBits( devices, outlets )

    if best is not None:
        print "Case #%d: %d" % ( caseNum, len( best ) )
    else:
        print "Case #%d: NOT POSSIBLE" % caseNum

def main():
    caseCount = int( sys.stdin.readline() )
    for case in xrange( caseCount ):
        singleCase( case + 1 )

main()
