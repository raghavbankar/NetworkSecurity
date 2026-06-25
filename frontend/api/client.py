from time import perf_counter

import requests
import streamlit as st

from config import BACKEND_URL, REQUEST_TIMEOUT


class ApiError(Exception):
    pass


def _handle_response(response):
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except ValueError:
            pass
        raise ApiError(f"{response.status_code}: {detail}") from exc
    except ValueError as exc:
        raise ApiError("Backend returned an invalid JSON response") from exc


def check_health():
    started = perf_counter()
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=REQUEST_TIMEOUT)
        elapsed_ms = round((perf_counter() - started) * 1000, 2)
        return {"ok": response.ok, "elapsed_ms": elapsed_ms, "data": _handle_response(response)}
    except requests.RequestException as exc:
        elapsed_ms = round((perf_counter() - started) * 1000, 2)
        return {"ok": False, "elapsed_ms": elapsed_ms, "error": str(exc)}


@st.cache_data(ttl=60)
def get_model_info():
    try:
        response = requests.get(f"{BACKEND_URL}/model_info", timeout=REQUEST_TIMEOUT)
        return {"ok": response.ok, "data": _handle_response(response)}
    except (requests.RequestException, ApiError) as exc:
        return {"ok": False, "error": str(exc)}


@st.cache_data(ttl=5)
def get_prediction_stats():
    try:
        response = requests.get(f"{BACKEND_URL}/prediction_stats", timeout=REQUEST_TIMEOUT)
        return {"ok": response.ok, "data": _handle_response(response)}
    except (requests.RequestException, ApiError) as exc:
        return {"ok": False, "error": str(exc)}


def predict_single(features):
    try:
        response = requests.post(
            f"{BACKEND_URL}/predict",
            json={"features": features},
            timeout=REQUEST_TIMEOUT,
        )
        get_prediction_stats.clear()
        return _handle_response(response)
    except requests.RequestException as exc:
        raise ApiError(str(exc)) from exc


def predict_batch(instances):
    try:
        response = requests.post(
            f"{BACKEND_URL}/predict_batch",
            json={"instances": instances},
            timeout=REQUEST_TIMEOUT,
        )
        get_prediction_stats.clear()
        return _handle_response(response)
    except requests.RequestException as exc:
        raise ApiError(str(exc)) from exc
