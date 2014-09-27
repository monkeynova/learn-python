#!/usr/bin/env python

import gbrand
import random

# P( value in position ) = empiricalBias[position][value]
empiricalBias = [
    [1.0, 1.29, 1.2, 1.11, 1.04, 0.97, 0.91, 0.86, 0.81, 0.77],
    [0.99, 0.94, 1.24, 1.16, 1.09, 1.02, 0.95, 0.9, 0.85, 0.81],
    [1.0, 0.94, 0.89, 1.2, 1.13, 1.07, 1.0, 0.95, 0.9, 0.86],
    [0.99, 0.95, 0.9, 0.87, 1.18, 1.11, 1.06, 1.01, 0.96, 0.92],
    [0.99, 0.96, 0.92, 0.88, 0.86, 1.17, 1.12, 1.06, 1.02, 0.97],
    [0.99, 0.95, 0.93, 0.9, 0.88, 0.86, 1.19, 1.13, 1.08, 1.04],
    [0.99, 0.97, 0.95, 0.92, 0.9, 0.88, 0.87, 1.2, 1.15, 1.11],
    [1.0, 0.98, 0.96, 0.95, 0.93, 0.91, 0.9, 0.9, 1.24, 1.19],
    [1.0, 0.98, 0.98, 0.96, 0.96, 0.96, 0.95, 0.94, 0.94, 1.29],
    [0.99, 1.0, 0.99, 1.0, 0.99, 1.0, 1.0, 0.99, 1.0, 0.99]
]

def probabilityBadPosition( position, value, N ):
    # TODO
    return 1.0 / N

def probabilityGoodPosition( position, value, N ):
    return 1.0 / N

def generateFeatures( list ):
    mid = len( list ) / 2
    mean1 = 0.0
    mean2 = 0.0
    weightedMean = 0.0

    for i in xrange( mid ):
        mean1 += list[i]
        mean2 += list[i + mid];
        weightedMean += (len( list ) - i) * list[i]
        weightedMean += (len( list ) - i - mid) * list[i + mid]

    mean1 /= len( list )
    mean2 /= len( list )
    weightedMean /= len( list )

    return {
        'sideMeanDelta' : mean1 / mean2,
        'weightedMean' : weightedMean / len( list ) / len( list ) / 0.25,
        'firstVal' : float( list[0] ) / len( list ) / 0.5,
        }

def weightedMean( list ):
    features = generateFeatures( list )
    return features["weightedMean"] > 0.99
    #return features["weightedMean"] > 0.25

def sideMean( list ):
    features = generateFeatures( list )
    return features["sideMeanDelta"] > 1
    #return features["leftMean"] > features["rightMean"]

def firstVal( list ):
    features = generateFeatures( list )
    return features["firstVal"] > 1.2

def combined( list ):
    features = generateFeatures( list )
    return (0.8 * features["sideMeanDelta"] + 1.2 * features["weightedMean"]) / 2.0 > 0.98

def adhoc( list ):
    weighted = weightedMean( list )
    side = sideMean( list )

    return weighted or side

    if weighted == side:
        return weighted
    else:
        return firstVal( list )

def tryClassifier( classifier, name ):
    N = 1000
    correct = 0
    correctGood = 0
    correctBad = 0
    attempts = 0
    for i in xrange( 60 ):
        attempts += 2
        good = gbrand.goodShuffle( N )
        if classifier( good ):
            correct += 1
            correctGood += 1
        bad = gbrand.badShuffle( N )
        if not classifier( bad ):
            correct += 1
            correctBad += 1

    print "%s: %d out of %d correct (%f%%)" % ( name, correct, attempts, 100.0 * correct / attempts )
    print "  %d out of %d good correct (%f%%)" % ( correctGood, attempts / 2, 200.0 * correctGood / attempts )
    print "  %d out of %d bad correct (%f%%)" % ( correctBad, attempts / 2, 200.0 * correctBad / attempts )

def main():
    tryClassifier( lambda x: True, "true" )
    tryClassifier( weightedMean, "weightedMean" )
    tryClassifier( sideMean, "sideMean" )
    tryClassifier( firstVal, "firstVal" )
    tryClassifier( adhoc, "adhoc" )
    tryClassifier( combined, "combined" )

    

main()
