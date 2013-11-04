# import the rest of the package

# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "pymaancrypt"
    import pymaancrypt

from . import snippets
from . import mathfuncs
from . import monoalphasubstitution
from . import transposition
from . import caesar
from . import encoder
from . import onetimepad
from . import rsa
from . import blockmodes

def run_all_tests(printTotal=False):
    """
    This runs the entire test suite
    """
    totalfailed = 0
    totalrun = 0

    print("Running tests on snippets module... ")
    result = snippets.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors

    print("Running tests on mathfuncs module... ")
    result = mathfuncs.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors


    print("Running tests on encoder module... ")
    result = encoder.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors


    print("Running tests on monoalphasubstitution module... ")
    result = monoalphasubstitution.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors


    print("Running tests on transposition module... ")
    result = transposition.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors

        
    print("Running tests on caesar module... ")
    result = caesar.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors
        
    print("Running tests on onetimepad module... ")
    result = onetimepad.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors
        
    print("Running tests on rsa module... ")
    result = rsa.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors
        
    print("Running tests on blockmodes module... ")
    result = blockmodes.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("\tOK (%d tests)" % (result[1],))
        # if not OK the test will output the errors

    if printTotal:
        if totalfailed == 0:
            print("\nAll %d tests succeeded!" % (totalrun,))
        else:
            print("\nFailed %d of total %d testcases" % (totalfailed, totalrun))

    return (totalfailed, totalrun)



if __name__ == "__main__":
    run_all_tests(True)
