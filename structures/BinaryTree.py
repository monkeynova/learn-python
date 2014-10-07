class Node:
    def __init__( self, key, value ):
        self.key = key
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        
    def _debug( self, indent ):
        print "%s%r (%r) = %r" % ( indent, self.key, self.parent and self.parent.key, self.value )

    def _assertValid( self ):
        if self.parent is not None:
            if self != self.parent.left and self != self.parent.right:
                raise Exception( "node is not a child of its parent" )

        self.left and self.left._assertValid()
        self.right and self.right._assertValid()
            
        
    def grandparent( self ):
        return self.parent and self.parent.parent

    def sibling( self ):
        if self.parent:
            if self.parent.left == self:
                return self.parent.right
            else:
                return self.parent.left

        return None

    def uncle( self ):
        return self.parent and self.parent.sibling()

class BinaryTree:
    def __init__( self, cmp=None ):
        self.root = None
        self.cmp = cmp or (lambda x, y: x < y)

    def _assertValid( self ):
        if self.root:
            if self.root.parent is not None:
                raise Exception( "root's parent is not none" )
            self.root._assertValid()

    def _heightNode( self, node ):
        if node is None:
            return 0
        else:
            return 1 + max( self._heightNode( node.left ), self._heightNode( node.right ) )

    def _height( self ):
        return self._heightNode( self.root )

    def _debugNoneNode( self, indent ):
        print "%sNone" % indent

    def _debugNode( self, node, indent ):
        if node is None:
            self._debugNoneNode( indent )
            return

        node._debug( indent )
        self._debugNode( node.left, "  " + indent )
        self._debugNode( node.right, "  " + indent )

    def _debug( self ):
        return self._debugNode( self.root, "" )

    def _makeNode( self, key, value ):
        return Node( key, value )

    def _onInsert( self, node ):
        return

    def _onDeleteSwap( self, toDelete, replacement ):
        return

    def _onDelete( self, deleted, replacement ):
        return

    def insert( self, key, value ):
        toInsert = self._makeNode( key, value )

        parent = None
        node = self.root

        while node is not None:
            if self.cmp( toInsert.key, node.key ):
                parent = node
                node = node.left
            else:
                parent = node
                node = node.right

        toInsert.parent = parent
        if parent == None:
            self.root = toInsert
        else:
            if self.cmp( toInsert.key, parent.key ):
                parent.left = toInsert
            else:
                parent.right = toInsert
        
        self._onInsert( toInsert )
        
    def _swap( self, node1, node2 ):
        if node1.parent is None:
            self.root = node2
        else:
            if node1.parent.left == node1:
                node1.parent.left = node2
            else:
                node1.parent.right = node2
        if node2.parent is None:
            self.root = node1
        else:
            if node2.parent.left == node2:
                node2.parent.left = node1
            else:
                node2.parent.right = node1

        node1.parent, node2.parent = node2.parent, node1.parent
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right

        for n in [ node1, node2 ]:
            if n.left is not None:
                n.left.parent = n
            if n.right is not None:
                n.right.parent = n

    def delete( self, key ):
        node = self._findNode( key )

        if node is None:
            return

        if node.right is not None and node.left is not None:
            find = node.right
            while find.left is not None:
                find = find.left
            self._swap( node, find )
            self._onDeleteSwap( node, find )

        replace = node.right or node.left

        if node.parent is None:
            self.root = replace
        else:
            if node.parent.left == node:
                node.parent.left = replace
            else:
                node.parent.right = replace

        if replace is not None:
            replace.parent = node.parent

        self._onDelete( node, replace )

    def _findNode( self, key ):
        node = self.root

        while node is not None:
            if node.key == key:
                return node

            if self.cmp( key, node.key ):
                node = node.left
            else:
                node = node.right

        return None
        
        
    def find( self, key ):
        node = self._findNode( key )

        if node is not None:
            return node.value

        return None
        
