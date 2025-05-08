import os
import sys
from sklearn.metrics import f1_score, precision_score, recall_score,accuracy_score
from Student_Performace.entity.artfact_entity import ClassificationMetricArtifact
from Student_Performace.exception.exception import StudentException

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        accuracy=accuracy_score(y_true,y_pred)
        precision = precision_score(y_true, y_pred, average="weighted")
        recall = recall_score(y_true, y_pred, average="weighted")
        f1 = f1_score(y_true, y_pred, average="weighted")

        classification_metric = ClassificationMetricArtifact(
        
            accuracy_score=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1  # if this is actually f1, consider renaming it
        )

        return classification_metric

    except Exception as e:
        raise StudentException(e, sys)


    

