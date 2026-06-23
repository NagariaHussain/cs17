"""
Rung 5 — storage. Until now the ledger has been a Python list living in RAM.
Close the program and 530 years of bookkeeping evaporate. Real books outlive the
process that wrote them, so the ledger has to live on disk.

The naive fix is to reach into the ledger and replace the list with SQLite calls
— but then every report, every document, the whole app, is welded to SQLite. The
pain isn't "we need a database", it's "the database would be glued to everything".

The fix is to invert the dependency. We name the thing the app actually needs —
a `Ledger`: something you can `post` to and read `postings` from — and make that
an abstract interface. The app depends on *that promise*, never on how it's kept.
Then storage becomes a swappable detail:

    InMemoryLedger   — the list from Rungs 2–4 (fast, forgets everything)
    SQLiteLedger     — same interface, but the rows live in a file on disk

`record_transactions()` and `trial_balance()` below take a `Ledger` and don't
know — can't know — which one they got. We run the SAME code against both and the
trial balance is identical. Then we close the SQLite connection, reopen the file,
and the books are still there. THAT is what storage bought us.

This is **dependency inversion**: high-level policy (accounting) depends on an
abstraction (`Ledger`); the low-level detail (a list? SQLite? an ORM?) depends on
that same abstraction too. The arrow that used to point app → list now points
both app → Ledger ← storage.
"""

import os
import sqlite3
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Accounts and entries — unchanged from Rungs 3–4.
# ---------------------------------------------------------------------------
class Account:
    def __init__(self, name):
        self.name = name

    def balance(self, debits, credits):
        raise NotImplementedError("each Account subclass defines its own balance")

    def __repr__(self):
        return self.name


class DebitNormalAccount(Account):    # assets, expenses
    normal_side = "Dr"

    def balance(self, debits, credits):
        return debits - credits


class CreditNormalAccount(Account):   # liabilities, equity, income
    normal_side = "Cr"

    def balance(self, debits, credits):
        return credits - debits


class Asset(DebitNormalAccount):      pass
class Expense(DebitNormalAccount):    pass
class Liability(CreditNormalAccount): pass
class Equity(CreditNormalAccount):    pass
class Income(CreditNormalAccount):    pass


@dataclass
class Posting:
    account: Account
    debit: int = 0    # paise
    credit: int = 0   # paise


@dataclass
class JournalEntry:
    narration: str
    postings: list = field(default_factory=list)

    def add(self, account, debit=0, credit=0):
        self.postings.append(Posting(account, debit, credit))
        return self

    def is_balanced(self):
        debits = sum(p.debit for p in self.postings)
        credits = sum(p.credit for p in self.postings)
        return debits == credits


# ---------------------------------------------------------------------------
# The Ledger INTERFACE — the heart of this rung. It names the two things the
# app needs of any ledger, and nothing about where the data lives. post_document
# is shared logic; post() and postings() are the seam each backend fills in.
# ---------------------------------------------------------------------------
class Ledger(ABC):
    @abstractmethod
    def post(self, entry):
        """Append a balanced entry to the book of record."""

    @abstractmethod
    def postings(self):
        """Yield every posting ever recorded — the flat ledger, for reporting."""

    def post_document(self, document):
        """Post anything that can express itself as a balanced entry. Identical
        for every backend, so it lives here, on the interface, written once."""
        self.post(document.to_journal_entry())

    @staticmethod
    def _reject_if_unbalanced(entry):
        if not entry.is_balanced():
            raise ValueError(f"Refusing to post unbalanced entry: {entry.narration!r}")


class InMemoryLedger(Ledger):
    """The list from Rungs 2–4 — now revealed as just one Ledger among others.
    Fast and simple; forgets everything the instant the program ends."""

    def __init__(self):
        self.entries = []

    def post(self, entry):
        self._reject_if_unbalanced(entry)
        self.entries.append(entry)

    def postings(self):
        for entry in self.entries:
            yield from entry.postings


