import os
import sys
from sklearn.metrics import f1_score,precision,recall
from Student_Performace.entity.artfact_entity import ClassificationMetricArtifact
from Student_Performace.exception.exception import StudentException


def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        f1score=f1_score(y_true,y_pred)
        precision_score=precision(y_true,y_pred)
        recall_score=recall(y_true,y_pred)
        classification_metric=ClassificationMetricArtifact(f1_score=f1score,precision=precision+score,recall=recall_score)
        return classification_metric
    except Exception as e:
        raise StudentException(e,sys)

    

