"""
Constants and configuration for the AI system.
"""
import os
from pathlib import Path
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CROP_PROFILES_DIR = DATA_DIR / "crop_profiles"

DATASET_PATH = RAW_DATA_DIR / "P2L_Urban_Crop_Dataset.csv"
IDEAL_RANGES_PATH = CROP_PROFILES_DIR / "crop_ideal_ranges.json"
REMEDIATION_RULES_PATH = PROJECT_ROOT / "ai" / "models" / "evaluator" / "remediation_rules.json"
MODEL_DIR = PROJECT_ROOT / "ai" / "models" / "recommender"
MODEL_PATH = MODEL_DIR / "model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"

# ──────────────────────────────────────────────
# Feature columns
# ──────────────────────────────────────────────
FEATURE_COLUMNS = ["temperature", "humidity", "ph"]
LABEL_COLUMN = "label"

# ──────────────────────────────────────────────
# Sensor validation ranges
# ──────────────────────────────────────────────
SENSOR_RANGES = {
    "temperature": {"min": 0.0, "max": 60.0, "unit": "°C"},
    "humidity": {"min": 0.0, "max": 100.0, "unit": "%"},
    "ph": {"min": 0.0, "max": 14.0, "unit": ""},
}

# ──────────────────────────────────────────────
# Evaluation thresholds
# ──────────────────────────────────────────────
MARGINAL_THRESHOLD = 0.10  # 10% deviation from ideal range


class EvalStatus(str, Enum):
    """Status evaluasi per parameter."""
    IDEAL = "IDEAL"
    MARGINAL = "MARGINAL"
    TIDAK_COCOK = "TIDAK_COCOK"


class OverallVerdict(str, Enum):
    """Verdict keseluruhan."""
    SANGAT_COCOK = "SANGAT COCOK"
    CUKUP_COCOK = "CUKUP COCOK"
    TIDAK_COCOK = "TIDAK COCOK"


VERDICT_ICONS = {
    OverallVerdict.SANGAT_COCOK: "😊",
    OverallVerdict.CUKUP_COCOK: "😐",
    OverallVerdict.TIDAK_COCOK: "😟",
}

STATUS_ICONS = {
    EvalStatus.IDEAL: "✅",
    EvalStatus.MARGINAL: "⚠️",
    EvalStatus.TIDAK_COCOK: "❌",
}

# ──────────────────────────────────────────────
# Label display names (Indonesian)
# ──────────────────────────────────────────────
CROP_DISPLAY_NAMES = {
    "cabai_rawit": "Cabai Rawit",
    "cabai_keriting": "Cabai Keriting",
    "tomat": "Tomat",
    "bayam": "Bayam",
    "kangkung": "Kangkung",
    "selada": "Selada",
    "terong": "Terong",
    "timun": "Timun",
    "bawang_merah": "Bawang Merah",
    "bawang_putih": "Bawang Putih",
    "sawi": "Sawi",
    "kacang_panjang": "Kacang Panjang",
    "seledri": "Seledri",
    "pare": "Pare",
    "kemangi": "Kemangi",
}

# ──────────────────────────────────────────────
# Model config
# ──────────────────────────────────────────────
KNN_N_NEIGHBORS = 5
KNN_WEIGHTS = "distance"
TOP_N_DEFAULT = 5

# ──────────────────────────────────────────────
# LLM config
# ──────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", os.getenv("GEMINI_API_KEY", "")) # Fallback to using the one in env if user pasted groq key there
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "500"))
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.7"))

# Chatbot config
CHATBOT_MAX_HISTORY = 10
CHATBOT_MAX_INPUT_LENGTH = 500
