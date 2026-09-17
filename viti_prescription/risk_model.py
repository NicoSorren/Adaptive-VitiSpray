import math
from typing import List, Dict, Any
from models import Environment, Spot

def calculate_environmental_factor(env: Environment) -> float:
    """
    Factor de favorabilidad ambiental.
    Conceptualmente separado del modelo de dispersión espacial.
    NOTA: Inicialmente usamos un modelo simplificado MVP.
    """
    # Modelo MVP simple: penaliza levemente temperaturas extremas o humedades bajas
    # Este es el lugar para reemplazar con curvas paramétricas (e.g. Duthie 1997 para Erysiphe necator)
    f_temp = 1.0
    if env.temp < 10 or env.temp > 35:
        f_temp = 0.5
    
    f_hum = 1.0
    if env.hum < 40:
        f_hum = 0.6
        
    return f_temp * f_hum

def calculate_risk_profile(x: float, spot: Spot, env: Environment, params: Dict[str, Any], row_length: float) -> float:
    """
    Calcula el riesgo de tratamiento en una posición x debido a un foco específico,
    incluyendo la asimetría generada por el viento.
    
    Permite calcular R(x) en cualquier posición de la hilera validando [0, row_length].
    """
    if x < 0 or x > row_length:
        return 0.0

    distance = x - spot.x
    
    # Determinar si x está aguas arriba o aguas abajo del viento
    # wind_long_comp > 0 significa que el viento va hacia +X.
    wind_long_comp = env.viento_longitudinal
    
    # Decaimiento según la dirección relativa al viento
    if abs(wind_long_comp) < 1e-6:
        # Sin viento longitudinal, expansión simétrica
        k = (params["k_upwind"] + params["k_downwind"]) / 2.0
    elif wind_long_comp > 0:
        # Viento hacia +X
        if distance >= 0:
            k = params["k_downwind"] # A favor del viento
        else:
            k = params["k_upwind"]   # En contra del viento
    else:
        # Viento hacia -X
        if distance <= 0:
            k = params["k_downwind"] # A favor del viento
        else:
            k = params["k_upwind"]   # En contra del viento

    # El riesgo decae exponencialmente con la distancia. El factor confianza amplifica R0.
    R0 = params["base_risk"] * spot.conf
    risk_spatial = R0 * math.exp(-k * abs(distance))
    
    # Aplicar factor de favorabilidad ambiental
    risk_env = calculate_environmental_factor(env)
    
    return risk_spatial * risk_env
