import os
import json
import numpy as np
from app.logger import get_logger

logger = get_logger(__name__)

def convert_numpy_types(obj):
    """
    Recursively convert NumPy data types to native Python types.
    """
    if isinstance(obj, dict):
        return {str(k): convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def save_to_json(results, filename="output/results.json"):
    """
    Save the final cluster data with proper conversion.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    clean_results = convert_numpy_types(results)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(clean_results, f, indent=4, ensure_ascii=False)

    logger.info(f"✅ Results saved to {filename}")
