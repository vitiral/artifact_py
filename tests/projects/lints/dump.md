```yaml @
artifact:
    code_paths:
      - src/
      - script.py
    exclude_code_paths:
      - src/exclude/
      - src/ignore.py
    code_url:
      "https://github.com/vitiral/artifact_py/blob/master/tests/projects/lints/{file}#L{line}"
```

# Failing Lints (SPC-fail) {#SPC-fail}
```yaml @
partof:
  - SPC-dne
  - TST-hi

subparts:
  - subpart
```
This artifact is has a partof that does not exist.

# Some Test (TST-hi) {#TST-hi}
This is a test

[@SPC-fail.subpart]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/lints/script.py#L3
[@SPC-fail]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/lints/script.py#L2
[@SPC-simple.deep]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/lints/src/deep/deep.py#L1
[@SPC-simple.script]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/lints/script.py#L1
[@SPC-simple.simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/lints/src/simple.py#L2
[@SPC-simple.tst-simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/lints/src/simple.py#L2
[@SPC-simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/lints/src/simple.py#L4
[SPC-fail.subpart]: #SPC-fail.subpart
[SPC-fail]: #SPC-fail
[TST-hi]: #TST-hi
