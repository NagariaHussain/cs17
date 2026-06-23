# Rung 6 — a URL for the books

> The kernel can post and total a ledger, but the only way to *see* it was to run
> a script and squint at a terminal. Here we give the books a URL: a tiny Flask
> layer sits on top of the kernel and renders the trial balance as a web page —
> and the kernel never knows it's inside a web server.

```sh
pip install -r requirements.txt
flask --app app run
```

then visit http://localhost:5000/

## What changed

Nothing in the kernel. `kernel.py` is imported **untouched** — the same file from
Rung 5 — and the web layer is written entirely against its public surface:

```python
import kernel

def get_ledger():                       # the kernel's SQLiteLedger,
    return kernel.SQLiteLedger(get_db())  # wrapped around this request's connection

@app.route("/")
def trial_balance():
    rows, total_dr, total_cr = kernel.trial_balance(get_ledger())
    return render_template("trial_balance.html",
                           rows=rows, total_dr=total_dr, total_cr=total_cr,
                           rupees=kernel.rupees)
```

The connection lives **per request** on `flask.g` and is closed in
`teardown_appcontext`; `init_db()` seeds the four opening transactions on startup
only if `gl_entry` is empty. The route does one thing: hand a `Ledger` to
`kernel.trial_balance()` and pour the result into a template.

## The idea

**The web layer sits on top of the kernel** — request → handler → response is
just another caller of the domain, no different from a script. This **cashes in
Rung 5's storage boundary**: because the app talks to a `Ledger` interface and
not a Python list, it could swap in `SQLiteLedger` without the kernel noticing —
and now Flask can drive that same interface without the kernel noticing either.
The domain has no idea it's inside a web server.

The pain removed: reading the books no longer means running a script and staring
at a terminal. A bookkeeper opens a URL.

## The next pain

You can **read** the books in a browser, but you still can't **record** anything
without editing Python and re-seeding. A report is not a system of record until
you can post to it from the same place you read it.

➡️ [Rung 7 — recording from the browser](../rung7_create/)

⬅️ [Rung 5](../rung5_storage/)
