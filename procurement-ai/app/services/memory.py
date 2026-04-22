from __future__ import annotations

history: list[dict] = []


def store_decision(decision: dict) -> None:
    history.append(decision)


def get_history(limit: int = 25) -> list[dict]:
    return history[-limit:]
