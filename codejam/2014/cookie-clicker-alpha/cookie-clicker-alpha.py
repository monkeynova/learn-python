#!/usr/bin/env python

import sys

def bestTime( farmCost, farmRate, goal ):
    time = 0
    farmCount = 0

    while True:
        cookiesPerSecond = 2 + farmCount * farmRate
        waitTime = time + goal / cookiesPerSecond
    
        if farmCost > goal:
            return waitTime

        newFarmCPS = 2 + (farmCount + 1) * farmRate
        newFarmWaitTime = time + (farmCost / cookiesPerSecond) + goal / newFarmCPS

        if ( newFarmWaitTime > waitTime ):
            return waitTime

        time = time + farmCost / cookiesPerSecond
        farmCount = farmCount + 1
        

def singleTest( testNum ):
    vals = map( float, sys.stdin.readline().split() )
    F = vals[0]
    C = vals[1]
    X = vals[2]

    time = bestTime( F, C, X )

    print "Case #%d: %f" % (testNum, time)

def main():
    testCount = int( sys.stdin.readline() )
    for testNum in xrange( testCount ):
        singleTest( testNum + 1 )

main()
