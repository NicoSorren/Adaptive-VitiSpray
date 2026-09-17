# viti_prescription/config.py

# Parámetros experimentales del MVP para el modelo espacial
# NOTA: Estos son parámetros paramétricos (MVP), NO epidemiológicos validados.
MVP_RISK_PARAMS = {
    "k_upwind": 0.5,         # Decaimiento del riesgo en contra del viento (mayor k = decae más rápido = menor distancia)
    "k_downwind": 0.15,      # Decaimiento del riesgo a favor del viento (menor k = decae más lento = mayor distancia)
    "risk_threshold": 0.2,   # Umbral a partir del cual se considera zona de tratamiento
    "base_risk": 1.0         # Riesgo inicial en el centro del foco (R0)
}

# Configuración de la simulación / hilera
ROW_CONFIG = {
    "length": 100.0,         # Longitud de la hilera en metros
    "resolution": 0.1        # Resolución espacial en metros (para cálculos discretos / gráficos)
}
