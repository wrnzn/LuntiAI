"""
LuntiAI — Model Training Pipeline
===================================
Trains a Random Forest classifier on the Philippine crop dataset
and saves the model artifacts for production use.

Features:
- Stratified train/test split (80/20)
- Hyperparameter-tuned Random Forest (200 estimators)
- Classification report with per-crop metrics
- Feature importance analysis
- Model serialization via joblib

Author: LuntiAI Team
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib


def load_dataset(path):
    """Load and validate the Philippine crop dataset."""
    print("Loading dataset...")
    df = pd.read_csv(path)
    print(f"  Loaded {len(df):,} rows x {len(df.columns)} columns")
    print(f"  Crops: {df['label'].nunique()} unique classes")
    print(f"  Features: {[c for c in df.columns if c != 'label']}")

    # Validate no nulls
    assert not df.isnull().any().any(), "Dataset contains null values!"
    return df


def train_model(df):
    """Train and evaluate the Random Forest model."""
    # Separate features and labels
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'OM']
    X = df[feature_cols].values
    y_raw = df['label'].values

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    print(f"\nLabel encoding: {dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))}")

    # Stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain set: {len(X_train):,} samples")
    print(f"Test set:  {len(X_test):,} samples")

    # Train Random Forest
    print("\nTraining Random Forest classifier...")
    print("  n_estimators=200, max_depth=25, min_samples_split=5")
    start_time = time.time()

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=25,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,  # Use all CPU cores
        class_weight='balanced',  # Handle slight class imbalance
    )

    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    print(f"  Training completed in {training_time:.1f}s")

    # Evaluate
    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nOverall Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")

    # Per-class report
    print(f"\nClassification Report:")
    report = classification_report(
        y_test, y_pred,
        target_names=label_encoder.classes_,
        digits=4
    )
    print(report)

    # Feature importance
    print("Feature Importance Rankings:")
    importances = model.feature_importances_
    feature_importance = sorted(
        zip(feature_cols, importances),
        key=lambda x: x[1],
        reverse=True
    )
    for i, (feat, imp) in enumerate(feature_importance, 1):
        bar = "#" * int(imp * 50)
        print(f"  {i}. {feat:<15} {imp:.4f} {bar}")

    return model, label_encoder, accuracy, feature_importance


def save_artifacts(model, label_encoder, accuracy, feature_importance, output_dir):
    """Save model artifacts to disk."""
    os.makedirs(output_dir, exist_ok=True)

    # Save model
    model_path = os.path.join(output_dir, "crop_model.pkl")
    joblib.dump(model, model_path, compress=3)
    model_size = os.path.getsize(model_path) / (1024 * 1024)
    print(f"\nModel saved: {model_path} ({model_size:.1f} MB)")

    # Save label encoder
    encoder_path = os.path.join(output_dir, "label_encoder.pkl")
    joblib.dump(label_encoder, encoder_path)
    print(f"Encoder saved: {encoder_path}")

    # Save metadata
    metadata = {
        "model_type": "RandomForestClassifier",
        "n_estimators": 200,
        "accuracy": round(accuracy, 4),
        "n_classes": len(label_encoder.classes_),
        "classes": list(label_encoder.classes_),
        "features": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "OM"],
        "feature_importance": {feat: round(imp, 4) for feat, imp in feature_importance},
        "training_data": "data/philippine_crop_dataset.csv",
        "training_samples": 96000,
        "test_samples": 24000,
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    meta_path = os.path.join(output_dir, "model_metadata.json")
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved: {meta_path}")


def main():
    """Main training pipeline."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "data", "philippine_crop_dataset.csv")
    model_dir = os.path.join(base_dir, "model")

    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset not found at {dataset_path}")
        print("Run 'python data/generate_dataset.py' first.")
        sys.exit(1)

    # Load
    df = load_dataset(dataset_path)

    # Train
    model, label_encoder, accuracy, feature_importance = train_model(df)

    # Save
    save_artifacts(model, label_encoder, accuracy, feature_importance, model_dir)

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    print(f"Artifacts saved to: {model_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
