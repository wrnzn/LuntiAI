"""
PostgreSQL persistence for LuntiAI accounts, quotas, and prediction history.
Migrated from SQLite to psycopg2 for Neon/Vercel deployment.
"""

import json
import os
import re
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Optional
from zoneinfo import ZoneInfo

import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get("DATABASE_URL", "")

FREE_DAILY_QUOTA = 3
PROMO_CODE = "LUNTIAI2026"
PHT = ZoneInfo("Asia/Manila")
PHONE_RE = re.compile(r"^(?:\+63|63|0)9\d{9}$")


def _connect() -> psycopg2.extensions.connection:
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@contextmanager
def _connection():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def _now_iso() -> str:
    return datetime.now(PHT).isoformat()


def _today_pht() -> str:
    return datetime.now(PHT).date().isoformat()


def _quota_resets_at() -> str:
    now = datetime.now(PHT)
    tomorrow = (now + timedelta(days=1)).date()
    return datetime.combine(tomorrow, datetime.min.time(), tzinfo=PHT).isoformat()


def normalize_phone(phone: str) -> str:
    """Normalize PH mobile numbers to +639XXXXXXXXX."""
    compact = re.sub(r"[\s-]", "", phone or "")
    if not PHONE_RE.match(compact):
        raise ValueError("Phone must be a valid PH mobile number")
    if compact.startswith("+63"):
        return compact
    if compact.startswith("63"):
        return f"+{compact}"
    return f"+63{compact[1:]}"


def _row_to_user(row: Optional[dict]) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    return {
        "id": row["id"],
        "phone": row["phone"],
        "name": row["name"],
        "tier": row["tier"],
        "query_count": row["query_count"],
        "query_date": row["query_date"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _get_user_by_phone(phone: str) -> Optional[dict]:
    with _connection() as conn:
        cur = _cursor(conn)
        cur.execute("SELECT * FROM users WHERE phone = %s", (phone,))
        return cur.fetchone()


def init_db() -> None:
    with _connection() as conn:
        cur = _cursor(conn)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                phone TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                tier TEXT DEFAULT 'free',
                query_count INTEGER DEFAULT 0,
                query_date TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS prediction_history (
                id SERIAL PRIMARY KEY,
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


def create_user(phone: str, name: str, password: str) -> dict[str, Any]:
    from auth import hash_password

    normalized_phone = normalize_phone(phone)
    clean_name = (name or "").strip()
    if not clean_name:
        raise ValueError("Name is required")
    if len(password or "") < 8:
        raise ValueError("Password must be at least 8 characters")

    now = _now_iso()
    try:
        with _connection() as conn:
            cur = _cursor(conn)
            cur.execute(
                """
                INSERT INTO users (
                    phone, name, password_hash, tier, query_count,
                    query_date, created_at, updated_at
                )
                VALUES (%s, %s, %s, 'free', 0, %s, %s, %s)
                RETURNING id
                """,
                (normalized_phone, clean_name, hash_password(password), _today_pht(), now, now),
            )
            user_id = cur.fetchone()["id"]
    except psycopg2.errors.UniqueViolation as exc:
        raise ValueError("Phone already registered") from exc

    user = get_user(user_id)
    if user is None:
        raise ValueError("User could not be created")
    return user


def authenticate_user(phone: str, password: str) -> Optional[dict[str, Any]]:
    from auth import verify_password

    try:
        normalized_phone = normalize_phone(phone)
    except ValueError:
        return None
    row = _get_user_by_phone(normalized_phone)
    if row is None or not verify_password(password, row["password_hash"]):
        return None
    return _row_to_user(row)


def get_user(user_id: int) -> Optional[dict[str, Any]]:
    with _connection() as conn:
        cur = _cursor(conn)
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
    return _row_to_user(row)


def update_user(user_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    from auth import hash_password

    updates: list[str] = []
    values: list[Any] = []

    if "name" in fields and fields["name"] is not None:
        name = str(fields["name"]).strip()
        if not name:
            raise ValueError("Name is required")
        updates.append("name = %s")
        values.append(name)

    if "password" in fields and fields["password"]:
        password = str(fields["password"])
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        updates.append("password_hash = %s")
        values.append(hash_password(password))

    if "tier" in fields and fields["tier"] is not None:
        tier = str(fields["tier"]).lower()
        if tier not in {"free", "premium"}:
            raise ValueError("Tier must be free or premium")
        updates.append("tier = %s")
        values.append(tier)

    if not updates:
        user = get_user(user_id)
        if user is None:
            raise ValueError("User not found")
        return user

    updates.append("updated_at = %s")
    values.append(_now_iso())
    values.append(user_id)

    with _connection() as conn:
        cur = _cursor(conn)
        cur.execute(
            f"UPDATE users SET {', '.join(updates)} WHERE id = %s",
            tuple(values),
        )
        if cur.rowcount == 0:
            raise ValueError("User not found")

    user = get_user(user_id)
    if user is None:
        raise ValueError("User not found")
    return user


def delete_user(user_id: int) -> bool:
    with _connection() as conn:
        cur = _cursor(conn)
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        return cur.rowcount > 0


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
        conn.autocommit = False
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE id = %s FOR UPDATE", (user_id,))
        row = cur.fetchone()
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
        cur.execute(
            """
            UPDATE users
            SET query_count = %s, query_date = %s, updated_at = %s
            WHERE id = %s
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
        cur = _cursor(conn)
        cur.execute(
            """
            INSERT INTO prediction_history (
                user_id, barangay, inputs_json, best_crop, confidence,
                crop_category, full_response_json, created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
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
        history_id = cur.fetchone()["id"]
    return {"id": history_id, "created_at": created_at}


def get_prediction_history(user_id: int, limit: int = 50) -> list[dict[str, Any]]:
    safe_limit = max(1, min(int(limit), 100))
    with _connection() as conn:
        cur = _cursor(conn)
        cur.execute(
            """
            SELECT *
            FROM prediction_history
            WHERE user_id = %s
            ORDER BY created_at DESC, id DESC
            LIMIT %s
            """,
            (user_id, safe_limit),
        )
        rows = cur.fetchall()

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
