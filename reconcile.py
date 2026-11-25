"""Nightly reconciliation between our payments and the payment processor's settlement file.

Rules (from the finance team):
1. A payment is settled when the processor's file has a line with the same payment id AND the same amount.
   A line with the same id but a different amount is a mismatch: the payment is still unsettled.
2. The merchant fee is amount x rate / 100, in whole cents, rounded half up (0.5 cent goes up).
   Rates come from the merchant contract as text, for example "2.9".
"""


def find_unsettled(payments, settlements):
    """Ids of the payments with no matching settlement, in the order of `payments`.

    payments and settlements are lists of dicts: {"payment_id": str, "amount_cents": int}.
    """
    unsettled = []
    for p in payments:
        settled = False
        for s in settlements:
            if s["payment_id"] == p["payment_id"]:
                settled = True
                break
        if not settled:
            unsettled.append(p["payment_id"])
    return unsettled


def merchant_fee_cents(amount_cents, rate_percent):
    """Fee in whole cents for one payment. rate_percent is text, for example "2.9"."""
    return round(amount_cents * float(rate_percent) / 100)


if __name__ == "__main__":
    payments = [{"payment_id": "p1", "amount_cents": 1000}, {"payment_id": "p2", "amount_cents": 2500},
                {"payment_id": "p3", "amount_cents": 700}]
    settlements = [{"payment_id": "p1", "amount_cents": 1000}, {"payment_id": "p2", "amount_cents": 2400}]
    print("unsettled:", find_unsettled(payments, settlements))
    print("fee on 250 cents at 1%:", merchant_fee_cents(250, "1"))
