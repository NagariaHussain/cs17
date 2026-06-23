"""Rung 11 — the reports owners actually want (the capstone).

Rung 10 gave a bookkeeper everything: a trial balance, invoices you can create,
list, open, cancel and amend, all behind a login. But an owner doesn't read a
trial balance — they ask two questions: "did we make money?" (Profit & Loss)
and "what do we own and owe?" (Balance Sheet).

This rung answers both, and the punchline of the whole quarter falls out for
free: a report is just another QUERY over the one append-only ledger. There's no
new data — we group the SAME postings differently, leaning on the kernel's
polymorphic account types (Rung 3) to sort accounts into Income / Expense /
Asset / Liability / Equity. The kernel (kernel.py) is still imported untouched.

This is the final rung, so it supersets every feature from rungs 6–10:
read the trial balance; create/list/open invoices via a `sales_invoice`
document table; cancel and amend them; users + login.
"""
import os
import sqlite3
from functools import wraps

from flask import (Flask, abort, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import kernel

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.db")

app = Flask(__name__)
app.secret_key = "rung11-reports-capstone-secret-key"


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
# Auth — a login_required gate (Rung 10). Everything but login/register is
# behind it.
# ---------------------------------------------------------------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


# ---------------------------------------------------------------------------
# The document store — app-level, NOT in the kernel. The kernel only knows GL
# entries; the "Sales Invoice" doctype and the user table are web-layer
# concerns (ERPNext-style).
# ---------------------------------------------------------------------------
def init_db():
    """Create the document and user tables; seed opening books + admin if empty."""
    db = get_db()
    ledger = get_ledger()  # creates the kernel's gl_entry table
    db.execute(
        """CREATE TABLE IF NOT EXISTS sales_invoice (
               id           INTEGER PRIMARY KEY AUTOINCREMENT,
               customer     TEXT    NOT NULL,
               amount       INTEGER NOT NULL,
               status       TEXT    NOT NULL DEFAULT 'Posted',
               entry_no     INTEGER NOT NULL,
               amended_from INTEGER,
               created_by   TEXT
           )"""
    )
    db.execute(
        """CREATE TABLE IF NOT EXISTS user (
               id            INTEGER PRIMARY KEY AUTOINCREMENT,
               username      TEXT    NOT NULL UNIQUE,
               password_hash TEXT   NOT NULL
           )"""
    )
    db.commit()
    # A default user so a fresh checkout can log straight in.
    if db.execute("SELECT COUNT(*) FROM user").fetchone()[0] == 0:
        db.execute(
            "INSERT INTO user (username, password_hash) VALUES (?, ?)",
            ("admin", generate_password_hash("admin")),
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
    create_invoice(ledger, db, "Acme Corp", 500_00, created_by="admin")
    ledger.post_document(kernel.Payment("Acme Corp", 200_00))


def create_invoice(ledger, conn, customer, amount, created_by, amended_from=None):
    """Post a SalesInvoice into the GL, then store the document row that points
    at the entry it emitted. Returns the new sales_invoice id."""
    entry_no = ledger.post_document(kernel.SalesInvoice(customer, amount))
    cur = conn.execute(
        "INSERT INTO sales_invoice "
        "(customer, amount, status, entry_no, amended_from, created_by) "
        "VALUES (?, ?, 'Posted', ?, ?, ?)",
        (customer, amount, entry_no, amended_from, created_by),
    )
    conn.commit()
    return cur.lastrowid


def list_invoices(conn):
    """Every stored invoice, oldest first — rows for the list view."""
    return conn.execute(
        "SELECT id, customer, amount, status, entry_no, amended_from, created_by "
        "FROM sales_invoice ORDER BY id"
    ).fetchall()


def get_invoice(conn, id):
    """One stored invoice by id, or None."""
    return conn.execute(
        "SELECT id, customer, amount, status, entry_no, amended_from, created_by "
        "FROM sales_invoice WHERE id = ?", (id,)
    ).fetchone()


# ---------------------------------------------------------------------------
# Reports — pure QUERIES over the one ledger. No new data; we re-group the same
# postings by the kernel's polymorphic account types (Rung 3).
# ---------------------------------------------------------------------------
def _grouped_balances():
    """Net the ledger and bucket (account, balance) rows by kernel type."""
    rows, _, _ = kernel.trial_balance(get_ledger())
    buckets = {"income": [], "expense": [], "asset": [], "liability": [], "equity": []}
    for account, balance in rows:
        if isinstance(account, kernel.Income):
            buckets["income"].append((account, balance))
        elif isinstance(account, kernel.Expense):
            buckets["expense"].append((account, balance))
        elif isinstance(account, kernel.Asset):
            buckets["asset"].append((account, balance))
        elif isinstance(account, kernel.Liability):
            buckets["liability"].append((account, balance))
        elif isinstance(account, kernel.Equity):
            buckets["equity"].append((account, balance))
    return buckets


# ---------------------------------------------------------------------------
# Routes.
# ---------------------------------------------------------------------------
@app.route("/")
@login_required
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
@login_required
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
        new_id = create_invoice(get_ledger(), get_db(), customer, amount_paise,
                                created_by=session["user"])
        # Post/Redirect/Get: a refresh can't double-post.
        return redirect(url_for("invoice_detail", id=new_id))
    return render_template("new_invoice.html", customer="", amount="", error=None)


@app.route("/invoices")
@login_required
def invoices():
    return render_template(
        "invoices.html",
        invoices=list_invoices(get_db()),
        rupees=kernel.rupees,
    )


@app.route("/invoices/<int:id>")
@login_required
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


@app.route("/invoices/<int:id>/cancel", methods=["POST"])
@login_required
def cancel_invoice(id):
    db = get_db()
    invoice = get_invoice(db, id)
    if invoice is None:
        abort(404)
    if invoice["status"] == "Posted":
        ledger = get_ledger()
        original = ledger.entry(invoice["entry_no"])
        # Append a reversing entry — the GL is never edited, only added to.
        ledger.post(original.reversed(
            f"Cancel: Sales Invoice #{id} — {invoice['customer']}"))
        db.execute("UPDATE sales_invoice SET status = 'Cancelled' WHERE id = ?", (id,))
        db.commit()
    return redirect(url_for("invoice_detail", id=id))


@app.route("/invoices/<int:id>/amend", methods=["GET", "POST"])
@login_required
def amend_invoice(id):
    db = get_db()
    invoice = get_invoice(db, id)
    if invoice is None:
        abort(404)
    if request.method == "POST":
        customer = request.form.get("customer", "").strip()
        amount_text = request.form.get("amount", "")
        if not customer:
            return render_template("amend_invoice.html", invoice=invoice,
                                   customer=customer, amount=amount_text,
                                   error="Customer is required.")
        try:
            amount_paise = kernel.parse_rupees(amount_text)
        except ValueError as e:
            return render_template("amend_invoice.html", invoice=invoice,
                                   customer=customer, amount=amount_text,
                                   error=str(e))
        ledger = get_ledger()
        # Amend = cancel the old (reverse its entry, flag the doc) then create a
        # fresh invoice that remembers where it came from.
        if invoice["status"] == "Posted":
            original = ledger.entry(invoice["entry_no"])
            ledger.post(original.reversed(
                f"Cancel: Sales Invoice #{id} — {invoice['customer']}"))
            db.execute("UPDATE sales_invoice SET status = 'Cancelled' WHERE id = ?", (id,))
            db.commit()
        new_id = create_invoice(ledger, db, customer, amount_paise,
                                created_by=session["user"], amended_from=id)
        return redirect(url_for("invoice_detail", id=new_id))
    # GET: a form prefilled with the current values (amount as plain rupees).
    return render_template(
        "amend_invoice.html",
        invoice=invoice,
        customer=invoice["customer"],
        amount=f"{invoice['amount'] // 100}.{invoice['amount'] % 100:02d}",
        error=None,
    )


@app.route("/reports/pnl")
@login_required
def pnl():
    buckets = _grouped_balances()
    total_income = sum(b for _, b in buckets["income"])
    total_expense = sum(b for _, b in buckets["expense"])
    return render_template(
        "pnl.html",
        income=buckets["income"],
        expense=buckets["expense"],
        total_income=total_income,
        total_expense=total_expense,
        net_profit=total_income - total_expense,
        rupees=kernel.rupees,
    )


@app.route("/reports/balance-sheet")
@login_required
def balance_sheet():
    buckets = _grouped_balances()
    total_income = sum(b for _, b in buckets["income"])
    total_expense = sum(b for _, b in buckets["expense"])
    net_profit = total_income - total_expense
    assets = buckets["asset"]
    total_assets = sum(b for _, b in assets)
    liabilities = buckets["liability"]
    equity = buckets["equity"]
    # Equity + Liabilities side carries the period's Net Profit from the P&L —
    # that's exactly what makes the two sides tie out (profit flows into equity).
    total_eq_liab = sum(b for _, b in liabilities) + sum(b for _, b in equity) + net_profit
    return render_template(
        "balance_sheet.html",
        assets=assets,
        total_assets=total_assets,
        liabilities=liabilities,
        equity=equity,
        net_profit=net_profit,
        total_eq_liab=total_eq_liab,
        rupees=kernel.rupees,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        row = get_db().execute(
            "SELECT username, password_hash FROM user WHERE username = ?",
            (username,)
        ).fetchone()
        if row is None or not check_password_hash(row["password_hash"], password):
            return render_template("login.html", username=username,
                                   error="Wrong username or password.")
        session["user"] = row["username"]
        return redirect(url_for("trial_balance"))
    return render_template("login.html", username="", error=None)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            return render_template("register.html", username=username,
                                   error="Username and password are required.")
        db = get_db()
        if db.execute("SELECT 1 FROM user WHERE username = ?", (username,)).fetchone():
            return render_template("register.html", username=username,
                                   error="That username is taken.")
        db.execute(
            "INSERT INTO user (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
        session["user"] = username
        return redirect(url_for("trial_balance"))
    return render_template("register.html", username="", error=None)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


with app.app_context():
    init_db()
