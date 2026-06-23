"""Rung 8 — seeing what you posted.

Rung 7 let you create invoices from the browser, but once posted they dissolved
into the general ledger — you could read the aggregate trial balance, but
"show me invoice #3" was impossible.

Here the web layer grows a document store of its own: a `sales_invoice` table,
kept DISTINCT from the kernel's append-only `gl_entry` table — exactly how
ERPNext keeps the "Sales Invoice" doctype separate from the "GL Entry" rows it
emits. With documents persisted as first-class rows we can list them and open
any one of them — the R in CRUD. The kernel (kernel.py) is still imported
untouched.
"""
import os
import sqlite3

from flask import Flask, abort, g, redirect, render_template, request, url_for

import kernel

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.db")

app = Flask(__name__)


def get_db():
    """One SQLite connection per request, stashed on flask.g."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def get_ledger():
    """The kernel's SQLiteLedger, wrapped around this request's connection."""
    return kernel.SQLiteLedger(get_db())


# ---------------------------------------------------------------------------
# The document store — app-level, NOT in the kernel. The kernel only knows GL
# entries; the "Sales Invoice" doctype is a web-layer concern (ERPNext-style).
# ---------------------------------------------------------------------------
def init_db():
    """Create the document table and seed the opening books if empty."""
    db = get_db()
    ledger = get_ledger()  # creates the kernel's gl_entry table
    db.execute(
        """CREATE TABLE IF NOT EXISTS sales_invoice (
               id       INTEGER PRIMARY KEY AUTOINCREMENT,
               customer TEXT    NOT NULL,
               amount   INTEGER NOT NULL,
               status   TEXT    NOT NULL DEFAULT 'Posted',
               entry_no INTEGER NOT NULL
           )"""
    )
    db.commit()
    if db.execute("SELECT COUNT(*) FROM gl_entry").fetchone()[0]:
        return
    # Opening books. Entries 1 & 2 are plain journal entries; the Acme invoice
    # goes through create_invoice so it lands in the document store (and the
    # list); the payment is a plain document with no invoice row of its own.
    ledger.post(kernel.JournalEntry("Owner invests cash")
                .add(kernel.cash, debit=1000_00)
                .add(kernel.capital, credit=1000_00))
    ledger.post(kernel.JournalEntry("Buy supplies for cash")
                .add(kernel.supplies, debit=300_00)
                .add(kernel.cash, credit=300_00))
    create_invoice(ledger, db, "Acme Corp", 500_00)
    ledger.post_document(kernel.Payment("Acme Corp", 200_00))


def create_invoice(ledger, conn, customer, amount):
    """Post a SalesInvoice into the GL, then store the document row that points
    at the entry it emitted. Returns the new sales_invoice id."""
    entry_no = ledger.post_document(kernel.SalesInvoice(customer, amount))
    cur = conn.execute(
        "INSERT INTO sales_invoice (customer, amount, status, entry_no) "
        "VALUES (?, ?, 'Posted', ?)",
        (customer, amount, entry_no),
    )
    conn.commit()
    return cur.lastrowid


def list_invoices(conn):
    """Every stored invoice, newest last — rows for the list view."""
    return conn.execute(
        "SELECT id, customer, amount, status, entry_no FROM sales_invoice "
        "ORDER BY id"
    ).fetchall()


def get_invoice(conn, id):
    """One stored invoice by id, or None."""
    return conn.execute(
        "SELECT id, customer, amount, status, entry_no FROM sales_invoice "
        "WHERE id = ?", (id,)
    ).fetchone()


# ---------------------------------------------------------------------------
# Routes.
# ---------------------------------------------------------------------------
@app.route("/")
def trial_balance():
    rows, total_dr, total_cr = kernel.trial_balance(get_ledger())
    return render_template(
        "trial_balance.html",
        rows=rows,
        total_dr=total_dr,
        total_cr=total_cr,
        rupees=kernel.rupees,
    )


@app.route("/invoices/new", methods=["GET", "POST"])
def new_invoice():
    if request.method == "POST":
        customer = request.form.get("customer", "").strip()
        amount_text = request.form.get("amount", "")
        if not customer:
            return render_template("new_invoice.html",
                                   customer=customer, amount=amount_text,
                                   error="Customer is required.")
        try:
            amount_paise = kernel.parse_rupees(amount_text)
        except ValueError as e:
            return render_template("new_invoice.html",
                                   customer=customer, amount=amount_text,
                                   error=str(e))
        # Valid: post AND store the document, then redirect to its detail page.
        new_id = create_invoice(get_ledger(), get_db(), customer, amount_paise)
        # Post/Redirect/Get: a refresh can't double-post.
        return redirect(url_for("invoice_detail", id=new_id))
    return render_template("new_invoice.html", customer="", amount="", error=None)


@app.route("/invoices")
def invoices():
    return render_template(
        "invoices.html",
        invoices=list_invoices(get_db()),
        rupees=kernel.rupees,
    )


@app.route("/invoices/<int:id>")
def invoice_detail(id):
    invoice = get_invoice(get_db(), id)
    if invoice is None:
        abort(404)
    entry = get_ledger().entry(invoice["entry_no"])
    return render_template(
        "invoice_detail.html",
        invoice=invoice,
        entry=entry,
        rupees=kernel.rupees,
    )


with app.app_context():
    init_db()
