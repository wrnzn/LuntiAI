"""
SQLite persistence for LuntiAI accounts, quotas, and prediction history.
"""

import json
import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Optional
from zoneinfo import ZoneInfo


DB_PATH = os.environ.get(
    "LUNTIAI_DB_PATH",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "instance", "users.db"),
)

FREE_DAILY_QUOTA = 3
PROMO_CODE = "LUNTIAI2026"
PHT = ZoneInfo("Asia/Manila")
USERNAME_RE = re.compile(r"^(?=.*[a-z])[a-z0-9][a-z0-9_-]{2,31}$")


def _connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def _connection():
    conn = _connect()
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def _now_iso() -> str:
    return datetime.now(PHT).isoformat()


def _today_pht() -> str:
    return datetime.now(PHT).date().isoformat()


def _quota_resets_at() -> str:
    now = datetime.now(PHT)
    tomorrow = (now + timedelta(days=1)).date()
    return datetime.combine(tomorrow, datetime.min.time(), tzinfo=PHT).isoformat()


def normalize_username(username: str) -> str:
    """Normalize a non-sensitive demo username."""
    normalized = (username or "").strip().lower()
    if not USERNAME_RE.fullmatch(normalized):
        raise ValueError(
            "Username must be 3-32 characters using letters, numbers, underscores, or hyphens"
        )
    return normalized


