"""`python3 check/check.py`: one line per task, for the interviewer. Do not edit anything in check/.
Standard library only."""

import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
TIME_LIMIT = 5  # seconds for 50,000 x 50,000

errors = []
try:
    import reconcile
except Exception as e:  # noqa: BLE001
    reconcile = None
    errors.append(f"import: {e}")


def safe(fn, *args):
    try:
        return fn(*args)
    except Exception as e:  # noqa: BLE001
        errors.append(f"{fn.__name__}: {e}")
        return None


P = lambda i, a: {"payment_id": i, "amount_cents": a}
payments = [P("a", 1000), P("b", 2500), P("c", 700), P("d", 1200), P("e", 300), P("b", 2500)]
settlements = [P("d", 1200), P("b", 2400), P("a", 1000), P("x", 999), P("b", 2500), P("e", 30)]
# a settled; b settled (one line has another amount, but another line matches); c missing; d settled; e wrong amount
t1a = t1b = False
if reconcile:
    t1a = safe(reconcile.find_unsettled, payments, settlements) == ["c", "e"]

    big = f"""
import sys, random
sys.path.insert(0, {ROOT!r})
import reconcile
random.seed(7)
n = 50000
pay = [{{"payment_id": "p%06d" % i, "amount_cents": 100 + i % 9000}} for i in range(n)]
sett = [dict(p) for p in pay if p["payment_id"][-1] != "7"]
random.shuffle(sett)
want = [p["payment_id"] for p in pay if p["payment_id"][-1] == "7"]
print("OK" if reconcile.find_unsettled(pay, sett) == want else "WRONG")
"""
    try:
        out = subprocess.run([sys.executable, "-c", big], capture_output=True, text=True, timeout=TIME_LIMIT)
        t1b = out.stdout.strip() == "OK"
        if out.returncode != 0:
            errors.append("find_unsettled (50,000): " + (out.stderr.strip().splitlines() or ["error"])[-1])
    except subprocess.TimeoutExpired:
        t1b = False

ties = [(250, "1", 3), (50, "1", 1), (1025, "2", 21), (4500, "0.5", 23)]
decimals = [(3000, "1.15", 35), (5500, "0.7", 39), (1005, "2.9", 29), (12345, "3.49", 431)]
t2a = t2b = False
if reconcile:
    t2a = all(safe(reconcile.merchant_fee_cents, a, r) == w for a, r, w in ties)
    t2b = all(safe(reconcile.merchant_fee_cents, a, r) == w for a, r, w in decimals)

h = hashlib.sha256()
for f in sorted(os.listdir(os.path.join(ROOT, "check"))):
    p = os.path.join(ROOT, "check", f)
    if os.path.isfile(p) and f.endswith(".py"):
        h.update(f.encode())
        with open(p, "rb") as fh:
            h.update(fh.read())


def line(label, text):
    print(label.ljust(24, ".") + " " + text)


mark = lambda b: "✓" if b else "✗"
print("\nPayment reconciliation — check\n")
line("T1 Unsettled payments", f"{t1a + t1b}/2  same id and amount {mark(t1a)}  50,000 lines in under {TIME_LIMIT}s {mark(t1b)}")
line("T2 Fees", f"{t2a + t2b}/2  half a cent goes up {mark(t2a)}  exact with decimal rates {mark(t2b)}")
for e in dict.fromkeys(errors):
    line("Python error", e)
line("Check files", h.hexdigest()[:8])
print("")
