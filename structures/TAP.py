testnum = 0

def no_plan():
    print "1.."

def plan( planNum ):
    print "1..%d" % planNum

def done_testing():
    global testnum
    plan( testnum )

def note( str ):
    print "# %s" % str

def ok( message=None ):
    global testnum
    testnum += 1
    if message:
        message = "# " + message
    else:
        message = ""
    print "ok %d%s" % ( testnum, message )

def fail( message=None ):
    global testnum
    testnum += 1
    if message:
        message = "# " + message
    else:
        message = ""
    print "not ok %d%s" % ( testnum, message )

def isval( a, b, message=None ):
    if a == b:
        ok( message )
    else:
        fail( message )

def isnt( a, b, message=None ):
    if a != b:
        ok( message )
    else:
        fail( message )
