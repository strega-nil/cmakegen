cmakegen
---

This is a basic little program, similar to `cargo-new`. Basic use is just

```
cmakegen project-name
```

to create an executable project named `project-name`
(although that's not a valid project name -
project names must be valid C++ identifiers)
In order to create a library, or header only library project,
use `--kind=library` or `--kind=headers`, respectively.

You can also choose between the C++ standards with `--std=14` or `17`;
the default is `14`.
