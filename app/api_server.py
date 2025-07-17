from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
from pathlib import Path
import logging
from app.logger import get_logger
from app.news_pipeline import run_news_pipeline

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger (fallback in case get_logger fails)
try:
    logger = get_logger(__name__)
except Exception:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

@app.get("/")
def root():
    return {"message": "FastAPI backend is running. Visit /docs for the API documentation."}

@app.get("/api/health")
def health_check():
    logger.info("Health check OK")
    return {"status": "OK"}

@app.post("/api/fetch-news")
def fetch_and_cluster_news():
    try:
        logger.info("Running news clustering pipeline...")
        result = run_news_pipeline()
        return result
    except Exception as e:
        logger.exception("Error during fetch-and-cluster.")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/api/news")
def get_clustered_news():
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output/ exists
    output_file = output_dir / "results.json"

    if not output_file.exists():
        logger.warning("No results file found.")
        return JSONResponse(
            status_code=404,
            content={"error": "No results file found."}
        )

    try:
        with output_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate structure
        if isinstance(data, dict):
            data_list = list(data.values())
        elif isinstance(data, list):
            data_list = data
        else:
            logger.error("Unexpected data format in results.json")
            return JSONResponse(
                status_code=500,
                content={"error": "Unexpected results format"}
            )

        # Ensure articles are list format
        for cluster in data_list:
            if not isinstance(cluster.get("articles", []), list):
                cluster["articles"] = [cluster["articles"]]

        logger.info("Returning properly structured clustered news data.")
        return data_list

    except Exception as e:
        logger.exception("Error reading or parsing clustered news.")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to read clusters: {str(e)}"}
        )
