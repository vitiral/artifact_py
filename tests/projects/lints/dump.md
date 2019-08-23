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

done: should not be done, but is
```
This artifact is has a partof that does not exist.

Some references that don't exist
[SPC-dne]
[SPC-dne.code]
[@SPC-dne]
[@SPC-dne.code]

And one that does
[TST-hi]


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
