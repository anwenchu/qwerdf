"""Synthetic existing call site; review input only, not a runnable service."""


def read_closing_total(binding, ledger_client):
    # Business precondition: positions and open orders have already been checked.
    snapshot = ledger_client.read_snapshot(
        account_id=binding.trading_account_id,
        settlement_asset=binding.settlement_asset,
    )
    if snapshot is None or snapshot.total is None:
        raise ValueError("balance snapshot unavailable; do not settle")
    return snapshot.total
