from pathlib import Path
import sys

# La carpeta vitispray/paths.py está dentro de Adaptive-VitiSpray/src/vitispray/
# Subimos un nivel para llegar a vitispray/, otro para src/ y otro para la raíz.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 1. Validación Básica de Seguridad
# Comprobamos la existencia de marcadores clave de la raíz del proyecto
if not (PROJECT_ROOT / "00_gestion").exists() and not (PROJECT_ROOT / "requirements.txt").exists():
    raise RuntimeError(
        f"ERROR CRÍTICO: PROJECT_ROOT se resolvió como '{PROJECT_ROOT}', "
        "pero no parece ser la raíz del repositorio (faltan carpetas base). "
        "Verifica la ubicación de src/paths.py."
    )

# 2. Carpetas Principales (Relativas a PROJECT_ROOT)
DATASETS_DIR = PROJECT_ROOT / "02_datasets"
YOLO_DIR = PROJECT_ROOT / "03_ia_yolo"
OUTPUTS_DIR = YOLO_DIR / "runs"
WEIGHTS_DIR = YOLO_DIR / "weights"
PRESCRIPTION_DIR = PROJECT_ROOT / "05_mapa_prescripcion" / "viti_prescription"

# 3. Rutas Específicas
DETECT_FIELD_DATASET = DATASETS_DIR / "dataset_detect_field"
MONOCLASS_DATASET = DATASETS_DIR / "dataset_monoclass_powdery_mildew"
