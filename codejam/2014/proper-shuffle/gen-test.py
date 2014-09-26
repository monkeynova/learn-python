#!/usr/bin/env python

import gbrand
import random

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
