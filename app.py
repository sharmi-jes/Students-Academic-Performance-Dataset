import sys
import os

import certifi
from dotenv import load_dotenv
import pymongo
import pandas as pd

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from Student_Performace.exception.exception import StudentException
from Student_Performace.logging.logger import logging
from Student_Performace.pipeline.training_pipeline import TrainingPipeline
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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Jinja2 templates
templates = Jinja2Templates(directory="./templates")

# Routes
@app.get("/", tags=["Root"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train", tags=["Model Training"])
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise StudentException(e, sys)


# Run the app
if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
