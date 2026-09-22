import cv2
import numpy as np
from pathlib import Path
import random

def polygon_area(xs, ys):
    return 0.5 * np.abs(np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1)))

def check_conversion():
    base_dir = Path("02_datasets/publicos/candidatos/Powdery Mildew.v1i.yolov11")
    out_dir = Path("00_gestion/dataset_candidates_audit/md_nahid_conversion_check")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Pick some specific images
    train_images = list((base_dir / "train" / "images").glob("*.jpg"))
    random.seed(42)
    sampled = random.sample(train_images, 5)
    
    for idx, img_p in enumerate(sampled):
        label_p = base_dir / "train" / "labels" / f"{img_p.stem}.txt"
        img = cv2.imread(str(img_p))
        if img is None: continue
        h, w = img.shape[:2]
        
        img_orig = img.copy()
        img_poly = img.copy()
        img_bbox = img.copy()
        img_super = img.copy()
        
        print(f"\nImage: {img_p.name} ({w}x{h})")
        with open(label_p, 'r') as f:
            lines = f.readlines()
            
        for obj_idx, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) < 5: continue
            
            coords = list(map(float, parts[1:]))
            xs = np.array(coords[0::2])
            ys = np.array(coords[1::2])
            
            # Original polygon points (scaled to img)
            pts_x = (xs * w).astype(np.int32)
            pts_y = (ys * h).astype(np.int32)
            pts = np.vstack((pts_x, pts_y)).T.reshape((-1, 1, 2))
            
            cv2.polylines(img_poly, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.polylines(img_super, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            
            # Correct Bbox calc (min/max)
            min_x, max_x = xs.min(), xs.max()
            min_y, max_y = ys.min(), ys.max()
            
            bx1, bx2 = int(min_x * w), int(max_x * w)
            by1, by2 = int(min_y * h), int(max_y * h)
            
            cv2.rectangle(img_bbox, (bx1, by1), (bx2, by2), (0, 0, 255), 2)
            cv2.rectangle(img_super, (bx1, by1), (bx2, by2), (0, 0, 255), 2)
            
            poly_rel_area = polygon_area(xs, ys)
            bbox_rel_area = (max_x - min_x) * (max_y - min_y)
            
            print(f"  Obj {obj_idx+1}:")
            # print first 100 chars of line
            print(f"    Line start: {line[:100]}...")
            print(f"    Num coords: {len(coords)} ({len(xs)} points)")
            print(f"    min_x: {min_x:.4f}, max_x: {max_x:.4f}")
            print(f"    min_y: {min_y:.4f}, max_y: {max_y:.4f}")
            print(f"    Bbox width: {max_x - min_x:.4f}, height: {max_y - min_y:.4f}")
            print(f"    Polygon rel area: {poly_rel_area:.4f}")
            print(f"    Bbox rel area:    {bbox_rel_area:.4f}")
            
        panel = cv2.hconcat([
            cv2.resize(img_orig, (400, 400)), 
            cv2.resize(img_poly, (400, 400)),
            cv2.resize(img_bbox, (400, 400)),
            cv2.resize(img_super, (400, 400))
        ])
        cv2.imwrite(str(out_dir / f"check_{img_p.stem}.jpg"), panel)

if __name__ == "__main__":
    check_conversion()
