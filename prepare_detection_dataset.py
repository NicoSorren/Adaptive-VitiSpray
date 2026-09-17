"""
Script de preparación del dataset unificado para YOLOv11-detect (Bounding Boxes) a Campo.
1. Convierte las anotaciones poligonales del dataset base a Bounding Boxes estándar de YOLO (0 xc yc w h).
2. Extrae las imágenes de campo del dataset italiano (Cerdeña 2021/2022), descartando estrictamente viveros y plantines en macetas.
3. Filtra la clase Powdery_Mildew como Clase 0 y mantiene el resto como negativos de fondo.
4. Genera dataset_detect_field/ con estructura train/valid/test y data.yaml.
"""

import sys
import os
import zipfile
import random
import numpy as np
from pathlib import Path

# Configurar stdout en utf-8 para Windows PowerShell
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Fijar semilla para reproducibilidad exacta
random.seed(42)

from vitispray.paths import PROJECT_ROOT, PUBLIC_DATASETS_DIR, DETECT_FIELD_DATASET

ORIG_BASE_DIR = PUBLIC_DATASETS_DIR / "Final Grape Leaf Disease Detection and Classification.v1i.yolov11"
ITALY_DIR = PUBLIC_DATASETS_DIR / "Downy Mildew and Powdery Mildew Symptoms"
TARGET_DIR = DETECT_FIELD_DATASET

# Palabras clave de carpetas a DESCARTAR (viveros, macetas, plantines)
DISCARD_KEYWORDS = ["piantine", "vaso"]

def is_discarded(folder_name):
    f_lower = folder_name.lower()
    return any(kw in f_lower for kw in DISCARD_KEYWORDS)

def polygon_to_bbox(coords):
    """Convierte lista de puntos [x1, y1, x2, y2, ...] a (xc, yc, w, h) normalizados."""
    pts = np.array(coords).reshape(-1, 2)
    xmin = np.min(pts[:, 0])
    xmax = np.max(pts[:, 0])
    ymin = np.min(pts[:, 1])
    ymax = np.max(pts[:, 1])
    
    # Asegurar límites [0, 1]
    xmin = max(0.0, min(1.0, float(xmin)))
    xmax = max(0.0, min(1.0, float(xmax)))
    ymin = max(0.0, min(1.0, float(ymin)))
    ymax = max(0.0, min(1.0, float(ymax)))
    
    w = max(0.001, xmax - xmin)
    h = max(0.001, ymax - ymin)
    xc = xmin + w / 2.0
    yc = ymin + h / 2.0
    return xc, yc, w, h

