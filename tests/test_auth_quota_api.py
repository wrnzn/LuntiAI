import os
import sys

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
def client(monkeypatch, tmp_path):
    import database
    import main

    db_path = tmp_path / "test-users.db"

    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-that-is-at-least-32-chars")
    monkeypatch.setattr(database, "DB_PATH", str(db_path))
    monkeypatch.setattr(main, "model", FakeModel())
    monkeypatch.setattr(main, "label_encoder", FakeLabelEncoder())
    monkeypatch.setattr(main, "explainer", None)
    monkeypatch.setattr(main, "load_model", lambda: True)
    database.init_db()

    with TestClient(main.app) as test_client:
        yield test_client



def test_free_user_quota_soft_lock_redeem_and_history(client):
    unauthenticated = client.post("/predict", json=PREDICTION_PAYLOAD)
    assert unauthenticated.status_code == 401

    registered = client.post(
        "/register",
        json={"username": "kiko-demo", "display_name": "Kiko", "password": "secret123"},
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
        assert "Cacao" in body["intercropping"]
        assert body["is_quota_limited"] is False
        assert body["quota_remaining"] == expected_remaining

    locked = client.post("/predict", json=PREDICTION_PAYLOAD, headers=headers)
    assert locked.status_code == 200
    locked_body = locked.json()
    assert locked_body["best_crop"] == "Coconut"
    assert locked_body["confidence"] == 90.0
    assert locked_body["is_quota_limited"] is True
    assert locked_body["quota_remaining"] == 0
    # Data still returned — frontend handles gating visually
    assert locked_body["top_predictions"] is not None
    assert locked_body["fertilizer_recommendations"] is not None
    assert locked_body["crop_economics"] is not None

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
        json={"username": "ana-demo", "display_name": "Ana", "password": "secret123"},
    )
    assert registered.status_code == 200
    headers = {"Authorization": f"Bearer {registered.json()['access_token']}"}

    updated = client.put("/me", json={"display_name": "Ana Cruz"}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["user"]["display_name"] == "Ana Cruz"

    deleted = client.delete("/me", headers=headers)
    assert deleted.status_code == 200

    me = client.get("/me", headers=headers)
    assert me.status_code == 401


def test_registration_rejects_phone_number_as_username(client):
    response = client.post(
        "/register",
        json={"username": "09171234567", "display_name": "Demo", "password": "secret123"},
    )

    assert response.status_code == 400
    assert "Username must" in response.json()["detail"]


def test_malformed_token_is_rejected(client):
    response = client.get("/me", headers={"Authorization": "Bearer not.a.valid-token"})

    assert response.status_code == 401
