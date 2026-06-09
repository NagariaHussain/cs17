# assignments — graded assessment prep

Unlike the [worksheets](../worksheets/) (generated, non-graded practice), an
**assignment** is graded work. The student-facing version is **hand-written
markdown published on the cs17 wiki** — this folder is the *prep / scratch /
reference* side: seed-data generators, model solutions, and instructor
walkthroughs that back each published assignment.

## Layout

One folder per assignment, named `<slug>_<topic>/` where `<slug>` matches the
published wiki URL (e.g. `q1-p2` → `portal.cs17.org/student-handbook/assignments/q1-p2`):

```
assignments/
  <slug>_<topic>/
    README.md       # instructor walkthrough / answer key
    build_seed.py   # (optional) regenerates the starter/reference data
    references/      # seed data students start from + model solution
```

## Assignments

| Folder | Topic | Wiki slug |
|--------|-------|-----------|
| [`q1-p2_jugaad_inventory`](q1-p2_jugaad_inventory/) | Spreadsheet inventory: VLOOKUP / SUMIFS / IFS / conditional formatting / dashboard | `q1-p2` |

## Adding a new assignment

1. `mkdir assignments/<slug>_<topic>/references`
2. Draft the instructor walkthrough in `README.md`.
3. If the assignment ships starter data, add a `build_seed.py` that writes into
   `references/` (path relative to the script — see `q1-p2_jugaad_inventory/build_seed.py`).
4. Drop the model solution into `references/`.
5. Publish the student-facing markdown to the wiki; keep this folder as the source of truth for prep.
