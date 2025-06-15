from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

from networksecurity.entity.artifact_entity import ClassificationMetrics

from sklearn.metrics import precision_score,f1_score,recall_score

def get_classificatin_score(y_true,y_pred)->ClassificationMetrics:
    try:
        model_precision_score=precision_score(y_true,y_pred)
        model_f1_score=f1_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)

        metrics=ClassificationMetrics(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    return metrics

