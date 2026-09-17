"""
Script para entrenar YOLOv11s-detect en el dataset unificado a campo (Bounding Boxes).
Modelo mono-clase exclusivo para Oídio (Powdery Mildew) en viñedos.
"""

import sys
from pathlib import Path
import argparse
import torch
from ultralytics import YOLO

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Entrenar YOLOv11s-detect para Oídio a Campo")
    parser.add_argument("--epochs", type=int, default=60, help="Número de épocas de entrenamiento")
    parser.add_argument("--batch", type=int, default=16, help="Tamaño de batch (16 ideal para RTX 4050)")
    parser.add_argument("--imgsz", type=int, default=640, help="Resolución de entrada de imágenes")
    parser.add_argument("--device", type=str, default="0" if torch.cuda.is_available() else "cpu", help="Dispositivo (0 para GPU CUDA)")
    parser.add_argument("--workers", type=int, default=4, help="Hilos para dataloader")
    parser.add_argument("--patience", type=int, default=20, help="Early stopping si no mejora")
    parser.add_argument("--name", type=str, default="yolo11s_detect_field_v1", help="Nombre del experimento")
    parser.add_argument("--model", type=str, default="yolo11s.pt",
                        help="Modelo inicial. Usar last.pt/best.pt para fine-tuning desde un checkpoint existente")
    args = parser.parse_args()

    from vitispray.paths import DETECT_FIELD_DATASET, YOLO_RUNS_DIR
    data_yaml = DETECT_FIELD_DATASET / "data.yaml"

    print("=" * 70)
    print("🚜 ENTRENAMIENTO YOLOv11s-DETECT (BOUNDING BOXES) - CAMPO MULTI-ORIGEN")
    print("=" * 70)
    print(f"* Configuración dataset: {data_yaml}")
    print(f"* GPU detectada:         {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    print(f"* Épocas configuradas:   {args.epochs}")
    print(f"* Batch size:            {args.batch}")
    print(f"* Resolución imgsz:      {args.imgsz}")
    print(f"* Nombre del run:        {args.name}")
    print("=" * 70)

    if not data_yaml.exists():
        print(f"❌ Error: No se encontró el archivo de datos en {data_yaml}")
        return

    # Cargar modelo (base o checkpoint para fine-tuning)
    model_path = args.model
    print(f"\n[>] Cargando modelo: {model_path}")
    model = YOLO(model_path)

    # Iniciar entrenamiento
    print("\n[>] Iniciando entrenamiento...")
    results = model.train(
        data=str(data_yaml),
        epochs=args.epochs,
        patience=args.patience,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        workers=args.workers,
        project=str(YOLO_RUNS_DIR / "detect"),
        name=args.name,
        exist_ok=True,
        plots=True,
        save=True,
        verbose=True
    )

    print("\n" + "=" * 70)
    print("✅ ENTRENAMIENTO DE DETECCIÓN FINALIZADO")
    print("=" * 70)
    save_dir = results.save_dir
    print(f"📁 Métricas y curvas guardadas en: {save_dir}")
    print(f"🏆 MEJOR MODELO PARA INFERENCIA:   {Path(save_dir) / 'weights' / 'best.pt'}")
    print(f"📊 ÚLTIMO MODELO:                  {Path(save_dir) / 'weights' / 'last.pt'}")
    print("=" * 70)

if __name__ == "__main__":
    main()
