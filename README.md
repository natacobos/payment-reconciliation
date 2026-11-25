# Fix the nightly payment reconciliation

Every night we compare our payments with the settlement file the payment processor sends us, and we
calculate each merchant's fee. Finance reported two problems. Your job is to fix `reconcile.py`.
The rules are at the top of that file. Python 3 only, nothing to install.

You may use your usual AI tool; we will watch how you use it. Please think out loud.

To try the code: `python3 reconcile.py`

## Tasks: 8 minutes in total (any order)

1. **Unsettled payments (about 4 minutes).** `find_unsettled` misses payments that the processor
   settled for a different amount (rule 1). Also, with a real night's file (50,000 payments and
   50,000 settlement lines) it takes far too long. Make it correct and fast.
2. **Fees off by a cent (about 4 minutes).** Some fees are one cent short. Make `merchant_fee_cents`
   follow rule 2 exactly.

If you are still on one task two minutes after its time, move on to the next one.

At 8 minutes we stop. Then run:

```
python3 check/check.py
```

Do not edit the `check` folder.
