#!/usr/bin/env python

import TAP
import PriorityQueue

import random

for i in xrange( 100 ):
    q = PriorityQueue.PriorityQueue()
    test = []
    should = []
    for i in xrange( 10 ):
        should.append( i )
        test.append( i )
    random.shuffle( test )
    for i in test:
        q.insert( i )

    got = []
    done = False
    while not done:
        x = q.pop()
        if x is None:
            done = True
        else:
            got.append( x )

    TAP.isval( got, should )

TAP.done_testing()
