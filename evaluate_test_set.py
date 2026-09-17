import sys
from pathlib import Path
import random
import cv2
import torch
from ultralytics import YOLO

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    from vitispray.paths import DETECT_FIELD_DATASET, PROJECT_ROOT
    model_path = PROJECT_ROOT / "runs" / "detect" / "yolo11m_detect_field_v1" / "weights" / "best.pt"
    data_yaml = DETECT_FIELD_DATASET / "data.yaml"
    out_dir = PROJECT_ROOT / "test_visual_predictions_m1"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("🔬 EVALUACIÓN INDEPENDIENTE EN TEST SET - YOLOv11m DETECT (MEDIUM)")
    print("=" * 70)
    print(f"* Modelo: {model_path}")
    print(f"* Dataset: {data_yaml}")
    print("=" * 70)

    model = YOLO(str(model_path))

    # 1. Evaluación formal en split de test
    print("\n[1/2] Calculando métricas formales sobre test set (1.458 imágenes)...")
    metrics = model.val(
        data=str(data_yaml),
        split="test",
        batch=16,
        imgsz=640,
        device="0" if torch.cuda.is_available() else "cpu",
        project=str(base_dir / "runs" / "detect"),
        name="test_evaluation_m1",
        exist_ok=True,
        save_json=False,
        plots=True
    )

    print("\n" + "=" * 70)
    print("📊 RESULTADOS EN CONJUNTO DE TEST INDEPENDIENTE:")
    print("=" * 70)
    p = metrics.box.p[0] * 100 if len(metrics.box.p) > 0 else 0
    r = metrics.box.r[0] * 100 if len(metrics.box.r) > 0 else 0
    map50 = metrics.box.map50 * 100
    map5095 = metrics.box.map * 100
    print(f"  Precision: {p:.2f}%")
    print(f"  Recall:    {r:.2f}%")
    print(f"  mAP@0.50:  {map50:.2f}%")
    print(f"  mAP@50-95: {map5095:.2f}%")
    print("=" * 70)

    # 2. Generar muestras visuales con predicciones en alta resolución
    print("\n[2/2] Generando predicciones visuales en imágenes de test...")
    test_img_dir = DETECT_FIELD_DATASET / "test" / "images"
    test_lbl_dir = DETECT_FIELD_DATASET / "test" / "labels"
    
    # Buscar imágenes que tengan oídio anotado y algunas sin anotar
    with_disease = []
    without_disease = []
    for img_p in test_img_dir.glob("*.jpg"):
        lbl_p = test_lbl_dir / f"{img_p.stem}.txt"
        if lbl_p.exists() and lbl_p.stat().st_size > 0:
            with_disease.append(img_p)
        else:
            without_disease.append(img_p)

    random.seed(42)
    sample_sick = random.sample(with_disease, min(12, len(with_disease)))
    sample_healthy = random.sample(without_disease, min(4, len(without_disease)))
    selected = sample_sick + sample_healthy
    random.shuffle(selected)

    print(f"Procesando {len(selected)} imágenes de muestra con cajas de predicción...")
    for i, img_path in enumerate(selected, 1):
        res = model.predict(str(img_path), conf=0.25, imgsz=640, device="0" if torch.cuda.is_available() else "cpu", verbose=False)[0]
        plotted = res.plot(line_width=2, font_size=1)
        save_name = f"test_pred_{i:02d}_{img_path.name}"
        cv2.imwrite(str(out_dir / save_name), plotted)

    print(f"✅ Muestras visuales guardadas en: {out_dir}")

if __name__ == "__main__":
    main()
