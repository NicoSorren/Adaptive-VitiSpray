import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any
from models import Spot, Environment, TreatmentZone
from risk_model import calculate_risk_profile
from config import ROW_CONFIG

def plot_prescription_map(spots: List[Spot], individual_zones: List[TreatmentZone], merged_zones: List[TreatmentZone], env: Environment, params: Dict[str, Any], row_length: float, save_path: str = None):
    """
    Gráfica 1: Mapa general de la hilera con zonas de prescripción finales.
    """
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Línea base de la hilera
    ax.plot([0, row_length], [0, 0], color='green', linewidth=4, label='Hilera de vid')
    
    # Focos detectados
    spot_xs = [s.x for s in spots]
    spot_confs = [s.conf for s in spots]
    ax.scatter(spot_xs, [0.1]*len(spots), c=spot_confs, cmap='Reds', s=100, label='Focos de Oídio', zorder=5, edgecolors='black')
    
    # Zonas fusionadas (finales)
    for i, z in enumerate(merged_zones):
        label = 'Zona de Tratamiento' if i == 0 else ""
        ax.plot([z.start, z.end], [-0.1, -0.1], color='red', linewidth=8, alpha=0.6, label=label)
        
    # Dirección del viento
    wind_comp = env.viento_longitudinal
    wind_text = f"Viento: {env.viento_vel} m/s (Dir: {env.viento_dir}º)"
    if wind_comp > 0:
        wind_dir_symbol = "-->"
    elif wind_comp < 0:
        wind_dir_symbol = "<--"
    else:
        wind_dir_symbol = "---"
        
    plt.title(f"Mapa de Prescripción - VitiSpray\n{wind_text} {wind_dir_symbol}")
    ax.set_xlim(0, row_length)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xlabel("Distancia longitudinal (m)")
    ax.legend(loc='upper right')
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.close(fig)

def plot_risk_functions(spots: List[Spot], env: Environment, params: Dict[str, Any], row_length: float, save_path: str = None):
    """
    Gráfica 2: Perfil continuo de riesgo R(x) a lo largo de la hilera superponiendo múltiples focos.
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    
    xs = np.arange(0, row_length + ROW_CONFIG["resolution"], ROW_CONFIG["resolution"])
    
    total_risk = np.zeros_like(xs)
    
    for s in spots:
        r_vals = np.array([calculate_risk_profile(x, s, env, params, row_length) for x in xs])
        ax.plot(xs, r_vals, linestyle='--', alpha=0.5, label=f'Riesgo Foco {s.id}')
        total_risk = np.maximum(total_risk, r_vals)  # El riesgo general puede ser el máximo (o la suma)
        
    ax.plot(xs, total_risk, color='red', linewidth=2, label='Riesgo Total (Max)')
    ax.axhline(y=params["risk_threshold"], color='black', linestyle=':', label='Umbral Tratamiento')
    
    ax.set_xlim(0, row_length)
    ax.set_xlabel("Distancia longitudinal (m)")
    ax.set_ylabel("Nivel de Riesgo R(x)")
    ax.set_title(f"Perfil de Riesgo Epidemiológico Asimétrico (Viento Dir: {env.viento_dir}º)")
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.close(fig)
