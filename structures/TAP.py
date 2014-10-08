testnum = 0

import sys

def no_plan():
    print "1.."

def plan( planNum ):
    print "1..%d" % planNum

def done_testing():
    global testnum
    plan( testnum )

def note( str ):
    print "# %s" % str

def diag( str ):
    sys.stderr.write( "# %s\n" % str )

def ok( message=None ):
    global testnum
    testnum += 1
    if message:
        message = "# " + message
    else:
        message = ""
    print "ok %d%s" % ( testnum, message )
    return True

def fail( message=None ):
    global testnum
    testnum += 1
    if message:
        message = "# " + message
    else:
        message = ""
    print "not ok %d%s" % ( testnum, message )
    return False

def isval( a, b, message=None ):
    if a == b:
        return ok( message )
    else:
        fail( message )
        diag( "  Values differ" )
        diag( "  got=%r" % a )
        diag( "  expected=%r" % b )
        return False

def isnt( a, b, message=None ):
    if a != b:
        return ok( message )
    else:
        fail( message )
        diag( "  Values are the same" )
        diag( "  got=expected=%r" % a )
        return False