def _row_to_user(row: Optional[sqlite3.Row]) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    return {
        "id": row["id"],
        "username": row["username"],
        "display_name": row["display_name"],
        "tier": row["tier"],
        "query_count": row["query_count"],
        "query_date": row["query_date"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    with _connection() as conn:
        return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def init_db() -> None:
    with _connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                tier TEXT DEFAULT 'free',
                query_count INTEGER DEFAULT 0,
                query_date TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                barangay TEXT,
                inputs_json TEXT NOT NULL,
                best_crop TEXT NOT NULL,
                confidence REAL NOT NULL,
                crop_category TEXT NOT NULL,
                full_response_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )


def create_user(username: str, display_name: str, password: str) -> dict[str, Any]:
    from auth import hash_password

    normalized_username = normalize_username(username)
    clean_display_name = (display_name or "").strip()
    if not clean_display_name:
        raise ValueError("Display name is required")
    if len(clean_display_name) > 50:
        raise ValueError("Display name must contain at most 50 characters")
    if len(password or "") < 8:
        raise ValueError("Password must be at least 8 characters")

    now = _now_iso()
    try:
        with _connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO users (
                    username, display_name, password_hash, tier, query_count,
                    query_date, created_at, updated_at
                )
                VALUES (?, ?, ?, 'free', 0, ?, ?, ?)
                """,
                (
                    normalized_username,
                    clean_display_name,
                    hash_password(password),
                    _today_pht(),
                    now,
                    now,
                ),
            )
            user_id = cursor.lastrowid
    except sqlite3.IntegrityError as exc:
        raise ValueError("Username already registered") from exc

    user = get_user(user_id)
    if user is None:
        raise ValueError("User could not be created")
    return user


def authenticate_user(username: str, password: str) -> Optional[dict[str, Any]]:
    from auth import verify_password

    try:
        normalized_username = normalize_username(username)
    except ValueError:
        return None
    row = _get_user_by_username(normalized_username)
    if row is None or not verify_password(password, row["password_hash"]):
        return None
    return _row_to_user(row)


def get_user(user_id: int) -> Optional[dict[str, Any]]:
    with _connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return _row_to_user(row)


def update_user(user_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    from auth import hash_password

    updates: list[str] = []
    values: list[Any] = []

    if "display_name" in fields and fields["display_name"] is not None:
        display_name = str(fields["display_name"]).strip()
        if not display_name:
            raise ValueError("Display name is required")
        if len(display_name) > 50:
            raise ValueError("Display name must contain at most 50 characters")
        updates.append("display_name = ?")
        values.append(display_name)

    if "password" in fields and fields["password"]:
        password = str(fields["password"])
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        updates.append("password_hash = ?")
        values.append(hash_password(password))

    if "tier" in fields and fields["tier"] is not None:
        tier = str(fields["tier"]).lower()
        if tier not in {"free", "premium"}:
            raise ValueError("Tier must be free or premium")
        updates.append("tier = ?")
        values.append(tier)

    if not updates:
        user = get_user(user_id)
        if user is None:
            raise ValueError("User not found")
        return user

    updates.append("updated_at = ?")
    values.append(_now_iso())
    values.append(user_id)

    with _connection() as conn:
        cursor = conn.execute(
            f"UPDATE users SET {', '.join(updates)} WHERE id = ?",
            tuple(values),
        )
        if cursor.rowcount == 0:
            raise ValueError("User not found")

    user = get_user(user_id)
    if user is None:
        raise ValueError("User not found")
    return user


def delete_user(user_id: int) -> bool:
    with _connection() as conn:
        cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        return cursor.rowcount > 0


def get_quota_status(user_id: int) -> dict[str, Any]:
    user = get_user(user_id)
    if user is None:
        raise ValueError("User not found")
    if user["tier"] == "premium":
        return {"allowed": True, "remaining": -1, "resets_at": _quota_resets_at()}

    count = user["query_count"] if user["query_date"] == _today_pht() else 0
    remaining = max(FREE_DAILY_QUOTA - count, 0)
    return {"allowed": remaining > 0, "remaining": remaining, "resets_at": _quota_resets_at()}


def check_and_increment_quota(user_id: int) -> dict[str, Any]:
    conn = _connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if row is None:
            raise ValueError("User not found")
        if row["tier"] == "premium":
            conn.commit()
            return {"allowed": True, "remaining": -1, "resets_at": _quota_resets_at()}

        today = _today_pht()
        current_count = row["query_count"] if row["query_date"] == today else 0
        if current_count >= FREE_DAILY_QUOTA:
            conn.commit()
            return {"allowed": False, "remaining": 0, "resets_at": _quota_resets_at()}

        next_count = current_count + 1
        conn.execute(
            """
            UPDATE users
            SET query_count = ?, query_date = ?, updated_at = ?
            WHERE id = ?
            """,
            (next_count, today, _now_iso(), user_id),
        )
        conn.commit()
        return {
            "allowed": True,
            "remaining": max(FREE_DAILY_QUOTA - next_count, 0),
            "resets_at": _quota_resets_at(),
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def record_prediction(user_id: int, inputs: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    created_at = _now_iso()
    with _connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO prediction_history (
                user_id, barangay, inputs_json, best_crop, confidence,
                crop_category, full_response_json, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                inputs.get("barangay"),
                json.dumps(inputs),
                result["best_crop"],
                float(result["confidence"]),
                result["crop_category"],
                json.dumps(result),
                created_at,
            ),
        )
        history_id = cursor.lastrowid
    return {"id": history_id, "created_at": created_at}


def get_prediction_history(user_id: int, limit: int = 50) -> list[dict[str, Any]]:
    safe_limit = max(1, min(int(limit), 100))
    with _connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM prediction_history
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (user_id, safe_limit),
        ).fetchall()

    history = []
    for row in rows:
        history.append(
            {
                "id": row["id"],
                "barangay": row["barangay"],
                "inputs": json.loads(row["inputs_json"]),
                "best_crop": row["best_crop"],
                "confidence": row["confidence"],
                "crop_category": row["crop_category"],
                "full_response": json.loads(row["full_response_json"])
                if row["full_response_json"]
                else None,
                "created_at": row["created_at"],
            }
        )
    return history


def redeem_code(user_id: int, code: str) -> dict[str, Any]:
    if (code or "").strip().upper() != PROMO_CODE:
        raise ValueError("Invalid promo code")
    return update_user(user_id, {"tier": "premium"})
