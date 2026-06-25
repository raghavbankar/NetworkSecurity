from io import StringIO

import pandas as pd

from utils.features import FEATURE_NAMES, label_for_prediction, risk_for_prediction


def validate_input_frame(frame):
    missing = [name for name in FEATURE_NAMES if name not in frame.columns]
    extra = [name for name in frame.columns if name not in FEATURE_NAMES and name != "Result"]
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}"
    if extra:
        return False, f"Unexpected columns: {', '.join(extra)}"
    return True, "CSV schema looks good."


def frame_to_instances(frame):
    feature_frame = frame[FEATURE_NAMES].copy()
    for column in FEATURE_NAMES:
        feature_frame[column] = pd.to_numeric(feature_frame[column], errors="raise")
    return feature_frame.to_dict(orient="records")


def attach_predictions(frame, predictions):
    result = frame.copy()
    result["Prediction"] = [label_for_prediction(value) for value in predictions]
    result["Risk Level"] = [risk_for_prediction(value) for value in predictions]
    result["Prediction Code"] = [int(value) for value in predictions]
    return result


def prediction_summary(predictions):
    total = len(predictions)
    attacks = sum(1 for value in predictions if int(value) == 0)
    normal = total - attacks
    attack_rate = round((attacks / total) * 100, 2) if total else 0
    return {
        "total": total,
        "attacks": attacks,
        "normal": normal,
        "attack_rate": attack_rate,
    }


def make_report_csv(results_frame):
    buffer = StringIO()
    results_frame.to_csv(buffer, index=False)
    return buffer.getvalue()

