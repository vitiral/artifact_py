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

# Done (SPC-done) {#SPC-done}
```yaml @
partof:
  - SPC-simple

done: "yes"
```

This is done by default

[@SPC-simple.deep]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/src/deep/deep.py#L1
[@SPC-simple.script]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/script.py#L1
[@SPC-simple.simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/src/simple.py#L2
[@SPC-simple.tst-simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/src/simple.py#L2
[@SPC-simple]: https://github.com/vitiral/artifact_py/blob/master/tests/projects/simple/src/simple.py#L4
[SPC-done]: #SPC-done
[SPC-notimpl]: #SPC-notimpl
[SPC-simple.deep]: #SPC-simple.deep
[SPC-simple.script]: #SPC-simple.script
[SPC-simple.simple]: #SPC-simple.simple
[SPC-simple.tst-exclude]: #SPC-simple.tst-exclude
[SPC-simple.tst-ignore]: #SPC-simple.tst-ignore
[SPC-simple.tst-simple]: #SPC-simple.tst-simple
[SPC-simple]: #SPC-simple
