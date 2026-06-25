import glob
import json
import os
import pickle
from datetime import datetime
from threading import Lock
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

FEATURE_NAMES = [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "SSLfinal_State",
    "Domain_registeration_length",
    "Favicon",
    "port",
    "HTTPS_token",
    "Request_URL",
    "URL_of_Anchor",
    "Links_in_tags",
    "SFH",
    "Submitting_to_email",
    "Abnormal_URL",
    "Redirect",
    "on_mouseover",
    "RightClick",
    "popUpWidnow",
    "Iframe",
    "age_of_domain",
    "DNSRecord",
    "web_traffic",
    "Page_Rank",
    "Google_Index",
    "Links_pointing_to_page",
    "Statistical_report",
]

MODEL_PATH = None
MODEL = None
PREDICTION_HISTORY_PATH = os.getenv("PREDICTION_HISTORY_PATH", os.path.join("Artifacts", "prediction_history.json"))
HISTORY_LOCK = Lock()

app = FastAPI(
    title="Network Security Phishing Detection",
    description="Inference API for the phishing detection model saved from the training pipeline.",
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    features: Dict[str, float]


class BatchPredictionRequest(BaseModel):
    instances: List[Dict[str, float]]


def find_latest_model_path() -> str:
    configured_path = os.getenv("MODEL_PATH")
    if configured_path:
        if os.path.exists(configured_path):
            return configured_path
        raise FileNotFoundError(f"MODEL_PATH is set but the file does not exist: {configured_path}")

    artifacts_dir = os.getenv("ARTIFACTS_DIR", "Artifacts")
    search_pattern = os.path.join(artifacts_dir, "*", "Model_Trainer", "Model_Trainer", "Model.pkl")
    candidates = glob.glob(search_pattern)
    if not candidates:
        raise FileNotFoundError(
            "No model file was found. Set MODEL_PATH or ensure the training artifacts are available under Artifacts/*/Model_Trainer/Model_Trainer/Model.pkl"
        )
    candidates.sort(key=os.path.getmtime, reverse=True)
    return candidates[0]


def load_model(model_path: str):
    with open(model_path, "rb") as file_obj:
        return pickle.load(file_obj)


def validate_feature_vector(feature_map: Dict[str, float]) -> np.ndarray:
    missing_features = [name for name in FEATURE_NAMES if name not in feature_map]
    extra_features = [name for name in feature_map if name not in FEATURE_NAMES]
    if missing_features or extra_features:
        message_parts = []
        if missing_features:
            message_parts.append(f"Missing features: {missing_features}")
        if extra_features:
            message_parts.append(f"Unexpected features: {extra_features}")
        raise HTTPException(status_code=422, detail="; ".join(message_parts))

    values = [float(feature_map[name]) for name in FEATURE_NAMES]
    return np.array(values, dtype=float).reshape(1, -1)


def get_model_root() -> Optional[str]:
    if not MODEL_PATH:
        return None
    marker = os.path.join("Model_Trainer", "Model_Trainer", "Model.pkl")
    if MODEL_PATH.endswith(marker):
        return MODEL_PATH[: -len(marker)].rstrip(os.sep)
    return None


def get_validation_test_path() -> Optional[str]:
    model_root = get_model_root()
    if not model_root:
        return None
    test_path = os.path.join(model_root, "Data_Validation", "valid_Data", "test.csv")
    return test_path if os.path.exists(test_path) else None


def get_underlying_estimator() -> Any:
    return getattr(MODEL, "model", MODEL)


def calculate_test_metrics() -> Dict[str, Optional[float]]:
    test_path = get_validation_test_path()
    if MODEL is None or test_path is None:
        return {"accuracy": None, "precision": None, "recall": None, "f1_score": None}

    test_frame = pd.read_csv(test_path)
    if "Result" not in test_frame.columns:
        return {"accuracy": None, "precision": None, "recall": None, "f1_score": None}

    features = test_frame[FEATURE_NAMES]
    y_true = test_frame["Result"].replace(-1, 0).astype(int)
    y_pred = np.asarray(MODEL.predict(features)).astype(int)

    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
    }


def get_feature_importance() -> List[Dict[str, float]]:
    estimator = get_underlying_estimator()
    importances = None

    if hasattr(estimator, "feature_importances_"):
        importances = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        importances = np.abs(np.asarray(estimator.coef_)).ravel()

    if importances is None:
        return []

    rows = [
        {"feature": feature, "importance": round(float(importance), 6)}
        for feature, importance in zip(FEATURE_NAMES, importances)
    ]
    rows.sort(key=lambda item: item["importance"], reverse=True)
    return rows


