import os
from models import Spot, Environment
from config import ROW_CONFIG, MVP_RISK_PARAMS
from prescription import generate_treatment_zone, merge_overlapping_zones, export_prescription_json
from visualization import plot_prescription_map, plot_risk_functions

def main():
    print("Iniciando generación de mapa de prescripción VitiSpray...")
    
    # 1. Definir entorno (viento a 0 grados, es decir, a favor de la hilera)
    env = Environment(
        viento_vel=3.0,
        viento_dir=0.0,
        temp=22.0,
        hum=65.0
    )
    
    # 2. Definir focos de ejemplo
    focos = [
        Spot(id=1, x=20.0, conf=0.91),
        Spot(id=2, x=48.0, conf=0.87),
        Spot(id=3, x=75.0, conf=0.95)
    ]
    
    row_length = ROW_CONFIG["length"]
    
    print(f"Longitud de hilera: {row_length}m. Viento: {env.viento_vel}m/s a {env.viento_dir}º")
    
    # 3. Generar zonas de tratamiento individuales
    individual_zones = []
    for spot in focos:
        zone = generate_treatment_zone(spot, env, MVP_RISK_PARAMS, row_length)
        individual_zones.append(zone)
        print(f"Foco {spot.id} -> Zona individual: [{zone.start:.2f}, {zone.end:.2f}] (Rmax: {zone.risk_max:.2f})")
        
    # 4. Fusionar zonas superpuestas
    merged_zones = merge_overlapping_zones(individual_zones)
    
    print("\nZonas fusionadas resultantes:")
    for i, z in enumerate(merged_zones):
        print(f"  Zona {i+1}: [{z.start:.2f}, {z.end:.2f}], Focos origen: {z.source_spot_ids}")
        
    # 5. Exportar y visualizar
    os.makedirs("outputs", exist_ok=True)
    json_path = os.path.join("outputs", "prescription_map.json")
    export_prescription_json(merged_zones, env, MVP_RISK_PARAMS, row_length, json_path)
    print(f"\nMapa exportado a {json_path}")
    
    map_path = os.path.join("outputs", "prescription_map.png")
    plot_prescription_map(focos, individual_zones, merged_zones, env, MVP_RISK_PARAMS, row_length, map_path)
    
    risk_path = os.path.join("outputs", "risk_profile.png")
    plot_risk_functions(focos, env, MVP_RISK_PARAMS, row_length, risk_path)
    print(f"Gráficas generadas en el directorio 'outputs'.")

if __name__ == "__main__":
    main()
