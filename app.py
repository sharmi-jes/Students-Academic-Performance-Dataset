import sys
import os
import traceback
import certifi
from dotenv import load_dotenv
import pymongo
import pandas as pd
from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from Student_Performace.exception.exception import StudentException
from Student_Performace.logging.logger import logging
from Student_Performace.pipeline.training_pipeline import TrainingPipeline
# from Student_Performace.constant.training_pipeline import USERNAME, PASSWORD
from Student_Performace.utils.main_utils.utils import load_object
from Student_Performace.utils.ml_utils.model.estimator import NetworkModel
from Student_Performace.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)

# Load environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
if mongo_db_url is None:
    raise ValueError("MONGO_DB_URL not found in environment variables")

# Setup MongoDB client
ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            return Response(content="Only CSV files are supported.", status_code=400)

        df = pd.read_csv(file.file)
        print({"columns": df.columns.tolist(), "rows": len(df)})

        # Load preprocessor and model
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        label_encoders = load_object("final_model/label_encoders.pkl")

        # Debug feature check
        print("Expected model features:", preprocessor.get_feature_names_out())
        print("Received features:", df.columns.tolist())

        # Predict
        network_model = NetworkModel(preprocessor=preprocessor, model=model, label_encoders=label_encoders)
        y_pred = network_model.predict(df)

        df['predicted_column'] = y_pred

        # Save to CSV
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)

        # Return HTML table
        try:
            table_html = df.to_html(classes='table table-striped')
            return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        except Exception:
            # If HTML template not found, fallback to JSON
            return {"predictions": y_pred.tolist()}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))  # 👈 This line is critical
    app_run(app, host="0.0.0.0", port=port)

