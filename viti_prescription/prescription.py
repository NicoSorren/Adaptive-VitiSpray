import json
import numpy as np
from typing import List, Dict, Any
from models import Spot, Environment, TreatmentZone
from risk_model import calculate_risk_profile
from config import ROW_CONFIG, MVP_RISK_PARAMS

def generate_treatment_zone(spot: Spot, env: Environment, params: Dict[str, Any], row_length: float) -> TreatmentZone:
    """
    Genera la zona de tratamiento individual para un foco escaneando la fila.
    """
    threshold = params["risk_threshold"]
    resolution = ROW_CONFIG["resolution"]
    
    # Rango de busqueda: todo el viñedo, o acotado
    # Para ser exactos, barremos la hilera con la resolución dada
    xs = np.arange(0, row_length + resolution, resolution)
    risk_values = [calculate_risk_profile(x, spot, env, params, row_length) for x in xs]
    
    # Encontrar índices donde el riesgo es mayor o igual al umbral
    above_threshold = [i for i, r in enumerate(risk_values) if r >= threshold]
    
    if not above_threshold:
        return TreatmentZone(start=spot.x, end=spot.x, risk_max=calculate_risk_profile(spot.x, spot, env, params, row_length), source_spot_ids=[spot.id])
        
    start_x = max(0.0, xs[above_threshold[0]])
    end_x = min(row_length, xs[above_threshold[-1]])
    max_risk = max(risk_values)
    
    return TreatmentZone(start=start_x, end=end_x, risk_max=max_risk, source_spot_ids=[spot.id])

def merge_overlapping_zones(zones: List[TreatmentZone]) -> List[TreatmentZone]:
    """
    Fusiona zonas que se solapan y mantiene trazabilidad de los focos que las generaron.
    """
    if not zones:
        return []
        
    # Ordenar por el punto de inicio
    sorted_zones = sorted(zones, key=lambda z: z.start)
    merged = [sorted_zones[0]]
    
    for current in sorted_zones[1:]:
        previous = merged[-1]
        # Si se solapan o son contiguas
        if current.start <= previous.end:
            # Fusionar
            previous.end = max(previous.end, current.end)
            previous.risk_max = max(previous.risk_max, current.risk_max)
            # Agregar IDs de focos sin duplicados
            for s_id in current.source_spot_ids:
                if s_id not in previous.source_spot_ids:
                    previous.source_spot_ids.append(s_id)
        else:
            merged.append(current)
            
    return merged

def export_prescription_json(zones: List[TreatmentZone], env: Environment, params: Dict[str, Any], row_length: float, filename: str):
    """
    Exporta las zonas de prescripción fusionadas en un formato JSON listo para Webots.
    Incluye metadata del modelo y entorno.
    """
    data = {
        "metadata": {
            "model_type": "MVP_distance_decay",
            "environment": {
                "wind_speed_ms": env.viento_vel,
                "wind_direction_deg": env.viento_dir,
                "temperature_c": env.temp,
                "humidity_percent": env.hum
            },
            "parameters": params
        },
        "row_id": 1,
        "row_length": row_length,
        "zones": [
            {
                "start": round(z.start, 2),
                "end": round(z.end, 2),
                "risk_max": round(z.risk_max, 4),
                "source_spot_ids": z.source_spot_ids
            }
            for z in zones
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
