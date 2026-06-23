"""
Accounting kernel — the domain model built across Rungs 0–5, vendored here so
the web app can import it untouched. The whole point of the storage boundary
(Rung 5) is that this module has NO idea it's running inside a web server.

This file is IDENTICAL in every Part-2 rung and must not be modified. All
web-specific concerns (document storage, users, reports) live in app.py.

Money is integer paise everywhere; ₹1000.00 is written 1000_00.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Accounts — polymorphic balance() by type (Rung 3).
# ---------------------------------------------------------------------------
class Account:
    def __init__(self, name):
        self.name = name

    def balance(self, debits, credits):
        raise NotImplementedError("each Account subclass defines its own balance")

    def __repr__(self):
        return self.name


class DebitNormalAccount(Account):    # assets, expenses — a debit grows them
    normal_side = "Dr"

    def balance(self, debits, credits):
        return debits - credits


class CreditNormalAccount(Account):   # liabilities, equity, income — a credit grows them
    normal_side = "Cr"

    def balance(self, debits, credits):
        return credits - debits


class Asset(DebitNormalAccount):      pass
class Expense(DebitNormalAccount):    pass
class Liability(CreditNormalAccount): pass
class Equity(CreditNormalAccount):    pass
class Income(CreditNormalAccount):    pass


# ---------------------------------------------------------------------------
# Postings and entries (Rung 2).
# ---------------------------------------------------------------------------
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

    def reversed(self, narration=None):
        """A new entry with every debit and credit swapped — used to CANCEL a
        posted entry without ever editing or deleting it (Rung 9)."""
        rev = JournalEntry(narration or f"Reversal of: {self.narration}")
        for p in self.postings:
            rev.add(p.account, debit=p.credit, credit=p.debit)
        return rev


# ---------------------------------------------------------------------------
# The Ledger interface and its backends (Rung 5).
# ---------------------------------------------------------------------------
class Ledger(ABC):
    @abstractmethod
    def post(self, entry):
        """Append a balanced entry; return its entry number."""

    @abstractmethod
    def postings(self):
        """Yield every Posting ever recorded — the flat ledger, for reporting."""

    def post_document(self, document):
        """Post anything that can express itself as a balanced entry."""
        return self.post(document.to_journal_entry())

    @staticmethod
    def _reject_if_unbalanced(entry):
        if not entry.is_balanced():
            raise ValueError(f"Refusing to post unbalanced entry: {entry.narration!r}")


class InMemoryLedger(Ledger):
    def __init__(self):
        self.entries = []

    def post(self, entry):
        self._reject_if_unbalanced(entry)
        self.entries.append(entry)
        return len(self.entries)

    def postings(self):
        for entry in self.entries:
            yield from entry.postings


class SQLiteLedger(Ledger):
    """Append-only GL table on disk. Posting is an INSERT; nothing is ever
    UPDATEd or DELETEd — corrections are new entries (see JournalEntry.reversed)."""

    def __init__(self, connection):
        self.conn = connection
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS gl_entry (
                   id        INTEGER PRIMARY KEY AUTOINCREMENT,
                   entry_no  INTEGER NOT NULL,
                   narration TEXT    NOT NULL,
                   account   TEXT    NOT NULL,
                   debit     INTEGER NOT NULL,
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
        return next_no

    def postings(self):
        for account_name, debit, credit in self.conn.execute(
                "SELECT account, debit, credit FROM gl_entry ORDER BY id"):
            yield Posting(CHART[account_name], debit, credit)

    def entry(self, entry_no):
        """Reconstruct one posted JournalEntry from the GL, by its number."""
        rows = self.conn.execute(
            "SELECT narration, account, debit, credit FROM gl_entry "
            "WHERE entry_no = ? ORDER BY id", (entry_no,)
        ).fetchall()
        if not rows:
            return None
        entry = JournalEntry(rows[0][0])
        for _, account_name, debit, credit in rows:
            entry.add(CHART[account_name], debit=debit, credit=credit)
        return entry


# ---------------------------------------------------------------------------
# Documents — they emit balanced entries (Rung 4).
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


# ---------------------------------------------------------------------------
# Chart of accounts (configuration, kept in code) and display helpers.
# ---------------------------------------------------------------------------
cash     = Asset("Cash")
supplies = Asset("Supplies")
debtors  = Asset("Debtors")
capital  = Equity("Capital")
sales    = Income("Sales")
rent     = Expense("Rent")
CHART = {a.name: a for a in (cash, supplies, debtors, capital, sales, rent)}


def rupees(paise):
    """Format integer paise as ₹ rupees, e.g. 70000 -> ' ₹700.00'."""
    sign = "-" if paise < 0 else " "
    paise = abs(paise)
    return f"{sign}₹{paise // 100}.{paise % 100:02d}"


def parse_rupees(text):
    """Parse a user-entered rupee amount ('500', '500.50', '₹500') to paise.
    Raises ValueError on anything that isn't a positive money amount."""
    cleaned = str(text).replace("₹", "").replace(",", "").strip()
    if not cleaned:
        raise ValueError("Amount is required.")
    amount = round(float(cleaned) * 100)
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return amount


def trial_balance(ledger):
    """Net every account and return (rows, total_dr, total_cr) where rows is a
    list of (Account, balance_paise). Each account reports its natural balance."""
    totals = {}
    for p in ledger.postings():
        debits, credits = totals.get(p.account, (0, 0))
        totals[p.account] = (debits + p.debit, credits + p.credit)
    rows, total_dr, total_cr = [], 0, 0
    for account, (debits, credits) in totals.items():
        bal = account.balance(debits, credits)
        rows.append((account, bal))
        if account.normal_side == "Dr":
            total_dr += bal
        else:
            total_cr += bal
    return rows, total_dr, total_cr
