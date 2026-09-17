import sys
import os
import glob
import random
import cv2
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

random.seed(42)

from vitispray.paths import DETECT_FIELD_DATASET, PROJECT_ROOT
DATASET_DIR = DETECT_FIELD_DATASET
OUT_DIR = PROJECT_ROOT / "inspeccion_dataset_detect"
OUT_DIR.mkdir(exist_ok=True)

for split in ["train", "valid"]:
    img_dir = DATASET_DIR / split / "images"
    lbl_dir = DATASET_DIR / split / "labels"
    
    # Encontrar archivos con al menos 1 caja
    italy_imgs = []
    base_imgs = []
    
    for lbl_file in lbl_dir.glob("*.txt"):
        with open(lbl_file, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
        if not lines:
            continue
            
        stem = lbl_file.stem
        candidates = list(img_dir.glob(f"{stem}.*"))
        if not candidates:
            continue
            
        img_candidate = candidates[0]
        if img_candidate.name.startswith("italy_"):
            italy_imgs.append((img_candidate, lbl_file))
        else:
            base_imgs.append((img_candidate, lbl_file))
            
    selected = random.sample(italy_imgs, min(3, len(italy_imgs))) + random.sample(base_imgs, min(3, len(base_imgs)))
    
    for img_file, lbl_file in selected:
        img = cv2.imread(str(img_file))
        if img is None:
            continue
        h, w = img.shape[:2]
        
        with open(lbl_file, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
            
        box_count = 0
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                cls_id = int(parts[0])
                xc, yc, bw, bh = map(float, parts[1:5])
                
                xmin = int((xc - bw / 2.0) * w)
                ymin = int((yc - bh / 2.0) * h)
                xmax = int((xc + bw / 2.0) * w)
                ymax = int((yc + bh / 2.0) * h)
                
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 3)
                cv2.putText(img, "Powdery_Mildew", (xmin, max(25, ymin - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                box_count += 1
                
        # Resize para visualización liviana
        max_dim = 1200
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))
            
        out_name = f"check_{split}_{img_file.name[:25]}.jpg"
        cv2.imwrite(str(OUT_DIR / out_name), img)
        print(f"[{split.upper()}] Guardada muestra: {out_name} ({box_count} cajas)")

print(f"\nMuestras de verificación generadas en: {OUT_DIR}")
