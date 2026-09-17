"""
Script de entrenamiento Baseline para Detección y Segmentación de Oídio en Vid
Modelo: YOLOv11s-seg (Ultralytics)
Hardware: NVIDIA GPU (CUDA)
"""

import sys
import argparse
from pathlib import Path
from ultralytics import YOLO
import torch

def parse_args():
    parser = argparse.ArgumentParser(description="Entrenar YOLOv11-seg para detección de enfermedades en vid")
    parser.add_argument("--model", type=str, default="yolo11s-seg.pt", help="Modelo base de Ultralytics (ej: yolo11n-seg.pt, yolo11s-seg.pt)")
    parser.add_argument("--data", type=str, default="dataset_monoclass_powdery_mildew/data.yaml", help="Ruta al archivo data.yaml del dataset")
    parser.add_argument("--epochs", type=int, default=50, help="Número máximo de épocas de entrenamiento")
    parser.add_argument("--patience", type=int, default=15, help="Early stopping: épocas sin mejora antes de detener")
    parser.add_argument("--batch", type=int, default=8, help="Tamaño del batch (8 es seguro para 6GB VRAM)")
    parser.add_argument("--imgsz", type=int, default=640, help="Resolución de imagen (640 estándar)")
    parser.add_argument("--name", type=str, default="monoclass_pm_v1", help="Nombre del experimento")
    parser.add_argument("--device", type=str, default="0", help="Dispositivo (0 para GPU CUDA, 'cpu' para CPU)")
    parser.add_argument("--workers", type=int, default=2, help="Hilos para dataloader en Windows")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 1. Rutas
    base_dir = Path(__file__).resolve().parent
    from vitispray.paths import MONOCLASS_DATASET
    dataset_yaml = MONOCLASS_DATASET / "data.yaml"
    
    print("=" * 70)
    print("ADAPTIVE-VITISPRAY - ENTRENAMIENTO DE PERCEPCION (YOLOv11-seg)")
    print("=" * 70)
    print(f"* Modelo inicial:       {args.model} (pesos preentrenados COCO)")
    print(f"* Dataset YAML:         {dataset_yaml}")
    print(f"* Epocas maximas:       {args.epochs} (Patience: {args.patience})")
    print(f"* Batch size:           {args.batch}")
    print(f"* Resolucion imagen:    {args.imgsz}x{args.imgsz}")
    print(f"* Dispositivo:          {args.device} (CUDA: {torch.cuda.is_available()})")
    if torch.cuda.is_available():
        print(f"* GPU detectada:        {torch.cuda.get_device_name(0)}")
        print(f"* VRAM disponible:      {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print("=" * 70)
    
    if not dataset_yaml.exists():
        print(f"❌ Error: No se encontró el dataset en {dataset_yaml}")
        sys.exit(1)
        
    # 2. Inicializar modelo YOLOv11-seg
    print(f"\n📦 Cargando pesos iniciales {args.model}...")
    model = YOLO(args.model)
    
    # 3. Entrenar
    print("\n🏋️ Iniciando ciclo de optimización...")
    results = model.train(
        data=str(dataset_yaml),
        epochs=args.epochs,
        patience=args.patience,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        workers=args.workers,
        project=str(base_dir / "runs" / "train"),
        name=args.name,
        exist_ok=True,
        plots=True,
        save=True,
        verbose=True
    )
    
    print("\n" + "=" * 70)
    print("✅ ENTRENAMIENTO FINALIZADO CON ÉXITO")
    print("=" * 70)
    save_dir = results.save_dir
    print(f"📁 Métricas y curvas guardadas en: {save_dir}")
    print(f"🏆 MEJOR MODELO PARA INFERENCIA:   {Path(save_dir) / 'weights' / 'best.pt'}")
    print(f"📊 ÚLTIMO MODELO (Checkpoit final): {Path(save_dir) / 'weights' / 'last.pt'}")
    print("=" * 70)

if __name__ == "__main__":
    main()
