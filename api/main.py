"""
LuntiAI — FastAPI Backend
===========================
Production-grade API for crop recommendation, weather data,
and barangay soil profiles.

Endpoints:
    POST /predict          — Crop prediction from soil & climate data
    GET  /barangays        — List all Tagum barangays with soil profiles
    GET  /weather/{name}   — Live weather for a barangay
    GET  /health           — Health check
    GET  /docs             — Auto-generated Swagger UI (built-in)

Author: LuntiAI Team
"""

import os
import sys
try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional in lean test environments
    def load_dotenv(*args, **kwargs):
        return False

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
import json
from typing import Any, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import numpy as np
import joblib
try:
    import shap
except ImportError:  # pragma: no cover - optional for tests and lean installs
    shap = None

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import auth
import database
from barangay_data import TAGUM_BARANGAYS, get_fertilizer_recommendations, get_crop_economics
from weather_service import get_weather_data

# =============================================================================
# App Configuration
# =============================================================================

app = FastAPI(
    title="LuntiAI API",
    description="Precision Agriculture Crop Recommendation System for Tagum City, Davao del Norte",
    version="1.0.0",
    docs_url="/docs",
)

# CORS — allow all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Load Model
# =============================================================================

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model")
model = None
label_encoder = None
model_metadata = None
explainer = None


def load_model():
    """Load trained Random Forest model and label encoder."""
    global model, label_encoder, model_metadata, explainer

    model_path = os.path.join(MODEL_DIR, "crop_model.pkl")
    encoder_path = os.path.join(MODEL_DIR, "label_encoder.pkl")
    meta_path = os.path.join(MODEL_DIR, "model_metadata.json")

    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}")
        return False

    model = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)

    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            model_metadata = json.load(f)

    # Initialize SHAP explainer
    if shap is not None:
        try:
            explainer = shap.TreeExplainer(model)
            print("SHAP explainer initialized.")
        except Exception as e:
            print(f"WARNING: Could not initialize SHAP explainer: {e}")
    else:
        print("WARNING: SHAP package not installed; explanations disabled.")

    print(f"Model loaded: {(model_metadata or {}).get('accuracy', 'N/A')} accuracy")
    return True


# Load on startup
@app.on_event("startup")
async def startup():
    database.init_db()
    if not load_model():
        print("WARNING: Model not loaded. Run train_model.py first.")


# =============================================================================
# Request/Response Models
# =============================================================================

class PredictionRequest(BaseModel):
    N: float = Field(..., ge=0, le=200, description="Nitrogen (mg/kg)")
    P: float = Field(..., ge=0, le=200, description="Phosphorus (mg/kg)")
    K: float = Field(..., ge=0, le=250, description="Potassium (mg/kg)")
    temperature: float = Field(..., ge=10, le=45, description="Temperature (Celsius)")
    humidity: float = Field(..., ge=0, le=100, description="Humidity (%)")
    ph: float = Field(..., ge=3, le=10, description="Soil pH")
    rainfall: float = Field(..., ge=0, le=500, description="Monthly rainfall (mm)")
    OM: float = Field(..., ge=0, le=15, description="Organic Matter (%)")
    barangay: Optional[str] = Field(None, description="Barangay name (optional)")


class RegisterRequest(BaseModel):
    phone: str = Field(..., description="PH mobile number")
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    phone: str = Field(..., description="PH mobile number")
    password: str = Field(..., min_length=8)


class UpdateMeRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    password: Optional[str] = Field(None, min_length=8)


class RedeemRequest(BaseModel):
    code: str = Field(..., min_length=1)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict
    quota: dict


class UserResponse(BaseModel):
    user: dict
    quota: dict


class PredictionResponse(BaseModel):
    best_crop: str
    confidence: float
    message: str
    top_predictions: Optional[list] = None
    fertilizer_recommendations: Optional[list] = None
    shap_explanation: Optional[dict] = None
    barangay_info: Optional[dict] = None
    crop_economics: Optional[dict] = None
    crop_category: str = ""
    maturity_years_to_first_harvest: Optional[str] = None
    maturity_warning: bool = False
    intercropping: Optional[list] = None
    is_quota_limited: bool = False
    quota_remaining: int = 0
    quota_resets_at: Optional[str] = None


# =============================================================================
# API Endpoints
# =============================================================================

# OpenWeatherMap API key
WEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")

