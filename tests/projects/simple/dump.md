```yaml @
artifact:
    code_paths:
      - src/
      - script.py
    exclude_code_paths:
      - src/exclude/
      - src/ignore.py
    code_url:
      "https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/{file}#L{line}"
```

# Simple Test Doc (SPC-simple) {#SPC-simple}
```yaml @
subparts:
  - simple
  - script
  - deep
  - tst-simple
  - tst-exclude
  - tst-ignore
```
Simple with some code links


# Not implemented (SPC-notimpl) {#SPC-notimpl}
```yaml @
partof:
  - SPC-simple
```

[@SPC-simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/src/simple.py#L4
[@SPC-simple.deep]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/src/deep/deep.py#L1
[@SPC-simple.script]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/script.py#L1
[@SPC-simple.simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/src/simple.py#L2
[@SPC-simple.tst-simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/src/simple.py#L2
