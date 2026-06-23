"""Rung 10 — who posted this?

Rung 9 let anyone with the URL create, cancel or amend an invoice — and the
books never recorded *who* did it. That's no good for a ledger: accounting
demands an audit trail, not just *what* happened but *who* made it happen.

This rung locks the door. Every route except `login`/`register` now sits behind
a `login_required` gate: even *reading* the books requires a session. Users live
in a `user` table with werkzeug-hashed passwords; logging in stores the username
in `flask.session`. And each invoice is stamped with `created_by = session['user']`,
so the list and detail pages can say "Posted by <user>".

The accounting kernel (kernel.py) is still imported untouched — users, sessions
and document storage are all web-layer concerns that live here in app.py.
"""
import os
import sqlite3
from functools import wraps

from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import kernel

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.db")

app = Flask(__name__)
app.secret_key = "rung10-who-posted-this"  # for sessions + flash messages


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
# Auth — "lock the door". Every app route except login/register requires a
# logged-in session. The decorator redirects anonymous visitors to /login.
# ---------------------------------------------------------------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def create_user(conn, username, password):
    """Store a user with a hashed password. Raises sqlite3.IntegrityError if the
    username is already taken (the UNIQUE constraint)."""
    conn.execute(
        "INSERT INTO user (username, password_hash) VALUES (?, ?)",
        (username, generate_password_hash(password)),
    )
    conn.commit()


def get_user(conn, username):
    """One user row by username, or None."""
    return conn.execute(
        "SELECT id, username, password_hash FROM user WHERE username = ?",
        (username,),
    ).fetchone()


# ---------------------------------------------------------------------------
# The document store — app-level, NOT in the kernel. The kernel only knows GL
# entries; the "Sales Invoice" doctype is a web-layer concern (ERPNext-style).
# Rung 10 adds one column: created_by — the author stamp for the audit trail.
# ---------------------------------------------------------------------------
def init_db():
    """Create the user + document tables and seed the opening books if empty."""
    db = get_db()
    ledger = get_ledger()  # creates the kernel's gl_entry table
    db.execute(
        """CREATE TABLE IF NOT EXISTS user (
               id            INTEGER PRIMARY KEY AUTOINCREMENT,
               username      TEXT    UNIQUE NOT NULL,
               password_hash TEXT    NOT NULL
           )"""
    )
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
    db.commit()
    # A default user so you can log in to a fresh database: admin / admin.
    if get_user(db, "admin") is None:
        create_user(db, "admin", "admin")
    if db.execute("SELECT COUNT(*) FROM gl_entry").fetchone()[0]:
        return
    # Opening books. Entries 1 & 2 are plain journal entries; the Acme invoice
    # goes through create_invoice so it lands in the document store (and the
    # list), stamped to admin; the payment is a plain document with no row.
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
    at the entry it emitted. `created_by` stamps the author (the audit trail);
    `amended_from` links this row to the invoice it supersedes (None for a fresh
    invoice). Returns the new sales_invoice id."""
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


def get_amended_to(conn, id):
    """The id of a later invoice that supersedes this one, or None."""
    row = conn.execute(
        "SELECT id FROM sales_invoice WHERE amended_from = ?", (id,)
    ).fetchone()
    return row["id"] if row else None


def cancel_invoice_doc(ledger, conn, invoice, status="Cancelled"):
    """Honestly void a posted invoice: read its original GL entry, post the
    reversing entry that nets it to zero, then flip the document's STATUS.
    The GL is append-only — we never touch the original rows; the reversal is a
    new fact, and 'status' is workflow state, not an accounting fact."""
    original = ledger.entry(invoice["entry_no"])
    ledger.post(original.reversed(f"Cancel: Sales Invoice — {invoice['customer']}"))
    conn.execute(
        "UPDATE sales_invoice SET status = ? WHERE id = ?",
        (status, invoice["id"]),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Auth routes — the only ones NOT behind login_required.
# ---------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            return render_template("register.html", username=username,
                                   error="Username and password are required.")
        try:
            create_user(get_db(), username, password)
        except sqlite3.IntegrityError:
            return render_template("register.html", username=username,
                                   error=f"Username {username!r} is already taken.")
        # Registered: log them straight in.
        session["user"] = username
        return redirect(url_for("trial_balance"))
    return render_template("register.html", username="", error=None)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_user(get_db(), username)
        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", username=username,
                                   error="Wrong username or password.")
        session["user"] = user["username"]
        return redirect(url_for("trial_balance"))
    return render_template("login.html", username="", error=None)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# App routes — all gated behind login_required.
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
        # Valid: post AND store the document (stamped with the current user),
        # then redirect to its detail page.
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
    conn = get_db()
    invoice = get_invoice(conn, id)
    if invoice is None:
        abort(404)
    entry = get_ledger().entry(invoice["entry_no"])
    return render_template(
        "invoice_detail.html",
        invoice=invoice,
        entry=entry,
        amended_to=get_amended_to(conn, id),
        rupees=kernel.rupees,
    )


@app.route("/invoices/<int:id>/cancel", methods=["POST"])
@login_required
def cancel_invoice(id):
    conn = get_db()
    invoice = get_invoice(conn, id)
    if invoice is None:
        abort(404)
    # Only a live invoice can be voided; a cancelled/amended one is already history.
    if invoice["status"] != "Posted":
        flash(f"Invoice #{id} is {invoice['status']} and can't be cancelled.")
        return redirect(url_for("invoice_detail", id=id))
    cancel_invoice_doc(get_ledger(), conn, invoice)
    flash(f"Invoice #{id} cancelled — a reversing entry was posted.")
    return redirect(url_for("invoice_detail", id=id))


@app.route("/invoices/<int:id>/amend", methods=["GET", "POST"])
@login_required
def amend_invoice(id):
    conn = get_db()
    invoice = get_invoice(conn, id)
    if invoice is None:
        abort(404)
    # Only a live invoice can be amended; superseded versions stay frozen.
    if invoice["status"] != "Posted":
        flash(f"Invoice #{id} is {invoice['status']} and can't be amended.")
        return redirect(url_for("invoice_detail", id=id))

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
        # Amend = cancel the old (reversing entry + status flip) then create a
        # new version linked back to it, stamped with the current user. Net GL
        # effect: the new invoice only.
        ledger = get_ledger()
        cancel_invoice_doc(ledger, conn, invoice)
        new_id = create_invoice(ledger, conn, customer, amount_paise,
                                created_by=session["user"], amended_from=id)
        flash(f"Invoice #{id} amended — created #{new_id}.")
        return redirect(url_for("invoice_detail", id=new_id))

    # GET: prefill the form with the current values (amount shown in ₹).
    return render_template("amend_invoice.html", invoice=invoice,
                           customer=invoice["customer"],
                           amount=f"{invoice['amount'] / 100:.2f}",
                           error=None)


with app.app_context():
    init_db()
