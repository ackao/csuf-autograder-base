# csuf-autograder-base

C++ Autograder for CSUF, compatible with Gradescope

End users please see https://github.com/ackao/csuf-autograder-template instead -- do not clone this repo manually.

## Features
* Compile and test multiple executables with multiple source files
* Configure visibility of test cases
* Assign weights for test cases; optional: assign points for compilation and/or linter as well

### C++
* Blackbox testing (give input on stdin; check stdout and/or exit code)
* Optional: Check for Linter warnings via clang-tidy
* Optional: Style check by diffing student code with clang-format output

## Coming Soon
* Googletest unit test support 

## Maybe implemented one day
* Support for other languages
* Ability to register custom grading workflows

Feel free to file feature requests

## Development and Testing -- Pull requests welcome!
1. Make a branch for your own feature. Do not commit directly to the `dev` branch.
1. Implement feature, test it locally, and send pull request to merge it into `dev` branch when ready.
1. Make a test course/assignment on Gradescope and test the `dev` version of the autograder (see below)
1. Send pull request to merge `dev` into `master`

### Dev environment
Log into https://ide.cs50.io/ and clone this repo. Also create the necessary directory structore for local testing:
```
~/
    autograder/             # pretends to be gradescope's /autograder dir
        results/              
        submission/         # test "student" code goes here
    csuf-autograder-base/   # the git repo and everything in it 
    autograder_config.yml   # config file needs to live here
```

Testing can now be done via:
```
$ python3 grade.py -t
```
Add the `-d` flag for debug output:
```
$ python3 grade.py -d -t
```

### Testing on Gradescope
1. Generate a repo from https://github.com/ackao/csuf-autograder-template and create the YAML config as usual
1. Change `run_autograder` to check out and fetch the `dev` branch:
    ```
    #!/usr/bin/env bash

    cd /autograder/source/csuf-autograder-base
    git checkout dev
    git fetch --all
    git reset --hard origin/dev
    python3 grade.py
    ```
1. Upload autograder to Gradescope. Now, hitting "Regrade assignment" will automatically fetch new changes from dev.

### Adding new languages

Create a directory for your new language called `($language)_tester`.

In that directory, implement classes that inherit from the following and override their unimplemented entrypoint functions:
* compiler.py (compile the code and give points if it compiles)
* linter.py (for any style/linter passes)
* test_runner.py (for running test cases)

When parsing the YAML config, try and reuse existing fields if possible. 

In autograder.py, add a case to the `cfg['language']` check and initialize instances of your classes.