class SQLiteLedger(Ledger):
    """The same interface, backed by an append-only table on disk. Posting is an
    INSERT; nothing is ever UPDATEd or DELETEd — corrections are new entries, the
    way a real ledger (and a write-ahead log, and git) works."""

    def __init__(self, connection):
        self.conn = connection
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS gl_entry (
                   id        INTEGER PRIMARY KEY AUTOINCREMENT,
                   entry_no  INTEGER NOT NULL,   -- groups postings into one entry
                   narration TEXT    NOT NULL,
                   account   TEXT    NOT NULL,
                   debit     INTEGER NOT NULL,   -- paise
                   credit    INTEGER NOT NULL
               )"""
        )

    def post(self, entry):
        self._reject_if_unbalanced(entry)
        next_no = self.conn.execute(
            "SELECT COALESCE(MAX(entry_no), 0) + 1 FROM gl_entry"
        ).fetchone()[0]
        self.conn.executemany(
            "INSERT INTO gl_entry (entry_no, narration, account, debit, credit) "
            "VALUES (?, ?, ?, ?, ?)",
            [(next_no, entry.narration, p.account.name, p.debit, p.credit)
             for p in entry.postings],
        )
        self.conn.commit()

    def postings(self):
        rows = self.conn.execute(
            "SELECT account, debit, credit FROM gl_entry ORDER BY id"
        )
        for account_name, debit, credit in rows:
            # The DB stores the account's NAME; its type (and thus its balance
            # rule) is rehydrated from the chart of accounts kept in code.
            yield Posting(CHART[account_name], debit, credit)


# ---------------------------------------------------------------------------
# Documents — unchanged from Rung 4. They emit entries; they neither know nor
# care which Ledger will store them.
# ---------------------------------------------------------------------------
class Document:
    def to_journal_entry(self):
        raise NotImplementedError("every Document must emit a balanced JournalEntry")


@dataclass
class SalesInvoice(Document):
    customer: str
    amount: int   # paise

    def to_journal_entry(self):
        return (JournalEntry(f"Sales Invoice — {self.customer}")
                .add(debtors, debit=self.amount)
                .add(sales, credit=self.amount))


@dataclass
class Payment(Document):
    customer: str
    amount: int   # paise

    def to_journal_entry(self):
        return (JournalEntry(f"Payment received — {self.customer}")
                .add(cash, debit=self.amount)
                .add(debtors, credit=self.amount))


# The chart of accounts: configuration, kept in code. The ledger stores the
# *transactions*; the accounts they refer to are looked up here by name.
cash     = Asset("Cash")
supplies = Asset("Supplies")
debtors  = Asset("Debtors")
capital  = Equity("Capital")
sales    = Income("Sales")
CHART = {a.name: a for a in (cash, supplies, debtors, capital, sales)}


# ---------------------------------------------------------------------------
# The APP — written entirely against the Ledger interface. Pass it any backend.
# ---------------------------------------------------------------------------
def record_transactions(ledger):
    """The same four transactions as Rung 4. Note the type of `ledger` is never
    inspected — this code works for InMemoryLedger, SQLiteLedger, or anything
    else that honours the interface."""
    ledger.post(
        JournalEntry("Owner invests cash")
            .add(cash, debit=1000_00)
            .add(capital, credit=1000_00)
    )
    ledger.post(
        JournalEntry("Buy supplies for cash")
            .add(supplies, debit=300_00)
            .add(cash, credit=300_00)
    )
    ledger.post_document(SalesInvoice("Acme Corp", 500_00))
    ledger.post_document(Payment("Acme Corp", 200_00))


def rupees(paise):
    sign = "-" if paise < 0 else " "
    paise = abs(paise)
    return f"{sign}₹{paise // 100}.{paise % 100:02d}"


def trial_balance(ledger, title):
    """Reporting, also written against the interface alone. It reads postings;
    it has no idea whether they came from a list or a database file."""
    totals = {}
    for p in ledger.postings():
        debits, credits = totals.get(p.account, (0, 0))
        totals[p.account] = (debits + p.debit, credits + p.credit)

    print(f"TRIAL BALANCE — {title}")
    print(f"{'':<10}{'Dr':>12}{'Cr':>12}")
    print("-" * 34)
    total_dr = total_cr = 0
    for account, (debits, credits) in totals.items():
        bal = account.balance(debits, credits)
        if account.normal_side == "Dr":
            total_dr += bal
            print(f"{account.name:<10}{rupees(bal):>12}{'':>12}")
        else:
            total_cr += bal
            print(f"{account.name:<10}{'':>12}{rupees(bal):>12}")
    print("-" * 34)
    print(f"{'TOTAL':<10}{rupees(total_dr):>12}{rupees(total_cr):>12}")
    print("  Debits equal credits. ✓\n" if total_dr == total_cr
          else "  THE BOOKS DO NOT BALANCE. ✗\n")


# 1. The in-memory ledger from Rungs 2–4 — now just one Ledger among others.
mem = InMemoryLedger()
record_transactions(mem)
trial_balance(mem, "InMemoryLedger (a list in RAM)")

# 2. The SAME app code, a different ledger underneath. Not one line of
#    record_transactions or trial_balance changed to make this work.
dbdir = tempfile.mkdtemp()
dbpath = os.path.join(dbdir, "books.db")
db = SQLiteLedger(sqlite3.connect(dbpath))
record_transactions(db)
trial_balance(db, "SQLiteLedger (rows on disk)")

# 3. The payoff. Drop the connection — as if the program exited — then reopen
#    the file. We post NOTHING; the books are read straight back from disk.
db.conn.close()
reopened = SQLiteLedger(sqlite3.connect(dbpath))
trial_balance(reopened, "SQLiteLedger reopened — survived a 'restart'")
reopened.conn.close()

# Tidy up the temp database this demo created.
os.remove(dbpath)
os.rmdir(dbdir)

print("Three ledgers, one app. The list forgets; the file remembers; the code")
print("above the Ledger interface never knew the difference. That is dependency")
print("inversion — and the end of the ladder.")
