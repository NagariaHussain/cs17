# Rung 9 — fixing mistakes without lying

> Rung 8 could create, list and open invoices — but once one was wrong (wrong
> customer, wrong amount) you were stuck: the general ledger is **append-only**,
> so you can't `UPDATE` or `DELETE` a posted fact without lying about what
> happened. Here we add the honest fix: **cancel** an invoice by posting a
> reversing entry that nets it to zero, and **amend** it by cancelling the old
> version and creating a new one linked back to it.

```sh
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Then visit http://localhost:5000/invoices

## What changed

Two new routes on the invoice document, plus one extra column to remember
lineage:

```python
CREATE TABLE sales_invoice (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    customer     TEXT    NOT NULL,
    amount       INTEGER NOT NULL,
    status       TEXT    NOT NULL DEFAULT 'Posted',
    entry_no     INTEGER NOT NULL,   -- the GL entry it emitted
    amended_from INTEGER             -- the invoice this one supersedes, if any
)
```

- **Cancel** (`POST /invoices/<id>/cancel`) — only a `Posted` invoice can be
  cancelled. We read the original GL entry with `get_ledger().entry(entry_no)`,
  post its `.reversed("Cancel: Sales Invoice — <customer>")` (debits and credits
  swapped, so the net effect on the books is zero), then flip the document's
  `status` to `Cancelled`. Redirects back to the detail page.
- **Amend** (`GET,POST /invoices/<id>/amend`) — the GET renders a form prefilled
  with the current customer and amount (in ₹). The POST validates, **cancels the
  old** invoice (reversing entry + status flip), then `create_invoice(...)` for
  the **new** values with `amended_from=<old id>`. Net GL effect: the new invoice
  only. Redirects to the new invoice's detail.

The detail page now shows action buttons — **Cancel** (`btn-danger`, a POST
form) and **Amend** (`btn-secondary` link) — but *only while the invoice is
`Posted`*. A cancelled or superseded invoice is frozen history with no buttons.
If `amended_from` is set it shows "Amended from #n"; if a later invoice points
back at this one it shows "Amended to #m".

The key distinction, made on purpose: **the GL ledger is append-only — we never
`UPDATE` or `DELETE` a `gl_entry` row.** A cancellation or amendment is a *new*
entry, not an edit. What we *do* update is the **document's workflow `status`**
(`Posted` → `Cancelled`) — and that's fine, because status is a web-layer
workflow state, not an accounting fact. The accounting facts (the GL rows) stay
immutable; only the doctype's bookkeeping of "is this version still live?"
changes.

## The idea

**Corrections are new facts, never edits or deletes.** This cashes in Rung 5's
append-only `gl_entry` table and `JournalEntry.reversed()`: to undo a posting you
post its mirror image, and to change it you undo-then-redo. That's the honest
**U and D of CRUD for accounting** — there is no in-place update or destructive
delete on the ledger, because a real set of books records *what happened*, and
unhappening something is itself something that happened. The audit trail stays
intact: you can still open the cancelled invoice, see its original entry, and see
the reversing entry that voided it.

## The next pain

Anyone can now post, cancel, or amend, and the ledger faithfully records *what*
happened — but not *who* did it. There's no accountability: no user behind a
posting, no trail of who voided that ₹50,000 invoice. A real ledger has to name
the person responsible.

➡️ [Rung 10 — who posted this?](../rung10_users/)

⬅️ [Rung 8](../rung8_list_detail/)
