import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Spot, Environment, TreatmentZone
from config import MVP_RISK_PARAMS
from risk_model import calculate_risk_profile
from prescription import merge_overlapping_zones, generate_treatment_zone

def test_merge_overlapping_zones():
    z1 = TreatmentZone(start=10.0, end=20.0, risk_max=0.5, source_spot_ids=[1])
    z2 = TreatmentZone(start=18.0, end=30.0, risk_max=0.6, source_spot_ids=[2])
    
    merged = merge_overlapping_zones([z1, z2])
    assert len(merged) == 1
    assert merged[0].start == 10.0
    assert merged[0].end == 30.0
    assert merged[0].risk_max == 0.6
    assert set(merged[0].source_spot_ids) == {1, 2}

def test_merge_separate_zones():
    z1 = TreatmentZone(start=10.0, end=20.0, risk_max=0.5, source_spot_ids=[1])
    z2 = TreatmentZone(start=25.0, end=30.0, risk_max=0.6, source_spot_ids=[2])
    
    merged = merge_overlapping_zones([z1, z2])
    assert len(merged) == 2

def test_zero_spots():
    assert merge_overlapping_zones([]) == []

def test_risk_profile_wind_direction():
    # Viento a favor de la hilera (+X)
    env_fwd = Environment(viento_vel=5.0, viento_dir=0.0, temp=22.0, hum=60.0)
    # Viento en contra de la hilera (-X)
    env_bwd = Environment(viento_vel=5.0, viento_dir=180.0, temp=22.0, hum=60.0)
    # Sin viento longitudinal
    env_perp = Environment(viento_vel=5.0, viento_dir=90.0, temp=22.0, hum=60.0)
    
    spot = Spot(id=1, x=50.0, conf=1.0)
    
    # Comprobar viento a favor (+X)
    # Hacia +X el k_downwind rige (menor k, cae más lento, riesgo mayor). 
    # Hacia -X el k_upwind rige (mayor k, cae más rápido, riesgo menor).
    risk_fwd_plus5 = calculate_risk_profile(55.0, spot, env_fwd, MVP_RISK_PARAMS, 100.0)
    risk_fwd_minus5 = calculate_risk_profile(45.0, spot, env_fwd, MVP_RISK_PARAMS, 100.0)
    assert risk_fwd_plus5 > risk_fwd_minus5
    
    # Comprobar viento en contra (-X)
    risk_bwd_plus5 = calculate_risk_profile(55.0, spot, env_bwd, MVP_RISK_PARAMS, 100.0)
    risk_bwd_minus5 = calculate_risk_profile(45.0, spot, env_bwd, MVP_RISK_PARAMS, 100.0)
    assert risk_bwd_minus5 > risk_bwd_plus5
    
    # Comprobar perpendicular (sin viento longitudinal), deberian ser simétricos
    # Porque env.viento_longitudinal = 0
    risk_perp_plus5 = calculate_risk_profile(55.0, spot, env_perp, MVP_RISK_PARAMS, 100.0)
    risk_perp_minus5 = calculate_risk_profile(45.0, spot, env_perp, MVP_RISK_PARAMS, 100.0)
    assert risk_perp_plus5 == risk_perp_minus5

def test_risk_profile_boundaries():
    env = Environment(viento_vel=0.0, viento_dir=0.0, temp=22.0, hum=60.0)
    spot = Spot(id=1, x=5.0, conf=1.0)
    
    # Riesgo fuera de los límites es 0
    assert calculate_risk_profile(-10.0, spot, env, MVP_RISK_PARAMS, 100.0) == 0.0
    assert calculate_risk_profile(110.0, spot, env, MVP_RISK_PARAMS, 100.0) == 0.0

def test_generate_treatment_zone_limits():
    env = Environment(viento_vel=0.0, viento_dir=0.0, temp=22.0, hum=60.0)
    # Foco muy cerca del inicio, la zona de tratamiento no debería extenderse a x < 0
    spot = Spot(id=1, x=0.5, conf=1.0)
    zone = generate_treatment_zone(spot, env, MVP_RISK_PARAMS, 100.0)
    
    assert zone.start >= 0.0
    assert zone.end <= 100.0
