```yaml @
artifact:
    root_dir: "./"
    code_paths:
        - src/
    exclude_code_paths: []
```

# Simple Artifact (SPC-simple) {#SPC-simple}
```yaml @
partof: []
done: null
subparts:
- foo
- bar
```

This is a simple, but complete, design document with two artifacts.

You can link to other artifacts with [SPC-other], or to subparts with
[SPC-simple.foo]. The link table will be automatically generated when this
artifact is exported.

# Other Artifact (SPC-other) {#SPC-other}
This is another artifact for demonstration purposes.
