import BinaryTree

class Node(BinaryTree.Node):
    def __init__( self, key, value ):
        BinaryTree.Node.__init__( self, key, value )
        self.color = "red"

    def _debug( self, indent ):
         print "%s%r(%r,%r) = %r" % ( indent, self.key, self.color, self.parent and self.parent.key, self.value ) 

class RedBlackTree(BinaryTree.BinaryTree):
    def _debugNoneNode( self, indent ):
        print "%sNone (black)" % indent
        
    def _countBlack( self, node ):
        if node is None:
            return 1

        base = 0
        if node.color == "black":
            base = 1
        else:
            if node.left is not None and node.left.color == "red":
                self._debug()
                raise Exception( "red node with red child" )
            if node.right is not None and node.right.color == "red":
                self._debug()
                raise Exception( "red node with red child" )

        leftCount = self._countBlack( node.left )
        rightCount = self._countBlack( node.right )

        if leftCount != rightCount:
            self._debug()
            raise Exception( "countBlack mismatch %d != %d" % (leftCount, rightCount ) )

        return leftCount + base

    def _assertValid( self ):
        BinaryTree.BinaryTree._assertValid( self )
        self._countBlack( self.root )
        return

    def _makeNode( self, key, value ):
        return Node( key, value )

    def _rotateLeft( self, node ):
        parent = node.parent

        newNode = node.right
        newLeft = node

        if parent is None:
            self.root = newNode
        elif node == parent.left:
            parent.left = newNode
        else:
            parent.right = newNode

        oldLeft = None

        newNode.parent = parent

        oldLeft = newNode.left
        
        newNode.left = newLeft
        newLeft.parent = newNode

        newLeft.right = oldLeft
        if oldLeft is not None:
            oldLeft.parent = newLeft
            
    def _rotateRight( self, node ):
        parent = node.parent

        newNode = node.left
        newRight = node

        if parent is None:
            self.root = newNode
        elif node == parent.left:
            parent.left = newNode
        else:
            parent.right = newNode

        newNode.parent = parent

        oldRight = newNode.right
        
        newNode.right = newRight
        newRight.parent = newNode

        newRight.left = oldRight
        if oldRight is not None:
            oldRight.parent = newRight
    
    def _onInsertFix( self, node ):
        if node.parent is None:
            node.color = "black"
            return

        if node.parent.color == "black":
            # all is well
            return

        uncle = node.uncle()
        grandparent = node.grandparent()
        if uncle is not None and uncle.color == "red":
            node.parent.color = "black"
            uncle.color = "black"
            grandparent.color = "red"
            self._onInsertFix( grandparent )
            return
        
        if node == node.parent.right and node.parent == grandparent.left:
            self._rotateLeft( node.parent )
            node = node.left
        elif node == node.parent.left and node.parent == grandparent.right:
            self._rotateRight( node.parent )
            node = node.right

        node.parent.color = "black"
        grandparent.color = "red"
        if node == node.parent.left:
            self._rotateRight( grandparent )
        else:
            self._rotateLeft( grandparent )

    def _onInsert( self, node ):
        #print "onInsert( %r (%s) )" % ( node.key, node.color )

        self._onInsertFix( node )
        self._assertValid()

    def _onDeleteSwap( self, toDelete, replacement ):
        #print "onDeleteSwap( %r, %r )" % ( toDelete.key, replacement.key )
        toDelete.color, replacement.color = replacement.color, toDelete.color

    def _onDeleteFix( self, deleted, replacement ):
        if deleted.color == "red":
            return

        if replacement is not None and replacement.color == "red":
            replacement.color = "black"
            return

        parent = None
        if replacement:
            parent = replacement.parent
        else:
            parent = deleted.parent

        if parent is None:
            # New root
            return

        sibling = parent.left
        if sibling == replacement:
            sibling = parent.right
        
        if sibling and sibling.color == "red":
            parent.color = "red"
            sibling.color = "black"
            if replacement == parent.left:
                self._rotateLeft( parent )
            else:
                self._rotateRight( parent )

            sibling = parent.left
            if sibling == replacement:
                sibling = parent.right

        siblingAllBlack = True # after sibling == "red" check
        if sibling:
            for sc in [ sibling.left, sibling.right ]:
                siblingAllBlack = siblingAllBlack and (sc is None or sc.color == "black")

        if siblingAllBlack:
            sibling.color = "red"

            if parent.color == "black":
                self._onDeleteFix( deleted, parent )
            else:
                parent.color = "black"

            return
        
        # Sibling is black. exactly one red child
        if replacement == parent.left and sibling.left and sibling.left.color == "red":
            sibling.color = "red"
            sibling.left.color = "black"
            self._rotateRight( sibling )
            sibling = sibling.parent # got rotated out
        elif replacement == parent.right and sibling.right and sibling.right.color == "red":
            sibling.color = "red"
            sibling.right.color = "black"
            self._rotateLeft( sibling ) 
            sibling = sibling.parent # Got rotated out

        sibling.color = parent.color
        parent.color = "black"

        if replacement == parent.left:
            if sibling.right:
                sibling.right.color = "black"
            self._rotateLeft( parent )
        else:
            if sibling.left:
                sibling.left.color = "black"
            self._rotateRight( parent )
    

    def _onDelete( self, deleted, replacement ):
        #print "onDelete( %r (%s), %r (%s) )" % ( deleted and deleted.key, deleted and deleted.color or "black", replacement and replacement.key, replacement and replacement.color or "black" )
        self._onDeleteFix( deleted, replacement )
        self._assertValid()