TREE_CROP_METADATA = {
    "Coconut": {
        "maturity_years_to_first_harvest": "6-8",
        "intercropping": ["Cacao"],
    },
    "Coffee": {
        "maturity_years_to_first_harvest": "3-4",
        "intercropping": ["Banana"],
    },
    "Mango": {
        "maturity_years_to_first_harvest": "5-7",
        "intercropping": ["Vegetables"],
    },
    "Apple": {"maturity_years_to_first_harvest": None, "intercropping": []},
    "Orange": {"maturity_years_to_first_harvest": None, "intercropping": []},
    "Papaya": {"maturity_years_to_first_harvest": None, "intercropping": []},
}
ROOT_CROPS = {"Cassava", "Sweet Potato"}
SHORT_CYCLE_CROPS = {
    "Rice", "Corn", "Mungbean", "Lentil", "Banana", "Cotton", "Jute",
    "Watermelon", "Pomegranate", "Grapes", "Maize", "Chickpea",
    "Kidney Beans", "Pigeon Peas", "Moth Beans", "Black Gram",
}


def _model_dump(model_obj: BaseModel) -> dict[str, Any]:
    if hasattr(model_obj, "model_dump"):
        return model_obj.model_dump()
    return model_obj.dict()


def _crop_metadata(crop_name: str) -> dict[str, Any]:
    if crop_name in TREE_CROP_METADATA:
        return {
            "crop_category": "tree_crop",
            "maturity_years_to_first_harvest": TREE_CROP_METADATA[crop_name][
                "maturity_years_to_first_harvest"
            ],
            "maturity_warning": True,
        }
    if crop_name in ROOT_CROPS:
        return {
            "crop_category": "root_crop",
            "maturity_years_to_first_harvest": None,
            "maturity_warning": False,
        }
    return {
        "crop_category": "short_cycle_crop",
        "maturity_years_to_first_harvest": None,
        "maturity_warning": False,
    }


def _intercropping_for(crop_name: str) -> Optional[list]:
    suggestions = TREE_CROP_METADATA.get(crop_name, {}).get("intercropping", [])
    return suggestions or None


def _user_response(user: dict) -> dict:
    return {"user": user, "quota": database.get_quota_status(user["id"])}


def _auth_response(user: dict) -> dict:
    return {
        "access_token": auth.create_access_token(user["id"]),
        "token_type": "bearer",
        **_user_response(user),
    }


