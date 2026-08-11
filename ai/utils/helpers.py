import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

def load_json(filepath: Path | str) -> Dict[str, Any]:
    """Loads a JSON file and returns its content as a dictionary."""
    path = Path(filepath)
    if not path.exists():
        logger.error(f"JSON file not found: {path}")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON {path}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error reading JSON {path}: {e}")
        return {}

def calculate_deviation(current: float, ideal_min: float, ideal_max: float) -> float:
    """
    Calculates the deviation of a value from the ideal range.
    Returns 0 if within range, positive deviation if above max, negative if below min.
    """
    if current < ideal_min:
        return current - ideal_min
    if current > ideal_max:
        return current - ideal_max
    return 0.0

def format_sensor_value(value: float, param: str, constants_module) -> str:
    """Formats a sensor value with its unit based on constants."""
    ranges = constants_module.SENSOR_RANGES.get(param)
    unit = ranges["unit"] if ranges else ""
    return f"{value:.2f}{unit}"
