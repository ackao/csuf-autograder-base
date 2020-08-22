# csuf-autograder-base

## example autograder_config.yml format

```
language: c++
linter: true
formatter: true
code:
- main: greeting/greeting.cpp
  compile_points: 10
  linter_points: 5
- main: hello_world/hello_world.cpp
  compile_points: 10
  linter_points: 5
- main: oops/oops.cpp
  compile_points: 10
  linter_points: 5
test_framework: blackbox

blackbox_tests:
- test_name: "greeting test"
  test_types:
    - output
  obj: greeting
  stdin: Bob
  stdout: "Hi, what's your name?\nHello, Bob!\n"
  points: 5
- test_name: "greeting test 2"
  test_types:
    - output
  obj: greeting
  stdin: Alice
  stdout: "Hi, what's your name?\nHello, Alice!\n"
  points: 5
- test_name: "greeting exit code test"
  test_types:
    - exitcode
  obj: greeting
  stdin: Alice
  exitcode: 0
  points: 10
- test_name: "oops exit code test"
  test_types:
    - exitcode
  obj: oops
  exitcode: 1
  points: 5
- test_name: "oops output test"
  test_types:
    - output
  obj: oops
  stdout: ""
  points: 5
- test_name: "hello_world output test"
  test_types:
    - output
  obj: hello_world
  stdout: "Hello, everyone!\n"
  points: 5
- test_name: "hello_world exit code test"
  test_types:
    - exitcode
  obj: hello_world
  exitcode: 0
  points: 5
```