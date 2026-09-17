"""
Script para generar inferencias visuales en alta resolución
sobre hojas con Oídio confirmado.
"""

from pathlib import Path
from ultralytics import YOLO
from vitispray.paths import MONOCLASS_DATASET, PROJECT_ROOT

def test_visual_predictions():
    from vitispray.paths import YOLO_RUNS_DIR, YOLO_PREDICTIONS_DIR
    weights_path = YOLO_RUNS_DIR / "train" / "monoclass_pm_v1" / "weights" / "best.pt"
    dataset_dir = MONOCLASS_DATASET / "valid"
    output_dir = YOLO_PREDICTIONS_DIR / "predicciones_visuales"
    
    print("=" * 70)
    print("Iniciando inferencia visual en alta resolucion...")
    print("=" * 70)
    
    # 1. Buscar imagenes que tengan anotaciones de oidio confirmadas
    labels_dir = dataset_dir / "labels"
    images_dir = dataset_dir / "images"
    
    sample_images = []
    for lbl in labels_dir.glob("*.txt"):
        if lbl.stat().st_size > 0: # tiene al menos 1 mancha de oidio
            img_match = list(images_dir.glob(f"{lbl.stem}.*"))
            if img_match:
                sample_images.append(str(img_match[0]))
            if len(sample_images) >= 6: # tomamos 6 ejemplos claros
                break
                
    print(f"Seleccionadas {len(sample_images)} fotos con oidio confirmado para visualizar.")
    
    # 2. Cargar modelo y predecir
    model = YOLO(weights_path)
    results = model.predict(
        source=sample_images,
        conf=0.25,
        save=True,
        project=str(output_dir.parent),
        name=output_dir.name,
        exist_ok=True,
        line_width=2
    )
    
    print("\n" + "=" * 70)
    print(f"Predicciones guardadas en alta resolucion en: {output_dir}")
    print("=" * 70)

if __name__ == "__main__":
    test_visual_predictions()
