#!/usr/bin/env python

import sys

def playNaomi( naomiWeights ):
    return naomiWeights[0]

def playDeceitfulNaomi( naomiWeights, kenWeights ):
    epsilon = 1e-7

    worstNaomi = min( naomiWeights )
    bestKen = max( kenWeights )

    if worstNaomi > bestKen:
        return ( naomiWeights[0], naomiWeights[0] )
    else:
        return ( worstNaomi, bestKen - epsilon )

def playKen( kenWeights, naomiPlay ):
    better = filter( lambda x: x > naomiPlay, kenWeights )
    if len( better ) > 0:
        return min( better )
    else:
        return min( kenWeights )

def playWar( naomiWeights, kenWeights ):
    score = 0

    naomiWeights = naomiWeights[:]
    kenWeights = kenWeights[:]

    while len( naomiWeights ) > 0:
        naomiPlay = playNaomi( naomiWeights )
        naomiWeights.remove( naomiPlay )
        kenPlay = playKen( kenWeights, naomiPlay )
        kenWeights.remove( kenPlay )

        print "%f vs %f" % ( naomiPlay, kenPlay )

        if kenPlay < naomiPlay:
            score = score + 1

    return score

def playDeceitfulWar( naomiWeights, kenWeights ):
    score = 0

    naomiWeights = naomiWeights[:]
    kenWeights = kenWeights[:]

    while len( naomiWeights ) > 0:
        ( naomiPlay, naomiTell ) = playDeceitfulNaomi( naomiWeights, kenWeights )
        naomiWeights.remove( naomiPlay )
        kenPlay = playKen( kenWeights, naomiTell )
        kenWeights.remove( kenPlay )

        print "%f (%f) vs %f" % ( naomiPlay, naomiTell, kenPlay )

        if kenPlay > naomiPlay == kenPlay > naomiTell:
            raise Exception( "internal trouble" )

        if kenPlay < naomiPlay:
            score = score + 1

    return score

def singleTest( testNum ):
    weightCount = int( sys.stdin.readline() )
    naomiWeights = map( float, sys.stdin.readline().split( " " ) )
    kenWeights = map( float, sys.stdin.readline().split( " " ) )

    warScore = playWar( naomiWeights, kenWeights )
    deceitfulWarScore = playDeceitfulWar( naomiWeights, kenWeights )

    print "Case #%d: %d %d" % (testNum, deceitfulWarScore, warScore )

def main():
    testCount = int( sys.stdin.readline() )
    for test in xrange( testCount ):
        singleTest( test + 1 )

main()
