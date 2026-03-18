from fastapi import FastAPI
from fastapi import HTTPException


app = FastAPI()


BALANCE = {}

@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
            )
    return {"wallet": wallet_name, "balance": BALANCE[wallet_name]}


@app.post("/wallets/{name}")
def recieve_money(name: str, amount: int):
    if name not in BALANCE:
        BALANCE[name] = 0
    BALANCE[name] += amount
    return {
        "message": f"Added {amount} to {name}",
        "wallet_name": name,
        "new_balance": BALANCE[name]
    }