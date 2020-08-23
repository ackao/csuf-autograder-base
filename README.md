# csuf-autograder-base

C++ Autograder for CSUF, compatible with Gradescope

End users please see https://github.com/ackao/csuf-autograder-template instead -- do not clone this repo manually.

## Features

* Compile and test multiple executables with multiple source files
* Configure visibility of test cases
* Blackbox testing (give input on stdin; check stdout and/or exit code)
* Optional: Check for Linter warnings via clang-tidy
* Assign weights for test cases; optional: assign points for compilation and/or linter as well

## Coming Soon

* Googletest unit test support 
* Diff student code with clang-format output

## Maybe implemented one day

* Support for other languages
* Ability to register custom grading workflows

Feel free to file pull requests or feature requests
