import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict
from sklearn.cluster import KMeans
import shutil
import csv
import builtins

def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

def extract_date(filename):
    parts = filename.replace('-', '_').split('_')
    if len(parts) > 1 and len(parts[1]) == 8:
        return parts[1]
    return "UNKNOWN"

def compute_entropy(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist.ravel() / hist.sum()
    logs = np.log2(hist + 1e-10)
    entropy = -np.sum(hist * logs)
    return entropy

def filter_selection():
    base_dir = Path("02_datasets/publicos/candidatos/Portugal/resized/Powdery Mildew")
    out_dir = Path("02_datasets/publicos/candidatos/Portugal/selected_for_annotation")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    images = list(base_dir.glob("*.jpg")) + list(base_dir.glob("*.png"))
    images = sorted(list(set(images))) # Added sorting for guaranteed deterministic behavior
    
    date_groups = defaultdict(list)
    features_dict = {}
    
    for idx, img_p in enumerate(images):
        date = extract_date(img_p.name)
        date_groups[date].append(img_p)
        
        img = cv2.imread(str(img_p))
        if img is None: continue
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))
        h, w = img.shape[:2]
        green_ratio = np.sum(green_mask > 0) / (w * h)
        
        entropy = compute_entropy(img)
        features_dict[img_p] = [brightness, contrast, green_ratio, entropy]
        
    TARGET = 300
    selection_details = []
    
    for date, imgs in sorted(date_groups.items()):
        n_samples = max(1, int(round((len(imgs) / len(images)) * TARGET)))
        n_samples = min(n_samples, len(imgs))
        
        if n_samples == len(imgs):
            selected = imgs
        else:
            feats = np.array([features_dict[p] for p in imgs])
            feats_norm = (feats - feats.mean(axis=0)) / (feats.std(axis=0) + 1e-6)
            
            kmeans = KMeans(n_clusters=n_samples, random_state=42).fit(feats_norm)
            selected = []
            for i in range(n_samples):
                cluster_points = np.where(kmeans.labels_ == i)[0]
                if len(cluster_points) > 0:
                    center = kmeans.cluster_centers_[i]
                    dists = np.linalg.norm(feats_norm[cluster_points] - center, axis=1)
                    closest = cluster_points[np.argmin(dists)]
                    selected.append(imgs[closest])
        
        for p in selected:
            selection_details.append((p, date))

    rejected_indices = {
        2, 3, 4, 7, 9, 10, 14, 15, 17, 19, 20, 23, 24, 25, 26, 28,
        38, 39, 40, 41, 45, 50, 51, 52, 55, 60, 61, 65, 71, 76, 81,
        84, 87, 90, 91, 92, 94, 96, 99, 104, 105, 111, 112, 114, 115,
        117, 118, 122, 123, 124, 126, 128, 132, 136, 139, 140, 141,
        146, 147, 148, 155, 160, 163, 164, 165, 171, 179, 182, 183,
        186, 191, 200, 203, 208, 212, 213, 216, 217, 222, 223, 225,
        227, 239, 240, 244, 247, 250, 260, 264, 265, 273, 277, 282,
        288
    }

    manifest_path = out_dir / "selected_for_annotation_manifest.csv"
    copied = 0
    
    with open(manifest_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'filename', 'fecha', 'source', 'status'])
        
        for i, (img_p, date) in enumerate(selection_details):
            idx = i + 1
            if idx not in rejected_indices:
                dst = out_dir / img_p.name
                shutil.copy2(img_p, dst)
                writer.writerow([idx, img_p.name, date, 'Portugal', 'selected_for_annotation'])
                copied += 1
                
    print(f"Total processed: {len(selection_details)}")
    print(f"Total rejected: {len(rejected_indices)}")
    print(f"Total copied for annotation: {copied}")
    if copied != 205:
        print("WARNING: Copied count does not match expected 205!")

if __name__ == "__main__":
    filter_selection()
