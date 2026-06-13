# output/

This directory holds **all generated artifacts** produced by the demos and
experiments, so the source tree stays clean.

Typical contents:

| File | Description |
|------|-------------|
| `*.btml` | The planned behavior tree in BTML text format |
| `*.dot`  | Graphviz source of the behavior tree |
| `*.png`  | Rendered behavior tree image (raster) |
| `*.svg`  | Rendered behavior tree image (vector) |

These files are regenerated on every run and are ignored by Git
(see `.gitignore`). You can safely delete anything here.

The output directory is resolved at runtime via
`btpg.utils.path.get_output_path()`, which always points to
`<repo_root>/output` and creates it if needed.
