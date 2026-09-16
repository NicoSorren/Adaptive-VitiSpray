"""
Script para preparar el dataset Mono-clase (exclusivo para Oídio - Powdery_Mildew).
Mantiene el dataset original 100% intacto y crea una estructura dedicada
usando enlaces de directorio (junctions) para no duplicar los 2.8 GB de imágenes.
"""

import os
import shutil
import subprocess
from pathlib import Path

def prepare_monoclass():
    base_dir = Path(__file__).resolve().parent
    orig_dir = base_dir / "Final Grape Leaf Disease Detection and Classification.v1i.yolov11"
    target_dir = base_dir / "dataset_monoclass_powdery_mildew"
    
    print("=" * 70)
    print("[*] CREANDO DATASET MONO-CLASE: POWDERY MILDEW (OIDIO)")
    print("=" * 70)
    print(f"* Dataset origen:  {orig_dir}")
    print(f"* Dataset destino: {target_dir}")
    print("=" * 70)
    
    if not orig_dir.exists():
        print(f"❌ Error: No se encontró el dataset original en {orig_dir}")
        return
        
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Mapeo: Clase 2 (Powdery_Mildew) -> Clase 0 (Powdery_Mildew)
    TARGET_CLASS_ID = 2
    NEW_CLASS_ID = 0
    
    stats = {}
    
    for split in ["train", "valid", "test"]:
        print(f"\n[>] Procesando split: '{split}'...")
        split_src = orig_dir / split
        split_dst = target_dir / split
        split_dst.mkdir(exist_ok=True)
        
        # 1. Crear hardlinks para images (0 bytes de duplicacion y resuelve ruta localmente)
        src_images = split_src / "images"
        dst_images = split_dst / "images"
        dst_images.mkdir(exist_ok=True)
        
        img_files = list(src_images.glob("*"))
        print(f"   -> Creando hardlinks de imagenes ({len(img_files)} archivos)...")
        for img in img_files:
            target_file = dst_images / img.name
            if not target_file.exists():
                try:
                    os.link(img, target_file)
                except FileExistsError:
                    pass
                except Exception as e:
                    shutil.copy2(img, target_file)
        
        # Eliminar cualquier cache viejo
        for cache in [split_dst / "labels.cache", split_dst / "labels.cache.npy"]:
            if cache.exists():
                cache.unlink()
        
        # 2. Procesar etiquetas (labels)
        src_labels = split_src / "labels"
        dst_labels = split_dst / "labels"
        dst_labels.mkdir(exist_ok=True)
        
        total_files = 0
        files_with_pm = 0
        total_pm_instances = 0
        empty_files = 0
        
        label_files = list(src_labels.glob("*.txt"))
        for lbl_file in label_files:
            total_files += 1
            pm_lines = []
            
            with open(lbl_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    cls_id = int(parts[0])
                    # Si es Powdery_Mildew (clase 2), la conservamos y remapeamos a 0
                    if cls_id == TARGET_CLASS_ID:
                        coords = " ".join(parts[1:])
                        pm_lines.append(f"{NEW_CLASS_ID} {coords}\n")
                        total_pm_instances += 1
            
            dst_file = dst_labels / lbl_file.name
            with open(dst_file, "w", encoding="utf-8") as f:
                f.writelines(pm_lines)
                
            if len(pm_lines) > 0:
                files_with_pm += 1
            else:
                empty_files += 1
                
        stats[split] = {
            "total_images": total_files,
            "images_with_pm": files_with_pm,
            "background_images": empty_files,
            "instances": total_pm_instances
        }
        print(f"   [+] {total_files} etiquetas procesadas:")
        print(f"      - Con Oidio: {files_with_pm}")
        print(f"      - Fondos/Negativos (sanas/otras): {empty_files}")
        print(f"      - Instancias de poligonos Oidio: {total_pm_instances}")
        
    # 3. Crear nuevo data.yaml mono-clase
    yaml_content = f"""# Dataset Mono-clase para Oidio de Vid (Powdery Mildew)
# Generado para el Proyecto Final de Estudios Adaptive-VitiSpray

path: {target_dir.as_posix()}
train: train/images
val: valid/images
test: test/images

nc: 1
names: ['Powdery_Mildew']
"""
    yaml_path = target_dir / "data.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
        
    print("\n" + "=" * 70)
    print("[+] DATASET MONO-CLASE CREADO CON EXITO")
    print("=" * 70)
    print(f"* Archivo de configuracion: {yaml_path}")
    print(f"* Clases: 1 ('Powdery_Mildew')")
    print(f"* Total instancias Oidio: {sum(s['instances'] for s in stats.values())}")
    print(f"* Total imagenes con Oidio: {sum(s['images_with_pm'] for s in stats.values())}")
    print(f"* Total imagenes negativas: {sum(s['background_images'] for s in stats.values())}")
    print("=" * 70)

if __name__ == "__main__":
    prepare_monoclass()
