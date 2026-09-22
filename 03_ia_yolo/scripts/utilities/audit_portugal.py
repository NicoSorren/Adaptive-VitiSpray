import cv2
import numpy as np
import hashlib
from pathlib import Path
from PIL import Image
import imagehash
from sklearn.cluster import KMeans
import os
import builtins

def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

def compute_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compute_phash(img_path):
    try:
        img = Image.open(img_path)
        return imagehash.phash(img)
    except Exception as e:
        return None

def analyze_portugal(base_dir, out_dir):
    base_dir = Path(base_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    pm_dir = base_dir / "resized" / "Powdery Mildew"
    images = list(pm_dir.glob("*.jpg")) + list(pm_dir.glob("*.JPG")) + list(pm_dir.glob("*.png"))
    
    total_imgs = len(images)
    print(f"Total Powdery Mildew images: {total_imgs}")
    
    resolutions = []
    file_sizes = []
    
    features = []
    valid_images = []
    
    my_hashes = {}
    my_phashes = {}
    
    for idx, img_p in enumerate(images):
        if idx % 50 == 0:
            print(f"Analyzing {idx}/{total_imgs}")
        size_kb = img_p.stat().st_size / 1024.0
        file_sizes.append(size_kb)
        
        md5 = compute_md5(img_p)
        my_hashes[img_p] = md5
        ph = compute_phash(img_p)
        my_phashes[img_p] = ph
        
        img = cv2.imread(str(img_p))
        if img is None: continue
        h, w = img.shape[:2]
        resolutions.append((w, h))
        
        # Calculate visual features for diversity sampling
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))
        green_ratio = np.sum(green_mask > 0) / (w * h)
        
        features.append([brightness, contrast, green_ratio, w, h])
        valid_images.append(img_p)
        
    res_w = [r[0] for r in resolutions]
    res_h = [r[1] for r in resolutions]
    
    print("\n--- INVENTORY ---")
    print(f"Count: {total_imgs}")
    if res_w:
        print(f"Resolution min: {min(res_w)}x{min(res_h)}, max: {max(res_w)}x{max(res_h)}, median: {np.median(res_w)}x{np.median(res_h)}")
        from collections import Counter
        res_str = [f"{w}x{h}" for w, h in resolutions]
        mode_res = Counter(res_str).most_common(1)[0]
        print(f"Most frequent resolution: {mode_res[0]} ({mode_res[1]} images)")
    print(f"File size min: {min(file_sizes):.1f}KB, max: {max(file_sizes):.1f}KB, median: {np.median(file_sizes):.1f}KB")
    
    # 2. Diversity sampling
    features = np.array(features)
    # Normalize features
    features_norm = (features - features.mean(axis=0)) / (features.std(axis=0) + 1e-6)
    
    n_samples = min(100, len(valid_images))
    kmeans = KMeans(n_clusters=n_samples, random_state=42).fit(features_norm)
    
    sampled_indices = []
    for i in range(n_samples):
        cluster_points = np.where(kmeans.labels_ == i)[0]
        if len(cluster_points) > 0:
            center = kmeans.cluster_centers_[i]
            dists = np.linalg.norm(features_norm[cluster_points] - center, axis=1)
            closest = cluster_points[np.argmin(dists)]
            sampled_indices.append(closest)
            
    sampled_images = [valid_images[i] for i in sampled_indices]
    
    # 3. Contact Sheets
    sheet_idx = 1
    for i in range(0, len(sampled_images), 10):
        batch = sampled_images[i:i+10]
        panel_imgs = []
        for j, img_p in enumerate(batch):
            img = cv2.imread(str(img_p))
            img = cv2.resize(img, (256, 256))
            h, w = img.shape[:2]
            # add text padding
            canvas = np.ones((300, 256, 3), dtype=np.uint8) * 255
            canvas[0:256, 0:256] = img
            text1 = f"Idx: {i+j+1}"
            text2 = img_p.name[:25]
            text3 = f"Res: {resolutions[valid_images.index(img_p)][0]}x{resolutions[valid_images.index(img_p)][1]}"
            cv2.putText(canvas, text1, (5, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            cv2.putText(canvas, text2, (5, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            cv2.putText(canvas, text3, (5, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            panel_imgs.append(canvas)
            
        # pad if less than 10
        while len(panel_imgs) < 10:
            panel_imgs.append(np.ones((300, 256, 3), dtype=np.uint8) * 255)
            
        top_row = cv2.hconcat(panel_imgs[:5])
        bottom_row = cv2.hconcat(panel_imgs[5:])
        sheet = cv2.vconcat([top_row, bottom_row])
        cv2.imwrite(str(out_dir / f"contact_sheet_{sheet_idx:02d}.jpg"), sheet)
        sheet_idx += 1
        
    return my_hashes, my_phashes

def load_dataset_hashes(name, pattern, pbar_total=None):
    print(f"Hashing {name}...")
    md5s = set()
    phashes = set()
    images = list(Path('.').glob(pattern))
    for idx, img_p in enumerate(images):
        if pbar_total and idx % 200 == 0:
            print(f" {name}: {idx}/{len(images)}")
        md5s.add(compute_md5(img_p))
        ph = compute_phash(img_p)
        if ph is not None:
            phashes.add(ph)
    return md5s, phashes

if __name__ == "__main__":
    portugal_md5, portugal_phash = analyze_portugal(
        "02_datasets/publicos/candidatos/Portugal",
        "00_gestion/dataset_candidates_audit/portugal"
    )
    
    # 5. Duplicates against others
    field_md5, field_phash = load_dataset_hashes("detect_field", "02_datasets/procesados/dataset_detect_field/*/images/*.jpg", True)
    hermos_md5, hermos_phash = load_dataset_hashes("HERMOS", "02_datasets/publicos/candidatos/HERMOS/j4xs3kh3fd-2/Images/*.jpg", True)
    md_md5, md_phash = load_dataset_hashes("MD Nahid", "02_datasets/publicos/candidatos/Powdery Mildew.v1i.yolov11/*/images/*.jpg", True)
    
    def check_dups(name, ref_md5, ref_phash):
        exact = 0
        near = 0
        for md5 in portugal_md5.values():
            if md5 in ref_md5: exact += 1
        for ph1 in portugal_phash.values():
            if ph1 is None: continue
            for ph2 in ref_phash:
                if abs(ph1 - ph2) <= 3:
                    near += 1
                    break
        print(f"Portugal vs {name} -> Exact: {exact}, Near: {near}")
        
    print("\n--- DUPLICATES ---")
    check_dups("dataset_detect_field", field_md5, field_phash)
    check_dups("HERMOS", hermos_md5, hermos_phash)
    check_dups("MD Nahid", md_md5, md_phash)
