#!/usr/bin/env python

import SubsetGenerator
import sys

for t in SubsetGenerator.SubsetGeneratorSize( 10, 1 ):
    print "%r" % t

for t in SubsetGenerator.SubsetGeneratorSize( 10, 2 ):
    print "%r" % t

for t in SubsetGenerator.SubsetGenerator( 3 ):
    print "%r" % t