def empty_prediction_history() -> Dict[str, Any]:
    return {"total_predictions": 0, "attack_predictions": 0, "normal_predictions": 0, "runs": []}


def read_prediction_history() -> Dict[str, Any]:
    if not os.path.exists(PREDICTION_HISTORY_PATH):
        return empty_prediction_history()
    try:
        with open(PREDICTION_HISTORY_PATH, "r", encoding="utf-8") as file_obj:
            history = json.load(file_obj)
    except (json.JSONDecodeError, OSError):
        return empty_prediction_history()

    default_history = empty_prediction_history()
    default_history.update(history)
    default_history["runs"] = history.get("runs", [])
    return default_history


def write_prediction_history(history: Dict[str, Any]) -> None:
    directory = os.path.dirname(PREDICTION_HISTORY_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(PREDICTION_HISTORY_PATH, "w", encoding="utf-8") as file_obj:
        json.dump(history, file_obj, indent=2)


def record_prediction_run(predictions: List[int], mode: str) -> None:
    attack_count = sum(1 for value in predictions if int(value) == 0)
    normal_count = len(predictions) - attack_count
    run = {
        "run": f"{mode} {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": mode,
        "records": len(predictions),
        "attacks": attack_count,
        "normal": normal_count,
    }

    with HISTORY_LOCK:
        history = read_prediction_history()
        history["total_predictions"] = int(history.get("total_predictions", 0)) + len(predictions)
        history["attack_predictions"] = int(history.get("attack_predictions", 0)) + attack_count
        history["normal_predictions"] = int(history.get("normal_predictions", 0)) + normal_count
        history.setdefault("runs", []).append(run)
        history["runs"] = history["runs"][-200:]
        write_prediction_history(history)


def prediction_stats_response() -> Dict[str, Any]:
    with HISTORY_LOCK:
        history = read_prediction_history()
    total = int(history.get("total_predictions", 0))
    attacks = int(history.get("attack_predictions", 0))
    normal = int(history.get("normal_predictions", 0))
    attack_rate = round((attacks / total) * 100, 2) if total else 0
    runs = history.get("runs", [])
    return {
        "summary": {
            "total": total,
            "attacks": attacks,
            "normal": normal,
            "attack_rate": attack_rate,
        },
        "analysis_history": runs,
        "recent_analyses": runs[-10:],
    }


@app.on_event("startup")
def startup_event() -> None:
    global MODEL, MODEL_PATH
    try:
        MODEL_PATH = find_latest_model_path()
        MODEL = load_model(MODEL_PATH)
    except Exception as exc:
        raise RuntimeError(f"Failed to load inference model: {exc}") from exc


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "model_path": MODEL_PATH or "not loaded"}


@app.get("/model_info")
def model_info() -> Dict[str, Any]:
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")

    estimator = get_underlying_estimator()
    metrics = calculate_test_metrics()
    return {
        "model_name": "Network Security Phishing Detector",
        "algorithm": estimator.__class__.__name__,
        "training_dataset": "Network_Data/phisingData.csv",
        "feature_count": len(FEATURE_NAMES),
        "features": FEATURE_NAMES,
        "model_path": MODEL_PATH,
        "test_data_path": get_validation_test_path(),
        "metrics": metrics,
        "feature_importance": get_feature_importance(),
        "description": "Serialized NetworkModel containing preprocessing and the selected classifier from the training pipeline.",
    }


@app.get("/prediction_stats")
def prediction_stats() -> Dict[str, Any]:
    return prediction_stats_response()


@app.post("/predict")
def predict(request: PredictionRequest) -> Dict[str, List[int]]:
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")

    feature_array = validate_feature_vector(request.features)
    try:
        prediction = MODEL.predict(feature_array)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {exc}") from exc

    predictions = [int(value) for value in np.atleast_1d(prediction)]
    record_prediction_run(predictions, "Single")
    return {"predictions": predictions}


@app.post("/predict_batch")
def predict_batch(request: BatchPredictionRequest) -> Dict[str, List[int]]:
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")

    if not request.instances:
        raise HTTPException(status_code=422, detail="The instances list must contain at least one record")

    validated_arrays = []
    for record in request.instances:
        validated_arrays.append(validate_feature_vector(record))

    feature_matrix = np.vstack(validated_arrays)
    try:
        predictions = MODEL.predict(feature_matrix)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {exc}") from exc

    prediction_values = [int(value) for value in np.atleast_1d(predictions)]
    record_prediction_run(prediction_values, "Batch")
    return {"predictions": prediction_values}
