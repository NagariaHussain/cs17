# Rung 5 — storage

> The ledger has been a Python list this whole time — close the program and the
> books vanish. Here we give it a disk to live on *without* welding the database
> to the app. We name what the app needs — a `Ledger` you can post to and read
> from — make that an interface, and let storage be a swappable detail behind it.

```sh
python ledger.py
```

## What changed

`Ledger` becomes an **abstract interface** — a promise, not an implementation:

```python
class Ledger(ABC):
    @abstractmethod
    def post(self, entry): ...
    @abstractmethod
    def postings(self): ...

    def post_document(self, document):          # shared by every backend
        self.post(document.to_journal_entry())
```

Two backends keep that promise in different ways:

```python
class InMemoryLedger(Ledger):   # the list from Rungs 2–4
    def post(self, entry):     self.entries.append(entry)
    def postings(self):        yield from ...

class SQLiteLedger(Ledger):     # an append-only table on disk
    def post(self, entry):     self.conn.execute("INSERT INTO gl_entry ...")
    def postings(self):        yield Posting(CHART[name], debit, credit)  # from rows
```

And the app is written against the interface alone — it never names a backend:

```python
def record_transactions(ledger):  ...   # takes a Ledger
def trial_balance(ledger, title):  ...  # takes a Ledger
```

## The idea

**Dependency inversion.** Before, the app *was* the list — `gl = []` sat right
there in the transaction code. The high-level thing (accounting) depended on a
low-level detail (a Python list). Now both depend on the same abstraction:

```
   before:   app ──────────────▶ list          (glued to one storage)
   after:    app ──▶ Ledger ◀── list / SQLite / ORM   (storage is pluggable)
```

`record_transactions()` and `trial_balance()` can't tell which ledger they were
handed — so we run the **same** code against an in-memory list and a SQLite file
and get the **same** trial balance. The proof is in the run: three identical
trial balances, and the third is read back from disk *after the connection was
closed and reopened* — a stand-in for restarting the app. The list forgets; the
file remembers; the code above the interface never knew the difference.

## Two details worth noticing

- **The table is append-only.** Posting is an `INSERT`; nothing is ever
  `UPDATE`d or `DELETE`d. Corrections are new entries — the same discipline as a
  write-ahead log or git history, and exactly how a real ledger has worked for
  530 years. Mistakes are fixed with reversing entries, never by erasing facts.
- **The chart of accounts stays in code; the transactions go in the DB.** SQLite
  stores each posting's account *name*; its type — and therefore its polymorphic
  `balance()` rule — is rehydrated from `CHART` when the rows are read back.
  Configuration lives in code, transactional data lives in the database.

## End of the ladder

```
0  raw rows            a list of tuples, nothing guards it
1  a function          post() guards debits == credits
2  objects             the rule lives inside the entry
3  accounts            account.balance() is polymorphic by type
4  documents           documents emit their own balanced entries
5  storage             the ledger is an interface; storage is swappable   ← you are here
```

Each rung removed a specific pain the previous rung made you feel. What's left is
a small but real accounting kernel: typed accounts, balanced-by-construction
documents posting into one append-only ledger on disk, and reports that are just
queries over it — the shape ERPNext, QuickBooks, and SAP all take, in miniature.

The natural next step (a course project, not a rung): wrap this kernel in Flask,
swap `SQLiteLedger` for an ORM-backed one behind the *same* interface, and you
have the web accounting app q3 set out to build.

⬅️ [Rung 4](../rung4_documents/)
