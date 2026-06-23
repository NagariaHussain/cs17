# Rung 7 — recording from the browser

> Rung 6 gave the books a URL you could *read* — but to record a sale you still
> had to edit Python and restart the server. Here the web layer grows its first
> WRITE: an HTML form. The user states a business fact ("invoice Acme ₹500"), the
> server validates it at the HTTP boundary, builds the matching document, and the
> document emits its own balanced entry into the ledger.

```sh
pip install -r requirements.txt
flask --app app run
```

Then visit http://localhost:5000/invoices/new.

## What changed

The new route is `POST /invoices/new`. Its whole job is the
parse → validate → build document → post → redirect flow:

```python
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
        invoice = kernel.SalesInvoice(customer, amount_paise)
        get_ledger().post_document(invoice)
        return redirect(url_for("trial_balance"))   # Post/Redirect/Get
    return render_template("new_invoice.html", customer="", amount="", error=None)
```

## The idea

**HTML forms + validation at the edge + Post/Redirect/Get.** The browser speaks
in form fields — raw, untrusted strings. The handler is the boundary where those
strings become trusted facts: `customer` must be non-empty, `amount` must go
through `kernel.parse_rupees()` (which raises `ValueError` on anything that
isn't a positive money amount). On failure we re-render the same form with the
entered values preserved and an error message — the user fixes one field, not
the whole form. On success we don't render a page; we issue a **302 redirect**
to the trial balance. That's Post/Redirect/Get: the URL the browser ends on is a
plain GET, so a refresh re-*reads* the books instead of re-*posting* the invoice.

This rung cashes in **Rung 4 (documents)**. The handler never touches debits and
credits — it builds a `SalesInvoice(customer, amount)` and calls
`post_document()`. The document knows it means "Debtors up, Sales up" and emits
that balanced entry itself. One document type maps to one form; the web layer
only has to collect business facts and hand them to the kernel.

## The next pain

You can now *create* invoices from the browser — but you can't *see* them. The
trial balance shows only the aggregate (Debtors and Sales went up by ₹250), not
the individual invoices behind it. You're posting facts into a black box.

➡️ [Rung 8 — seeing what you posted](../rung8_list_detail/)

⬅️ [Rung 6](../rung6_a_url/)
