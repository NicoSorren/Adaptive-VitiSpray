import os
import sys
import hashlib
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np

try:
    import imagehash
    from PIL import Image
    HAS_IMAGEHASH = True
except ImportError:
    HAS_IMAGEHASH = False

def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    from vitispray.paths import PROJECT_ROOT, DETECT_FIELD_DATASET, YOLO_RUNS_DIR, YOLO_DIR
    
    ext_dir = YOLO_DIR / "external_validation"
    if not ext_dir.exists():
        print(f"Error: {ext_dir} no existe.")
        sys.exit(1)
        
    ext_images = []
    for ext in [".jpg", ".jpeg", ".png"]:
        ext_images.extend(list(ext_dir.glob(f"*{ext}")))
        
    print(f"Encontradas {len(ext_images)} imagenes en external_validation.")
    
    # 1. Duplicates check
    print("\n--- Verificando duplicados ---")
    ext_hashes_md5 = {get_md5(p): p for p in ext_images}
    ext_hashes_phash = {}
    if HAS_IMAGEHASH:
        for p in ext_images:
            try:
                ext_hashes_phash[str(imagehash.phash(Image.open(p)))] = p
            except Exception:
                pass
                
    dataset_dir = DETECT_FIELD_DATASET
    duplicates_found = 0
    for split in ["train", "valid", "test"]:
        img_dir = dataset_dir / split / "images"
        if not img_dir.exists():
            continue
        for img_path in img_dir.glob("*.jpg"):
            md5 = get_md5(img_path)
            if md5 in ext_hashes_md5:
                print(f"DUPLICADO EXACTO: {ext_hashes_md5[md5].name} es igual a {img_path.name}")
                duplicates_found += 1
            elif HAS_IMAGEHASH:
                try:
                    phash = str(imagehash.phash(Image.open(img_path)))
                    for ext_ph, ext_p in ext_hashes_phash.items():
                        if imagehash.hex_to_hash(phash) - imagehash.hex_to_hash(ext_ph) < 3:
                            print(f"NEAR DUPLICATE: {ext_p.name} es similar a {img_path.name}")
                            duplicates_found += 1
                except Exception:
                    pass
    if duplicates_found == 0:
        print("Ningun duplicado encontrado.")
        
    # 2. Inference
    print("\n--- Ejecutando inferencias ---")
    model_path = YOLO_RUNS_DIR / "detect" / "yolo11m_detect_field_v1" / "weights" / "best.pt"
    if not model_path.exists():
        print(f"Error: No se encontro el modelo en {model_path}")
        sys.exit(1)
        
    model = YOLO(str(model_path))
    
    for conf in [0.25, 0.50, 0.70]:
        conf_dir = ext_dir / f"predictions_v2_conf{str(conf).replace('.', '')}"
        if str(conf) == '0.5':
            conf_dir = ext_dir / "predictions_v2_conf050"
        elif str(conf) == '0.7':
            conf_dir = ext_dir / "predictions_v2_conf070"
        conf_dir.mkdir(exist_ok=True, parents=True)
        print(f"Prediciendo a conf={conf}...")
        results = model.predict(source=[str(p) for p in ext_images], conf=conf, imgsz=640, verbose=False, save=False)
        for res, img_path in zip(results, ext_images):
            # Save plotted image
            res_img = res.plot(line_width=2)
            cv2.imwrite(str(conf_dir / img_path.name), res_img)
            
            # Text result
            boxes = res.boxes
            conf_str = "N/A"
            if len(boxes) > 0:
                conf_str = f"{float(boxes.conf.max()):.2f}"
            print(f"{img_path.name} @ conf={conf} -> {len(boxes)} boxes, max_conf={conf_str}")
            
if __name__ == "__main__":
    main()
