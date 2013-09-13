# import the rest of the package

import monoalphasubstitution
import caesar
import encoder

def run_all_tests(printTotal=False):
    """
    This runs the entire test suite
    """
    totalfailed = 0
    totalrun = 0

    print("Running tests on encoder module... ", end='')
    result = encoder.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("OK")
        # if not OK the test will output the errors


    print("Running tests on monoalphasubstitution module... ", end='')
    result = monoalphasubstitution.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("OK")
        # if not OK the test will output the errors

        
    print("Running tests on caesar module... ", end='')
    result = caesar.testmodule()
    totalfailed += result[0]
    totalrun += result[1]
    if(result[0] == 0):
        print("OK")
        # if not OK the test will output the errors

    if printTotal:
        print("Failed %d of total %d testcases" % (totalfailed, totalrun))

    return (totalfailed, totalrun)

if __name__ == "__main__":
    run_all_tests(True)
