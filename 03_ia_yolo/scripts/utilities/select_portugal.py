import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict
from sklearn.cluster import KMeans
import math
import builtins
import time

def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

def extract_date(filename):
    # IMG_20251014_100648.jpg
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

def select_images():
    base_dir = Path("02_datasets/publicos/candidatos/Portugal/resized/Powdery Mildew")
    out_dir = Path("00_gestion/dataset_candidates_audit/portugal_selected")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Due to glob duplicating on Windows when adding extensions, 
    # we just glob *.jpg (which matches .JPG too)
    images = list(base_dir.glob("*.jpg")) + list(base_dir.glob("*.png"))
    # ensure unique paths just in case
    images = list(set(images))
    print(f"Total unique images: {len(images)}")
    
    # 1. Group temporally
    date_groups = defaultdict(list)
    features_dict = {}
    
    for idx, img_p in enumerate(images):
        if idx % 100 == 0: print(f"Processing features {idx}/{len(images)}")
        date = extract_date(img_p.name)
        date_groups[date].append(img_p)
        
        img = cv2.imread(str(img_p))
        if img is None: continue
        
        # calculate features
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
    selected_images = []
    selection_details = []
    
    print("\n--- Selection by Date ---")
    for date, imgs in sorted(date_groups.items()):
        # Proportional allocation, min 1
        n_samples = max(1, int(round((len(imgs) / len(images)) * TARGET)))
        n_samples = min(n_samples, len(imgs))
        print(f"Date {date}: {len(imgs)} images -> selecting {n_samples}")
        
        if n_samples == len(imgs):
            selected = imgs
        else:
            # K-means clustering for diversity
            feats = np.array([features_dict[p] for p in imgs])
            # normalize
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
        
        selected_images.extend(selected)
        for p in selected:
            selection_details.append((p, date))
            
    print(f"\nTotal selected: {len(selected_images)}")
    
    # 4. Contact Sheets
    # 30 per sheet (e.g. 5 columns, 6 rows)
    sheet_idx = 1
    COLS = 5
    ROWS = 6
    PER_SHEET = COLS * ROWS
    
    for i in range(0, len(selected_images), PER_SHEET):
        batch = selection_details[i:i+PER_SHEET]
        panel_imgs = []
        for j, (img_p, date) in enumerate(batch):
            img = cv2.imread(str(img_p))
            img = cv2.resize(img, (256, 256))
            # canvas with text pad
            canvas = np.ones((310, 256, 3), dtype=np.uint8) * 255
            canvas[0:256, 0:256] = img
            
            text1 = f"Idx: {i+j+1}"
            text2 = img_p.name[:25]
            text3 = f"Date: {date}"
            cv2.putText(canvas, text1, (5, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
            cv2.putText(canvas, text2, (5, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
            cv2.putText(canvas, text3, (5, 305), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
            
            panel_imgs.append(canvas)
            
        while len(panel_imgs) < PER_SHEET:
            panel_imgs.append(np.ones((310, 256, 3), dtype=np.uint8) * 255)
            
        rows = []
        for r in range(ROWS):
            row_imgs = panel_imgs[r*COLS:(r+1)*COLS]
            rows.append(cv2.hconcat(row_imgs))
            
        sheet = cv2.vconcat(rows)
        cv2.imwrite(str(out_dir / f"selection_sheet_{sheet_idx:02d}.jpg"), sheet)
        sheet_idx += 1
        
    print("Contact sheets generated.")

if __name__ == "__main__":
    select_images()
