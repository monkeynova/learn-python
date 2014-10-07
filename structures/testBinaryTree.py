#!/usr/bin/env python

import BinaryTree
import RedBlackTree
import TAP
import random

TAP.note( "Binary Tree: sorted" )

t = BinaryTree.BinaryTree()
for i in xrange( 10 ):
    t.insert( i, 2 * i )

TAP.note( "Height is %d" % t._height() )

TAP.isval( t.find( 1 ), 2 )
TAP.isval( t.find( 5 ), 10 )
TAP.isval( t.find( 0 ), 0 )
TAP.isval( t.find( 9 ), 18 )

TAP.note( "Binary Tree: Optimal insert order" )

t = BinaryTree.BinaryTree()
for i in [ 5, 2, 8, 0, 1, 3, 4, 6, 7, 9 ]:
    t.insert( i, 2 * i )

TAP.note( "Height is %d" % t._height() )

for i in [ 5, 2, 8, 0, 1, 3, 4, 6, 7 ]:
    TAP.isval( t.find( i ), 2 * i )
    t.delete( i )
    TAP.isnt( t.find( i ), 2 * i )
    TAP.isval( t.find( 9 ), 18 )

TAP.note( "Binary Tree: Optimal insert order with deletes" )

t = BinaryTree.BinaryTree()
for i in [ 5, 2, 8, 0, 1, 3, 4, 6, 7, 9 ]:
    t.insert( i, 2 * i )

TAP.note( "Height is %d" % t._height() )
    
for i in xrange( 10 ):
    TAP.isval( t.find( i ), 2 * i )
    t.delete( i )
    TAP.isnt( t.find( i ), 2 * i )
    for j in xrange( 10 - i - 1 ):
        TAP.isval( t.find( i + j + 1 ), 2 * (i + j + 1) )

TAP.note( "RB Tree sort" )

t = RedBlackTree.RedBlackTree()
for i in xrange( 10 ):
    t.insert( i, 2 * i )
    t._assertValid()

TAP.note( "Height is %d" % t._height() )

TAP.isval( t.find( 1 ), 2 )
TAP.isval( t.find( 5 ), 10 )
TAP.isval( t.find( 0 ), 0 )
TAP.isval( t.find( 9 ), 18 )

TAP.note( "RB Tree reverse sort" )

t = RedBlackTree.RedBlackTree()
for i in xrange( 10 ):
    t.insert( 9 - i, 2 * (9 - i) )
    t._assertValid()

TAP.note( "Height is %d" % t._height() )

TAP.isval( t.find( 1 ), 2 )
TAP.isval( t.find( 5 ), 10 )
TAP.isval( t.find( 0 ), 0 )
TAP.isval( t.find( 9 ), 18 )

TAP.note( "RedBlack Tree: sorted insert order with deletes" )

t = RedBlackTree.RedBlackTree()
for i in xrange( 10 ):
    t.insert( i, 2 * i )

TAP.note( "Height is %d" % t._height() )
    
for i in xrange( 10 ):
    TAP.isval( t.find( i ), 2 * i )
    t.delete( i )
    TAP.isnt( t.find( i ), 2 * i )
    for j in xrange( 10 - i - 1 ):
        TAP.isval( t.find( i + j + 1 ), 2 * (i + j + 1) )
    t._assertValid()


t = RedBlackTree.RedBlackTree()
dict = []
for i in xrange( 101 ):
    dict.append( None )

for i in xrange( 10000 ):
    randitem = random.randint( 0, 100 )
    if dict[randitem] is not None:
        TAP.isval( t.find( randitem ), dict[randitem] )
        t.delete( randitem )
        TAP.isval( t.find( randitem ), None )
        dict[randitem] = None
    else:
        TAP.isval( t.find( randitem ), None )
        t.insert( randitem, randitem * 2 )
        TAP.isval( t.find( randitem ), randitem * 2 )
        dict[randitem] = randitem * 2
    if i % 1000 == 0:
        TAP.note( "Height is %d" % t._height() )

TAP.done_testing()
