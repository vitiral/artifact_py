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

[SPC-away]: https://this.goes.away.com
[SPC-away.subpart]: https://this.goes.away.com
