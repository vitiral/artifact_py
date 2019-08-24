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


[SPC-away]: https://this.goes.away.com
[SPC-away.subpart]: https://this.goes.away.com
