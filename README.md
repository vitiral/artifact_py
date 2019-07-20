# Artifact-py: a reimagining of [artifact]

This is a reimplementation of [artifact]. It will be the barebones of artifact
necessary to put it in a build system. No featureful cli, no web-ui. Just
parsing and exporting of json/markdown/etc.

At the same time, this is not a strict rewrite. It is a reimagining and will probably guide
the development of artifact 3.0. The primary differences will be:
- The use of the new [anchor_txt] markdown attribute format, developed
  specifically for this project
- Removal of `.art/settings.toml`, replaced with an attribute block at the top
  of the root artifact file.
- A few minor tweaks to simplify how artifacts are specified and linked.

[artifact]: https://github.com/vitiral/artifact
[anchor_txt]: https://github.com/vitiral/anchor_txt


# Design (SPC-design) {#SPC-design}
```yaml @
artifact:
  root_dir: './'

  code_paths:
    - artifact_py/
    - tests/

  exclude_code_paths:
    - tests/artifacts_only/
    - tests/projects/
    - tests/test_code.py


  code_url:
    "https://github.com/vitiral/artifact/blob/master/{file}#L{line}"

subparts:
  - artifact
  - settings
  - code
```

## Settings (#SPC-design.settings}
Artifacts are injected from the `--doc` markdown design document. All
settings/attributes are provided using the [anchor_txt] format. Settings
are provided by adding the following to an `artifact` attribute anywhere
in the document:

- `root_dir`: the root directory when creating paths. This will affect
  where other path settings use as a reference.
- `code_paths`: paths to files or directories to look for code.
  See [Code Links](#SPC-design.code) for more information.
- `exclude_code_paths`: paths to exclude when searching for artifacts.


## Artifact {#SPC-design.artifact}
An artifact is a piece of documentation that can be linked to other pieces of
documentation and to source code. It has the following attributes:

- `name`: defines how it can be linked. The name is defined in the
  anchor header (`{#REQ-foo}`)
  - There are three types of artifacts: REQ (requirement), SPC (specification),
    TST (test)
- `partof`: the other artifacts this artifact is a partof.
- `subparts`: pieces of an artifact that can be linked in code.
- `done`: force an artifact to be considered specified and tested


## Code Links {#SPC-design.code}
Artifacts are linked in code by:
- Defining an artifact name or subpart
- Specifying `code_paths` in [Settings](#SPC-design.settings)
- Putting a tag anywhere in code of the form:
  - `#SPC-foo`
  - `#SPC-foo.bar`

Artifact will run a regular expression over all files found in `code_paths` and
will mark artifacts as specified/tested if they are linked in code.


# License

The source code is Licensed under either of

* Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
  http://www.apache.org/licenses/LICENSE-2.0)
* MIT license ([LICENSE-MIT](LICENSE-MIT) or
  http://opensource.org/licenses/MIT)

at your option.

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.

[SPC-design.artifact]: https://github.com/vitiral/artifact/blob/master/artifact_py/artifact.py#L28

