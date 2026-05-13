import os
import sys
import uuid
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))


PREDICTION_PAYLOAD = {
    "N": 70,
    "P": 45,
    "K": 55,
    "temperature": 27.5,
    "humidity": 82,
    "ph": 5.8,
    "rainfall": 175,
    "OM": 3.2,
    "barangay": "Madaum",
}


class FakeModel:
    def predict(self, features):
        return np.array([0])

    def predict_proba(self, features):
        return np.array([[0.9, 0.08, 0.02]])


class FakeLabelEncoder:
    classes_ = np.array(["Coconut", "Rice", "Corn"])

    def inverse_transform(self, values):
        return np.array([self.classes_[int(value)] for value in values])


@pytest.fixture()
def client(monkeypatch):
    import database
    import main

    db_dir = Path.cwd() / ".tmp"
    db_dir.mkdir(exist_ok=True)
    db_path = db_dir / f"test-users-{uuid.uuid4().hex}.db"

    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")
    monkeypatch.setattr(database, "DB_PATH", str(db_path))
    monkeypatch.setattr(main, "model", FakeModel())
    monkeypatch.setattr(main, "label_encoder", FakeLabelEncoder())
    monkeypatch.setattr(main, "explainer", None)
    monkeypatch.setattr(main, "load_model", lambda: True)
    database.init_db()

    with TestClient(main.app) as test_client:
        yield test_client

    try:
        db_path.unlink()
    except FileNotFoundError:
        pass


def test_free_user_quota_soft_lock_redeem_and_history(client):
    unauthenticated = client.post("/predict", json=PREDICTION_PAYLOAD)
    assert unauthenticated.status_code == 401

    registered = client.post(
        "/register",
        json={"phone": "09171234567", "name": "Kiko", "password": "secret123"},
    )
    assert registered.status_code == 200
    token = registered.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for expected_remaining in [2, 1, 0]:
        predicted = client.post("/predict", json=PREDICTION_PAYLOAD, headers=headers)
        assert predicted.status_code == 200
        body = predicted.json()
        assert body["best_crop"] == "Coconut"
        assert body["confidence"] == 90.0
        assert body["crop_category"] == "tree_crop"
        assert body["maturity_years_to_first_harvest"] == "6-8"
        assert body["maturity_warning"]
        assert body["top_predictions"]
        assert body["fertilizer_recommendations"]
        assert body["crop_economics"]
        assert body["intercropping"] is None
        assert body["is_quota_limited"] is False
        assert body["quota_remaining"] == expected_remaining

    locked = client.post("/predict", json=PREDICTION_PAYLOAD, headers=headers)
    assert locked.status_code == 200
    locked_body = locked.json()
    assert locked_body["best_crop"] == "Coconut"
    assert locked_body["confidence"] == 90.0
    assert locked_body["is_quota_limited"] is True
    assert locked_body["quota_remaining"] == 0
    assert locked_body["top_predictions"] is None
    assert locked_body["fertilizer_recommendations"] is None
    assert locked_body["shap_explanation"] is None
    assert locked_body["crop_economics"] is None

    free_history = client.get("/history", headers=headers)
    assert free_history.status_code == 403

    redeemed = client.post("/redeem", json={"code": "LUNTIAI2026"}, headers=headers)
    assert redeemed.status_code == 200
    assert redeemed.json()["user"]["tier"] == "premium"

    premium_prediction = client.post("/predict", json=PREDICTION_PAYLOAD, headers=headers)
    assert premium_prediction.status_code == 200
    premium_body = premium_prediction.json()
    assert premium_body["is_quota_limited"] is False
    assert premium_body["quota_remaining"] == -1
    assert "Cacao" in premium_body["intercropping"]

    history = client.get("/history", headers=headers)
    assert history.status_code == 200
    assert history.json()["total"] == 5
    assert history.json()["history"][0]["best_crop"] == "Coconut"


def test_user_can_update_profile_and_delete_account(client):
    registered = client.post(
        "/register",
        json={"phone": "+639181234567", "name": "Ana", "password": "secret123"},
    )
    assert registered.status_code == 200
    headers = {"Authorization": f"Bearer {registered.json()['access_token']}"}

    updated = client.put("/me", json={"name": "Ana Cruz"}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["user"]["name"] == "Ana Cruz"

    deleted = client.delete("/me", headers=headers)
    assert deleted.status_code == 200

    me = client.get("/me", headers=headers)
    assert me.status_code == 401