@app.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    try:
        user = database.create_user(request.phone, request.name, request.password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _auth_response(user)


@app.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    user = database.authenticate_user(request.phone, request.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return _auth_response(user)


@app.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(auth.get_current_user)):
    return _user_response(current_user)


@app.put("/me", response_model=UserResponse)
async def update_me(request: UpdateMeRequest, current_user: dict = Depends(auth.get_current_user)):
    fields = {key: value for key, value in _model_dump(request).items() if value is not None}
    try:
        user = database.update_user(current_user["id"], fields)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _user_response(user)


@app.delete("/me")
async def delete_me(current_user: dict = Depends(auth.get_current_user)):
    database.delete_user(current_user["id"])
    return {"message": "Account deleted"}


@app.post("/redeem", response_model=UserResponse)
async def redeem(request: RedeemRequest, current_user: dict = Depends(auth.get_current_user)):
    try:
        user = database.redeem_code(current_user["id"], request.code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _user_response(user)


@app.get("/history")
async def history(limit: int = 50, current_user: dict = Depends(auth.get_current_user)):
    if current_user["tier"] != "premium":
        raise HTTPException(status_code=403, detail="Premium feature")
    rows = database.get_prediction_history(current_user["id"], limit=limit)
    return {"total": len(rows), "history": rows}


@app.post("/predict", response_model=PredictionResponse)
async def predict_crop(request: PredictionRequest, current_user: dict = Depends(auth.get_current_user)):
    """
    Predict the optimal crop based on soil and climate conditions.
    Returns top-3 predictions with confidence scores and fertilizer advice.
    """
    if model is None or label_encoder is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please restart server.")

    features = np.array([
        request.N, request.P, request.K,
        request.temperature, request.humidity,
        request.ph, request.rainfall, request.OM
    ]).reshape(1, -1)

    # Predict
    prediction_encoded = model.predict(features)[0]
    crop_name = label_encoder.inverse_transform([prediction_encoded])[0]

    # Probabilities
    probabilities = model.predict_proba(features)[0]
    max_prob = float(max(probabilities))
    confidence = round(max_prob * 100, 2)
    metadata = _crop_metadata(str(crop_name))
    quota = database.check_and_increment_quota(current_user["id"])
    has_full_access = bool(quota["allowed"])

    # Top 5 predictions
    top_indices = np.argsort(probabilities)[::-1][:5]
    top_predictions = []
    for idx in top_indices:
        label = label_encoder.inverse_transform([idx])[0]
        prob = round(float(probabilities[idx]) * 100, 2)
        if prob > 0.5:  # Only show meaningful predictions
            top_predictions.append({"crop": str(label), "probability": prob})

    # Fertilizer recommendations
    fertilizer_recs = get_fertilizer_recommendations(
        request.N, request.P, request.K, request.ph, request.OM
    )

    # Barangay info if provided
    barangay_info = None
    if request.barangay and request.barangay in TAGUM_BARANGAYS:
        brgy = TAGUM_BARANGAYS[request.barangay]
        barangay_info = {
            "name": request.barangay,
            "soil_type": brgy["soil_type"],
            "classification": brgy["classification"],
            "primary_crops": brgy["primary_crops"],
            "notes": brgy["notes"],
        }

    # SHAP Explanation
    shap_explanation = None
    if explainer is not None:
        try:
            # Get SHAP values for the predicted class
            predicted_class_idx = int(prediction_encoded)
            shap_values = explainer.shap_values(features)
            
            # Extract values for the specific class. shap_values can be a list or a 3D array depending on version
            if isinstance(shap_values, list):
                class_shap = shap_values[predicted_class_idx][0]
            else:
                class_shap = shap_values[0, :, predicted_class_idx]
                
            feature_names = ["N", "P", "K", "Temp", "Humidity", "pH", "Rainfall", "OM"]
            
            # Combine names and values, sort by absolute impact
            impacts = sorted(zip(feature_names, class_shap), key=lambda x: abs(x[1]), reverse=True)
            
            shap_explanation = {
                "top_positive": [
                    {"feature": feat, "value": float(val)} for feat, val in impacts if val > 0
                ][:3],
                "top_negative": [
                    {"feature": feat, "value": float(val)} for feat, val in impacts if val < 0
                ][:3],
            }
        except Exception as e:
            print(f"SHAP calculation error: {e}")

    # Crop economics for ROI
    crop_econ = get_crop_economics(crop_name)

    intercropping = None
    if metadata["crop_category"] == "tree_crop":
        intercropping = _intercropping_for(str(crop_name))

    message = f"Based on your soil and climate conditions, {crop_name} is the recommended crop."
    if not has_full_access:
        message = (
            f"{crop_name} is the recommended crop. Daily free quota reached; "
            "Premium details unlock after reset or upgrade."
        )

    result = {
        "best_crop": str(crop_name),
        "confidence": confidence,
        "message": message,
        "top_predictions": top_predictions,
        "fertilizer_recommendations": fertilizer_recs,
        "shap_explanation": shap_explanation,
        "barangay_info": barangay_info,
        "crop_economics": crop_econ,
        "crop_category": metadata["crop_category"],
        "maturity_years_to_first_harvest": metadata["maturity_years_to_first_harvest"],
        "maturity_warning": metadata["maturity_warning"],
        "intercropping": intercropping,
        "is_quota_limited": not has_full_access,
        "quota_remaining": quota["remaining"],
        "quota_resets_at": quota["resets_at"],
    }
    database.record_prediction(current_user["id"], _model_dump(request), result)
    return PredictionResponse(**result)


@app.get("/barangays")
async def list_barangays():
    """List all 23 Tagum City barangays with their soil profiles."""
    result = {}
    for name, data in TAGUM_BARANGAYS.items():
        result[name] = {
            "N": data["N"],
            "P": data["P"],
            "K": data["K"],
            "OM": data.get("OM", 2.5),
            "pH": data["pH"],
            "soil_type": data["soil_type"],
            "classification": data["classification"],
            "primary_crops": data["primary_crops"],
            "notes": data["notes"],
            "lat": data["lat"],
            "lon": data["lon"],
        }
    return {"barangays": result, "total": len(result)}


@app.get("/weather/{barangay}")
async def get_barangay_weather(barangay: str):
    """Get current weather for a specific barangay in Tagum City."""
    if barangay not in TAGUM_BARANGAYS:
        raise HTTPException(
            status_code=404,
            detail=f"Barangay '{barangay}' not found. Use /barangays to see available options."
        )

    brgy = TAGUM_BARANGAYS[barangay]
    weather = get_weather_data(brgy["lat"], brgy["lon"], WEATHER_API_KEY)

    return {
        "barangay": barangay,
        "weather": weather,
        "soil": {
            "N": brgy["N"],
            "P": brgy["P"],
            "K": brgy["K"],
            "OM": brgy.get("OM", 2.5),
            "pH": brgy["pH"],
            "soil_type": brgy["soil_type"],
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "label_encoder_loaded": label_encoder is not None,
        "model_accuracy": model_metadata.get("accuracy") if model_metadata else None,
        "supported_crops": list(label_encoder.classes_) if label_encoder is not None else [],
        "barangays_loaded": len(TAGUM_BARANGAYS),
    }


@app.get("/")
async def root():
    """API documentation redirect."""
    return {
        "name": "LuntiAI API",
        "version": "1.0.0",
        "description": "Precision Agriculture for Tagum City",
        "docs": "/docs",
        "endpoints": {
            "POST /predict": "Crop recommendation prediction",
            "GET /barangays": "List all barangay soil profiles",
            "GET /weather/{barangay}": "Live weather data",
            "GET /health": "System health check",
        }
    }


# =============================================================================
# Serve Frontend (Static Files)
# =============================================================================

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


# =============================================================================
# Run
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