def prepare_dataset():
    print("=" * 70)
    print("🚀 PREPARANDO DATASET MULTI-ORIGEN A CAMPO (YOLOv11-DETECT)")
    print("=" * 70)
    print(f"Destino: {TARGET_DIR}")
    
    for split in ["train", "valid", "test"]:
        (TARGET_DIR / split / "images").mkdir(parents=True, exist_ok=True)
        (TARGET_DIR / split / "labels").mkdir(parents=True, exist_ok=True)
        
    stats = {
        "base": {"train": 0, "valid": 0, "test": 0, "pm_boxes": 0},
        "italy_field": {"train": 0, "valid": 0, "pm_boxes": 0, "discarded_images": 0}
    }
    
    # -------------------------------------------------------------
    # 1. PROCESAR DATASET BASE (ROBOFLOW)
    # -------------------------------------------------------------
    print("\n[1/3] Procesando dataset base (conversión de polígonos a cajas)...")
    for split in ["train", "valid", "test"]:
        img_src_dir = ORIG_BASE_DIR / split / "images"
        lbl_src_dir = ORIG_BASE_DIR / split / "labels"
        
        img_dst_dir = TARGET_DIR / split / "images"
        lbl_dst_dir = TARGET_DIR / split / "labels"
        
        lbl_files = list(lbl_src_dir.glob("*.txt"))
        print(f"  -> Split '{split}': {len(lbl_files)} archivos...", flush=True)
        
        # Pre-indexar imágenes para búsqueda instantánea O(1)
        image_map = {f.stem: f for f in img_src_dir.iterdir() if f.is_file()}
        
        for lbl_file in lbl_files:
            base_stem = lbl_file.stem
            img_file = image_map.get(base_stem)
            if not img_file:
                continue
            dst_img = img_dst_dir / img_file.name
            
            # Hardlink de imagen
            if not dst_img.exists():
                try:
                    os.link(img_file, dst_img)
                except Exception:
                    import shutil
                    shutil.copy2(img_file, dst_img)
                    
            # Procesar etiquetas
            with open(lbl_file, "r") as f:
                lines = [l.strip() for l in f if l.strip()]
                
            out_lines = []
            for l in lines:
                parts = l.split()
                cls_id = int(parts[0])
                coords = [float(p) for p in parts[1:]]
                
                # Clase 2 en original es Powdery_Mildew -> pasa a Clase 0
                if cls_id == 2 and len(coords) >= 4:
                    xc, yc, w, h = polygon_to_bbox(coords)
                    out_lines.append(f"0 {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
                    stats["base"]["pm_boxes"] += 1
                    
            # Guardar archivo de etiquetas (si está vacío, cuenta como fondo negativo)
            dst_lbl = lbl_dst_dir / f"{base_stem}.txt"
            with open(dst_lbl, "w") as f:
                f.writelines(out_lines)
                
            stats["base"][split] += 1

    # -------------------------------------------------------------
    # 2. PROCESAR DATASET ITALIA (GHIANI ET AL.) - FILTRANDO VIVEROS
    # -------------------------------------------------------------
    print("\n[2/3] Procesando dataset de Cerdeña (Italia) - Curaduría estricta de campo...")
    
    zip_pairs = [
        (
            ITALY_DIR / "Dataset 2021" / "powdery_downy_mildew_2021.zip",
            ITALY_DIR / "Dataset 2021" / "annot_powdery_downy_mildew_2021.zip",
            "2021",
            "annot_2021"
        ),
        (
            ITALY_DIR / "Dataset 2022" / "powdery_downy_mildew_2022.zip",
            ITALY_DIR / "Dataset 2022" / "annot_powdery_downy_mildew_2022.zip",
            "2022",
            "annot_2022"
        )
    ]
    
    field_entries = [] # lista de (zip_img, zip_annot, img_path_in_zip, annot_path_in_zip, year)
    
    for z_img_path, z_annot_path, year, annot_root in zip_pairs:
        if not z_img_path.exists() or not z_annot_path.exists():
            print(f"⚠️ Archivo zip no encontrado: {z_img_path}")
            continue
            
        with zipfile.ZipFile(z_img_path, "r") as zi, zipfile.ZipFile(z_annot_path, "r") as za:
            annot_set = set(za.namelist())
            for img_name in zi.namelist():
                if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                
                parts = img_name.split("/")
                folder_name = parts[0]
                
                # Chequeo de exclusión de vivero / macetas
                if is_discarded(folder_name):
                    stats["italy_field"]["discarded_images"] += 1
                    continue
                    
                # Encontrar anotación correspondiente
                # 2021: annot_2021/Folder/file.txt
                # 2022: annot_2022/Folder/file.txt
                annot_candidate = f"{annot_root}/{img_name}"
                annot_txt = os.path.splitext(annot_candidate)[0] + ".txt"
                
                if annot_txt in annot_set:
                    field_entries.append((z_img_path, z_annot_path, img_name, annot_txt, year))
                    
    print(f"  -> Total de imágenes de campo identificadas: {len(field_entries)}")
    print(f"  -> Imágenes de vivero/macetas descartadas:   {stats['italy_field']['discarded_images']}")
    
    # Barajar para partición aleatoria 80% Train, 20% Valid
    random.shuffle(field_entries)
    n_train = int(len(field_entries) * 0.8)
    train_entries = field_entries[:n_train]
    val_entries = field_entries[n_train:]
    
    for entries, split in [(train_entries, "train"), (val_entries, "valid")]:
        img_dst_dir = TARGET_DIR / split / "images"
        lbl_dst_dir = TARGET_DIR / split / "labels"
        
        for z_img_path, z_annot_path, img_name, annot_txt, year in entries:
            clean_stem = f"italy_{year}_" + Path(img_name).name.replace(" ", "_")
            stem_no_ext = Path(clean_stem).stem
            
            # Extraer imagen
            with zipfile.ZipFile(z_img_path, "r") as zi:
                img_data = zi.read(img_name)
                ext = Path(img_name).suffix.lower() or ".jpg"
                out_img_path = img_dst_dir / f"{stem_no_ext}{ext}"
                with open(out_img_path, "wb") as f:
                    f.write(img_data)
                    
            # Extraer y mapear etiquetas
            with zipfile.ZipFile(z_annot_path, "r") as za:
                lbl_data = za.read(annot_txt).decode("utf-8", errors="ignore")
                
            out_lines = []
            for line in lbl_data.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 5:
                    cls_id = int(parts[0])
                    # En Italia: Clase 0 = Oidio (Powdery Mildew)
                    if cls_id == 0:
                        xc, yc, w, h = parts[1:5]
                        out_lines.append(f"0 {xc} {yc} {w} {h}\n")
                        stats["italy_field"]["pm_boxes"] += 1
                        
            out_lbl_path = lbl_dst_dir / f"{stem_no_ext}.txt"
            with open(out_lbl_path, "w") as f:
                f.writelines(out_lines)
                
            stats["italy_field"][split] += 1
            
    # -------------------------------------------------------------
    # 3. CREAR ARCHIVO data.yaml
    # -------------------------------------------------------------
    print("\n[3/3] Generando archivo de configuración data.yaml...")
    yaml_content = f"""# Configuración de Dataset para Detección a Campo (YOLOv11-detect)
path: {TARGET_DIR.as_posix()}
train: train/images
val: valid/images
test: test/images

nc: 1
names: ['Powdery_Mildew']
"""
    with open(TARGET_DIR / "data.yaml", "w") as f:
        f.write(yaml_content)
        
    print("\n" + "=" * 70)
    print("✅ DATASET UNIFICADO PREPARADO EXITOSAMENTE")
    print("=" * 70)
    print(f"Total imágenes Train: {stats['base']['train'] + stats['italy_field']['train']} (Base: {stats['base']['train']} | Italia Campo: {stats['italy_field']['train']})")
    print(f"Total imágenes Valid: {stats['base']['valid'] + stats['italy_field']['valid']} (Base: {stats['base']['valid']} | Italia Campo: {stats['italy_field']['valid']})")
    print(f"Total imágenes Test:  {stats['base']['test']} (Base intacto)")
    print(f"Total cajas de Oídio: {stats['base']['pm_boxes'] + stats['italy_field']['pm_boxes']} cajas")
    print(f"Imágenes de vivero/macetas descartadas: {stats['italy_field']['discarded_images']}")
    print(f"Configuración guardada en: {TARGET_DIR / 'data.yaml'}")
    print("=" * 70)

if __name__ == "__main__":
    prepare_dataset()
