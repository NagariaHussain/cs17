"""Rung 7 — recording from the browser.

Rung 6 gave the books a URL you could *read*. But to record a sale you still had
to edit Python and restart the server. Here the web layer grows its first WRITE:
an HTML form. The user states a business fact — "invoice Acme ₹500" — the handler
validates it at the HTTP boundary, builds the matching kernel Document, and posts
it. The kernel (kernel.py) is still imported untouched.
"""
import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for

import kernel

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.db")

app = Flask(__name__)


def get_db():
    """One SQLite connection per request, stashed on flask.g."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def get_ledger():
    """The kernel's SQLiteLedger, wrapped around this request's connection."""
    return kernel.SQLiteLedger(get_db())


def init_db():
    """Seed the four opening transactions if the GL is empty."""
    ledger = get_ledger()
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM gl_entry").fetchone()[0]
    if count:
        return
    ledger.post(kernel.JournalEntry("Owner invests cash")
                .add(kernel.cash, debit=1000_00)
                .add(kernel.capital, credit=1000_00))
    ledger.post(kernel.JournalEntry("Buy supplies for cash")
                .add(kernel.supplies, debit=300_00)
                .add(kernel.cash, credit=300_00))
    ledger.post_document(kernel.SalesInvoice("Acme Corp", 500_00))
    ledger.post_document(kernel.Payment("Acme Corp", 200_00))


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
        # Validate the stated business fact at the HTTP boundary.
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
        # Valid: build the document, let it emit its balanced entry, post it.
        invoice = kernel.SalesInvoice(customer, amount_paise)
        get_ledger().post_document(invoice)
        # Post/Redirect/Get: redirect so a refresh can't double-post.
        return redirect(url_for("trial_balance"))
    return render_template("new_invoice.html", customer="", amount="", error=None)


with app.app_context():
    init_db()
