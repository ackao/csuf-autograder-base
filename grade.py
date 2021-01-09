"""
Main entrypoint for autograder
"""
import getopt
import json
import os
import shutil
import sys

from autograder import Autograder
from util import copy_dir_if_exists, recursive_copy_with_overwrite

def main():
    """
    Main entrypoint for autograder
    """

    cwd = os.getcwd()
    sys.path.append(cwd)
    tmp_folder = os.path.join(cwd, 'tmp')
    student_src_dir = os.path.join(tmp_folder, 'src')
    build_dir = os.path.join(tmp_folder, 'build')
    replacements_dir = os.path.join(os.path.dirname(cwd), 'replacements')
    test_dir = os.path.join(tmp_folder, 'test')

    # copy student code from /autograder/submission to a temp folder
    if os.path.exists(tmp_folder):
        shutil.rmtree(tmp_folder)
    if TEST_ENV:
        # shutil.copytree('/home/ubuntu/autograder/submission/', student_src_dir)
        shutil.copytree('/home/pinventado/code/ag/autograder/submission/', student_src_dir)
    else:
        shutil.copytree('/autograder/submission/', student_src_dir)

    if os.path.exists(replacements_dir):
        recursive_copy_with_overwrite(replacements_dir, student_src_dir)

    os.mkdir(build_dir)

    # copy googletest cases into tmp folder
    copy_dir_if_exists('../tests', test_dir)

    # create new autograder object from config
    autograder = Autograder("../autograder_config.yml", student_src_dir, build_dir, test_dir)

    # try to compile student code -- results are in autograder.compiler.results
    if autograder.compiler:
        autograder.compiler.compile()
        if DEBUG:
            print("Failed to compile: {}".format(autograder.compiler.get_failures()))
            print(autograder.compiler.results)
        with open(os.path.join(tmp_folder, 'compile_commands.json'), 'w+') as outfile:
            json.dump(autograder.compiler.compile_commands, outfile)

    # run linter
    if autograder.linter:
        autograder.linter.run()
        if DEBUG:
            print(autograder.linter.results)

    # run style check
    if autograder.stylecheck:
        autograder.stylecheck.run()
        if DEBUG:
            print(autograder.stylecheck.results)

    # run test cases (get json output from googletest)
    if autograder.compiler:
      autograder.tester.set_skip(autograder.compiler.get_failures())
    autograder.tester.run_test()
    if DEBUG:
        print(autograder.tester.results)

    if TEST_ENV:
        # outfile_path = '/home/ubuntu/autograder/results/results.json'
        outfile_path = '/home/pinventado/code/ag/autograder/results/results.json'
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
