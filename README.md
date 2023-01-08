# iograft Types and Nodes for fileseq

This repository contains types and nodes for interacting with file sequences using the `fileseq` library from justinfx: [https://github.com/justinfx/fileseq](https://github.com/justinfx/fileseq).

These types/nodes depend on the `fileseq` package being installed (i.e. with pip).

## Adding the fileseq nodes/types to an environment

To use these nodes/types the following additions need to be made to the environment you would like to use the nodes in:
- Update the `Python Path` to include the path of the `fileseq` package.
- Update the `Python Path` to include the `types` directory of this repository.
- Update the `Plugin Path` to include the `types` and `nodes` directories of this repository.

*NOTE* Using these nodes does NOT require a new environment.

## fileseq Types

Two new types are added in this repository:
- FrameSet - wrapper around the `fileseq.FrameSet` class.
- FileSequence - wrapper around the `fileseq.FileSequence` class.

Both of these added types support being set directly from the UI via an input string. For a `FrameSet` this might look like "1-200". For `FileSequence` types, iograft adds a new ToString function that formats a sequence similarly to what can be found in the Nuke file browser (i.e. `/projects/iograft/render/octopus_ceramic.####.exr (1-100)`).
