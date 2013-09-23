# import the rest of the package

try:
    import snippets
    import monoalphasubstitution
    import transposition
    import caesar
    import encoder
except ImportError:
    import pymaancrypt.snippets
    import pymaancrypt.monoalphasubstitution
    import pymaancrypt.transposition
    import pymaancrypt.caesar
    import pymaancrypt.encoder

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

    if printTotal:
        if totalfailed == 0:
            print("\nAll %d tests succeeded!" % (totalrun,))
        else:
            print("\nFailed %d of total %d testcases" % (totalfailed, totalrun))

    return (totalfailed, totalrun)

if __name__ == "__main__":
    run_all_tests(True)
