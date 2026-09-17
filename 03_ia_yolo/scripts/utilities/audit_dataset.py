import os
import cv2
import numpy as np
import glob
from collections import defaultdict

def dhash(image, hash_size=8):
    # Convert to grayscale and resize to (hash_size + 1) x hash_size
    resized = cv2.resize(image, (hash_size + 1, hash_size), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # Calculate differences between adjacent pixels
    diff = gray[:, 1:] > gray[:, :-1]
    # Convert boolean array to a single 64-bit integer hash
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hamming_distance(h1, h2):
    # XOR the two hashes and count the number of 1s (set bits)
    return bin(h1 ^ h2).count('1')

def main():
    base_dir = "02_datasets/procesados/dataset_detect_field"
    splits = ["train", "valid", "test"]
    
    stats = {
        "train": {"A": 0, "B": 0, "pos": 0, "neg": 0, "boxes": 0, "box_areas": [], "box_counts": []},
        "valid": {"A": 0, "B": 0, "pos": 0, "neg": 0, "boxes": 0, "box_areas": [], "box_counts": []},
        "test": {"A": 0, "B": 0, "pos": 0, "neg": 0, "boxes": 0, "box_areas": [], "box_counts": []}
    }
    
    # We only care about Italy for data leakage
    italy_hashes = {"train": [], "valid": []}
    
    for split in splits:
        img_dir = os.path.join(base_dir, split, "images")
        lbl_dir = os.path.join(base_dir, split, "labels")
        
        if not os.path.exists(img_dir): continue
        
        images = glob.glob(os.path.join(img_dir, "*.*"))
        for img_path in images:
            filename = os.path.basename(img_path)
            is_italy = filename.startswith("italy_")
            
            if is_italy:
                stats[split]["B"] += 1
            else:
                stats[split]["A"] += 1
                
            # Labels
            stem = os.path.splitext(filename)[0]
            lbl_path = os.path.join(lbl_dir, stem + ".txt")
            
            has_label = False
            boxes_in_img = 0
            if os.path.exists(lbl_path):
                with open(lbl_path, "r") as f:
                    lines = [l.strip() for l in f if l.strip()]
                if lines:
                    has_label = True
                    for l in lines:
                        parts = list(map(float, l.split()))
                        if len(parts) >= 5:
                            w, h = parts[3], parts[4]
                            area = w * h
                            stats[split]["box_areas"].append(area)
                            boxes_in_img += 1
            
            if has_label:
                stats[split]["pos"] += 1
                stats[split]["boxes"] += boxes_in_img
                stats[split]["box_counts"].append(boxes_in_img)
            else:
                stats[split]["neg"] += 1
                stats[split]["box_counts"].append(0)
                
            # Hashing for Italy images (leakage analysis)
            if is_italy and split in ["train", "valid"]:
                img = cv2.imread(img_path)
                if img is not None:
                    h = dhash(img)
                    italy_hashes[split].append((filename, h))

    # Print Report
    print("=== COMPOSICIÓN POR FUENTE Y SPLIT ===")
    for split in splits:
        print(f"[{split.upper()}] A (Roboflow): {stats[split]['A']} | B (Italia): {stats[split]['B']}")
        print(f"         Positivas: {stats[split]['pos']} | Negativas (Background): {stats[split]['neg']}")
        
    print("\n=== DISTRIBUCIÓN DE ANOTACIONES ===")
    for split in splits:
        print(f"[{split.upper()}]")
        print(f"  Total BBoxes: {stats[split]['boxes']}")
        if stats[split]['box_counts']:
            arr = np.array(stats[split]['box_counts'])
            print(f"  BBoxes por img -> Promedio: {np.mean(arr):.2f} | Mediana: {np.median(arr)} | Max: {np.max(arr)}")
        if stats[split]['box_areas']:
            areas = np.array(stats[split]['box_areas'])
            print(f"  Área Relativa -> Mediana: {np.median(areas)*100:.2f}% | P25: {np.percentile(areas, 25)*100:.2f}% | P75: {np.percentile(areas, 75)*100:.2f}%")
            small = np.sum(areas < 0.05) / len(areas)
            print(f"  Pequeñas (<5% área): {small*100:.2f}%")

    print("\n=== DATA LEAKAGE EN ITALIA (NEAR-DUPLICATES TRAIN vs VALID) ===")
    exact_dups = 0
    near_dups = 0
    
    # Comparar train vs valid
    for train_file, train_h in italy_hashes["train"]:
        for val_file, val_h in italy_hashes["valid"]:
            dist = hamming_distance(train_h, val_h)
            if dist == 0:
                exact_dups += 1
                if exact_dups <= 5:
                    print(f"  [EXACT] {train_file} == {val_file}")
            elif dist <= 4:
                near_dups += 1
                if near_dups <= 5:
                    print(f"  [NEAR] {train_file} ~= {val_file} (dist: {dist})")
                    
    total_val_italy = len(italy_hashes["valid"])
    if total_val_italy > 0:
        leakage = ((exact_dups + near_dups) / total_val_italy) * 100
        print(f"\n  Duplicados Exactos: {exact_dups}")
        print(f"  Near Duplicates (Dist <= 4): {near_dups}")
        print(f"  Leakage Estimado sobre Valid Italia: {leakage:.2f}%")

if __name__ == "__main__":
    main()
