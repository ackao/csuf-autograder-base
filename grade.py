"""
Main entrypoint for autograder
"""
import getopt
import json
import os
import shutil
import sys

from autograder import Autograder

def main():
    """
    Main entrypoint for autograder
    """

    cwd = os.getcwd()
    sys.path.append(cwd)
    tmp_folder = os.path.join(cwd, 'tmp')
    student_src_folder = os.path.join(tmp_folder, 'src')
    build_folder = os.path.join(tmp_folder, 'build')

    # copy student code from /autograder/submission to a temp folder
    if os.path.exists(tmp_folder):
        shutil.rmtree(tmp_folder)
    if TEST_ENV:
        shutil.copytree('/home/ubuntu/autograder/submission/', student_src_folder)
    else:
        shutil.copytree('/autograder/submission/', student_src_folder)
    os.mkdir(build_folder)

    # create new autograder object from config
    autograder = Autograder("../autograder_config.yml", student_src_folder, build_folder)

    # try to compile student code -- results are in autograder.compiler.results
    autograder.compiler.compile()
    if DEBUG:
        print("Failed to compile: {}".format(autograder.compiler.get_failures()))
        print(autograder.compiler.results)
    with open(os.path.join(tmp_folder, 'compile_commands.json'), 'w+') as outfile:
        json.dump(autograder.compiler.compile_commands, outfile)

    # run linter
    if autograder.linter:
        autograder.linter.run_test()
        if DEBUG:
            print(autograder.linter.results)

    # run formatter

    # run test cases (get json output from googletest)
    autograder.tester.set_skip(autograder.compiler.get_failures())
    autograder.tester.run_test()
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
    DEBUG = False
    TEST_ENV = False
    try:
        for opt, _ in getopt.getopt(sys.argv[1:], "dt")[0]:
            if opt == '-d':
                DEBUG = True
            if opt == '-t':
                TEST_ENV = True
    except getopt.GetoptError:
        print('grade.py -d <DEBUG flag> -t <test env flag>')
        sys.exit(2)
    main()
