# csuf-autograder-base

## autograder_config.yml format

```
language: c++
test_framework: (googletest|blackbox)
linter: (true|false)
formatter: (true|false)
code:
- main: greeting/greeting.cpp
  [compile_points: 10]
  [linter_points: 5]
- main: hello_world/hello_world.cpp
  [compile_points: 10]
  [linter_points: 5]
- main: oops/oops.cpp
  [compile_points: 10]
  [linter_points: 5]
```