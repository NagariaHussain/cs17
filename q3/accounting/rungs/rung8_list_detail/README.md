# Rung 8 — seeing what you posted

> Rung 7 let you *create* invoices from the browser, but the moment you posted
> one it dissolved into the general ledger — you could read the aggregate trial
> balance, yet "show me invoice #3" was impossible. Here we persist each invoice
> as a document of its own, separate from the ledger entries it emits, and add
> the two views that make a record useful: a list, and a detail page.

```sh
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Then visit http://localhost:5000/invoices

## What changed

The web layer grows a document store: a **`sales_invoice`** table, created in
`app.py`'s `init_db()` alongside the kernel's `gl_entry` table — and kept
deliberately separate from it:

```python
CREATE TABLE sales_invoice (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT    NOT NULL,
    amount   INTEGER NOT NULL,
    status   TEXT    NOT NULL DEFAULT 'Posted',
    entry_no INTEGER NOT NULL          -- points at the GL entry it emitted
)
```

Three helpers, all in `app.py` (the kernel never learns about invoices as rows):

```python
create_invoice(ledger, conn, customer, amount)  # post to GL, then store the doc
list_invoices(conn)                              # rows for the list view
get_invoice(conn, id)                            # one row, or None
```

`create_invoice` posts `kernel.SalesInvoice(...)`, captures the `entry_no` the
ledger hands back, and writes a `sales_invoice` row pointing at it. The
`new_invoice` POST handler now calls it, so a created invoice is both **posted**
into the books *and* **stored** for listing. This is the same split ERPNext
makes: the **Sales Invoice doctype** is one table, the **GL Entry** rows it
generates are another — the document is a business record, the GL is the
accounting fact, and one points at the other.

## The idea

**Persist documents as a doctype table, then read them back.** Rungs 4–5 gave
documents that emit balanced entries; now those documents get a home of their
own on disk instead of vanishing into the ledger. Once a thing is a row, the two
most basic things you can do with it are **list** every one and **open** any
one — the **R (Read) in CRUD**. The detail page shows both faces of the record:
the document's own fields (customer, amount, status) *and* the GL lines it
posted, rehydrated with `SQLiteLedger.entry(entry_no)`.

## The next pain

Sooner or later someone fat-fingers an invoice — wrong customer, wrong amount —
and wants to fix or void it. But the ledger is **append-only**: you can't
`UPDATE` or `DELETE` a posted fact without lying about what happened. The honest
fix is a *new* entry that reverses the old one.

➡️ [Rung 9 — fixing mistakes without lying](../rung9_cancel_amend/)

⬅️ [Rung 7](../rung7_create/)
