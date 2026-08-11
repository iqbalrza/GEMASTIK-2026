import json
import logging
from typing import Dict, Any
from ai.utils import constants
from ai.utils.helpers import load_json, calculate_deviation

logger = logging.getLogger(__name__)

class PlantFirstEvaluator:
    def __init__(self):
        self.ideal_ranges = load_json(constants.IDEAL_RANGES_PATH)
        self.remediation_rules = load_json(constants.REMEDIATION_RULES_PATH)
        
        if not self.ideal_ranges:
            logger.warning(f"Failed to load ideal ranges from {constants.IDEAL_RANGES_PATH}")
        if not self.remediation_rules:
            logger.warning(f"Failed to load remediation rules from {constants.REMEDIATION_RULES_PATH}")

    def evaluate(self, crop_name: str, temperature: float, humidity: float, ph: float) -> Dict[str, Any]:
        """
        Evaluates soil conditions for a specific crop.
        """
        crop_name = crop_name.lower().replace(" ", "_")
        
        if crop_name not in self.ideal_ranges:
            return {
                "error": f"Crop '{crop_name}' not found in profiles.",
                "valid": False
            }
            
        profile = self.ideal_ranges[crop_name]
        
        # Evaluate each parameter
        temp_eval = self._evaluate_parameter("temperature", temperature, profile["temperature"])
        hum_eval = self._evaluate_parameter("humidity", humidity, profile["humidity"])
        ph_eval = self._evaluate_parameter("ph", ph, profile["ph"])
        
        # Calculate overall verdict
        evaluations = [temp_eval, hum_eval, ph_eval]
        status_counts = {
            constants.EvalStatus.IDEAL: 0,
            constants.EvalStatus.MARGINAL: 0,
            constants.EvalStatus.TIDAK_COCOK: 0
        }
        
        for e in evaluations:
            status_counts[e["status"]] += 1
            
        if status_counts[constants.EvalStatus.TIDAK_COCOK] > 0:
            overall_verdict = constants.OverallVerdict.TIDAK_COCOK
        elif status_counts[constants.EvalStatus.MARGINAL] > 0:
            overall_verdict = constants.OverallVerdict.CUKUP_COCOK
        else:
            overall_verdict = constants.OverallVerdict.SANGAT_COCOK
            
        return {
            "valid": True,
            "crop": crop_name,
            "display_name": profile["display_name"],
            "verdict": overall_verdict,
            "verdict_icon": constants.VERDICT_ICONS[overall_verdict],
            "details": {
                "temperature": temp_eval,
                "humidity": hum_eval,
                "ph": ph_eval
            }
        }
        
    def _evaluate_parameter(self, param: str, value: float, range_def: Dict[str, Any]) -> Dict[str, Any]:
        ideal_min = range_def["min"]
        ideal_max = range_def["max"]
        
        deviation = calculate_deviation(value, ideal_min, ideal_max)
        
        if deviation == 0:
            status = constants.EvalStatus.IDEAL
            remediation = None
        else:
            # Calculate percentage deviation
            range_span = ideal_max - ideal_min
            # Prevent division by zero if min==max
            if range_span == 0:
                range_span = 1.0 
            
            percent_deviation = abs(deviation) / range_span
            
            if percent_deviation <= constants.MARGINAL_THRESHOLD:
                status = constants.EvalStatus.MARGINAL
            else:
                status = constants.EvalStatus.TIDAK_COCOK
                
            # Get remediation
            rule_key = "too_low" if deviation < 0 else "too_high"
            remediation = self.remediation_rules.get(param, {}).get(rule_key, {})
            
        return {
            "value": value,
            "ideal_min": ideal_min,
            "ideal_max": ideal_max,
            "status": status,
            "icon": constants.STATUS_ICONS[status],
            "deviation": deviation,
            "remediation": remediation
        }
