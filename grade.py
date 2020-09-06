from autograder import Autograder
import getopt, json, os, shutil, sys

def main(DEBUG=False, TEST_ENV=False):
    CWD = os.getcwd()
    sys.path.append(CWD)
    TMP_FOLDER = os.path.join(CWD, 'tmp')
    STUDENT_SRC_FOLDER = os.path.join(TMP_FOLDER, 'src')
    BUILD_FOLDER = os.path.join(TMP_FOLDER, 'build')

    # copy student code from /autograder/submission to a temp folder
    if os.path.exists(TMP_FOLDER):
        shutil.rmtree(TMP_FOLDER)
    if TEST_ENV:
        shutil.copytree('/home/ubuntu/autograder/submission/', STUDENT_SRC_FOLDER)
    else:
        shutil.copytree('/autograder/submission/', STUDENT_SRC_FOLDER)
    os.mkdir(BUILD_FOLDER)

    # create new autograder object from config
    autograder = Autograder("../autograder_config.yml", STUDENT_SRC_FOLDER, BUILD_FOLDER)

    # try to compile student code -- results are in autograder.compiler.results
    autograder.compiler.compile()
    if DEBUG:
        print("Failed to compile: {}".format(autograder.compiler.get_failures()))
        print(autograder.compiler.results)
    with open(os.path.join(TMP_FOLDER, 'compile_commands.json'), 'w+') as outfile:
        json.dump(autograder.compiler.compile_commands, outfile)

    # run linter
    if autograder.linter:
        autograder.linter.run_test()
        if DEBUG:
            print(autograder.linter.results)

    # run formatter

    # run test cases (get json output from googletest)
    autograder.tester.run_test(failed=autograder.compiler.get_failures())
    if DEBUG:
        print(autograder.tester.results)

    if TEST_ENV:
        outfile_path = '/home/ubuntu/autograder/results/results.json'
    else:
        outfile_path = '/autograder/results/results.json'

    # create json object with overall results and write to results directory
    with open(outfile_path, 'w+') as outfile:
        outfile.write(autograder.make_json())


if __name__ == '__main__':
    debug = False
    test_env = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],"dt")
    except getopt.GetoptError:
        print('grade.py -d <debug flag> -t <test env flag>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-d':
            debug = True
        if opt == '-t':
            test_env = True
    main(DEBUG=debug, TEST_ENV=test_env)
