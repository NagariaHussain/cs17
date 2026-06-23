# Rung 1 — a function

> The ledger is still a list of rows. But you no longer touch it directly — you
> go through `post()`, and `post()` won't let an unbalanced transaction in.

```sh
python ledger.py
```

## What changed

```python
def post(*lines):
    debits  = sum(d for _, d, _ in lines)
    credits = sum(c for _, _, c in lines)
    if debits != credits:
        raise ValueError("Refusing to post.")
    gl.extend(lines)
```

The same typo from Rung 0 is now **caught the instant you post it**, with the
offending transaction right in front of you — not 3,000 rows later in a broken
report.

## The idea (named only now that you've felt the need for it)

**Procedural abstraction.** A function is a *name that hides steps* — but the
deeper point here is that it can *guard an invariant*. `post` is the only door
into the ledger, so "debits == credits" is true of every transaction by
construction. You can't forget the rule, because the rule is the door.

Note what did **not** change: the trial balance code is identical to Rung 0. The
*data* is still loose tuples. That's the next pain →

## The next pain

The balancing rule lives in `post()`, off to the side. The data (the rows)
lives somewhere else. If you build a transaction by hand and want to ask "is
this balanced?" *before* posting it, you can't — there's no transaction
*object* to ask. The rule and the data have drifted apart.

➡️ [Rung 2 — objects](../rung2_objects/)
