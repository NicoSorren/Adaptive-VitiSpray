import os
from pathlib import Path
import xml.etree.ElementTree as ET
import cv2
import numpy as np
import hashlib
from PIL import Image
import imagehash
import random
import yaml
from collections import defaultdict

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
        print(f"Error computing phash for {img_path}: {e}")
        return None

def analyze_md_nahid(base_dir, out_panels_dir, detect_field_hashes):
    print("=== Analyzing MD Nahid ===")
    base_dir = Path(base_dir)
    out_panels_dir = Path(out_panels_dir)
    out_panels_dir.mkdir(parents=True, exist_ok=True)
    
    yaml_file = base_dir / "data.yaml"
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    classes = data['names']
    print(f"Classes: {classes}")
    
    total_imgs = 0
    pos_imgs = 0
    neg_imgs = 0
    bboxes_per_img = []
    rel_areas = []
    resolutions = []
    
    splits = ['train', 'valid', 'test']
    images_to_sample = []
    
    my_hashes = {}
    my_phashes = {}
    exact_dups = 0
    near_dups = 0
    
    for split in splits:
        split_dir = base_dir / split / "images"
        if not split_dir.exists():
            continue
        
        for img_p in split_dir.glob("*.jpg"):
            total_imgs += 1
            
            # Read image for resolution
            img = cv2.imread(str(img_p))
            if img is None:
                continue
            h, w = img.shape[:2]
            resolutions.append((w, h))
            img_area = w * h
            
            # Check duplicates
            md5 = compute_md5(img_p)
            my_hashes[md5] = img_p
            if md5 in detect_field_hashes['md5']:
                exact_dups += 1
                
            ph = compute_phash(img_p)
            if ph is not None:
                my_phashes[img_p] = ph
                for ref_ph in detect_field_hashes['phash'].values():
                    if abs(ph - ref_ph) <= 3:
                        near_dups += 1
                        break
            
            # Read label
            label_p = base_dir / split / "labels" / f"{img_p.stem}.txt"
            is_pos = False
            boxes = 0
            if label_p.exists():
                with open(label_p, 'r') as f:
                    lines = f.readlines()
                if len(lines) > 0:
                    is_pos = True
                    pos_imgs += 1
                    boxes = len(lines)
                    bboxes_per_img.append(boxes)
                    
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) >= 5: # bounding box
                            _, _, _, bw, bh = map(float, parts[:5])
                            rel_area = (bw * bh) # YOLO format is relative width/height
                            rel_areas.append(rel_area)
            if not is_pos:
                neg_imgs += 1
                bboxes_per_img.append(0)
            
            if is_pos:
                images_to_sample.append((img_p, label_p))
                
    res_w = [r[0] for r in resolutions]
    res_h = [r[1] for r in resolutions]
    
    print(f"Total imgs: {total_imgs}, Pos: {pos_imgs}, Neg: {neg_imgs}")
    if res_w:
        print(f"Min res: {min(res_w)}x{min(res_h)}, Max res: {max(res_w)}x{max(res_h)}, Median: {np.median(res_w)}x{np.median(res_h)}")
    
    if rel_areas:
        rel_areas = np.array(rel_areas)
        print(f"Median relative area: {np.median(rel_areas):.4f}")
        print(f"p25: {np.percentile(rel_areas, 25):.4f}, p75: {np.percentile(rel_areas, 75):.4f}")
        print(f"Range: {np.min(rel_areas):.4f} - {np.max(rel_areas):.4f}")
        print(f">40%: {np.mean(rel_areas > 0.40) * 100:.2f}%")
        
    print(f"Bboxes per img (all): Mean {np.mean(bboxes_per_img):.2f}, Median {np.median(bboxes_per_img):.2f}")
    print(f"Exact dups vs field: {exact_dups}, Near dups: {near_dups}")
    
    # Generate 25 panels
    sampled = random.sample(images_to_sample, min(25, len(images_to_sample)))
    for idx, (img_p, label_p) in enumerate(sampled):
        img = cv2.imread(str(img_p))
        gt_img = img.copy()
        h, w = img.shape[:2]
        with open(label_p, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) >= 5:
                    _, cx, cy, bw, bh = map(float, parts[:5])
                    x1 = int((cx - bw/2) * w)
                    y1 = int((cy - bh/2) * h)
                    x2 = int((cx + bw/2) * w)
                    y2 = int((cy + bh/2) * h)
                    cv2.rectangle(gt_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        panel = cv2.hconcat([cv2.resize(img, (640, 640)), cv2.resize(gt_img, (640, 640))])
        cv2.imwrite(str(out_panels_dir / f"sample_{idx}.jpg"), panel)
        
    return my_hashes, my_phashes

def analyze_hermos(base_dir, out_panels_dir, detect_field_hashes):
    print("\n=== Analyzing HERMOS ===")
    base_dir = Path(base_dir)
    out_panels_dir = Path(out_panels_dir)
    out_panels_dir.mkdir(parents=True, exist_ok=True)
    
    img_dir = base_dir / "j4xs3kh3fd-2" / "Images"
    
    total_imgs = 0
    pos_imgs = 0
    neg_imgs = 0
    bboxes_per_img = []
    rel_areas = []
    resolutions = []
    
    class_names = set()
    
    images_to_sample = []
    
    my_hashes = {}
    my_phashes = {}
    exact_dups = 0
    near_dups = 0
    
    images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.JPG"))
    for idx, img_p in enumerate(images):
        if idx % 50 == 0:
            print(f"HERMOS: Processed {idx}/{len(images)} images")
        total_imgs += 1
        
        xml_p = img_p.with_suffix('.xml')
        is_pos = False
        boxes = 0
        img_boxes = []
        
        # We need to read image if we want to hash it or know resolution
        # Let's read resolution from XML if available
        if xml_p.exists():
            tree = ET.parse(xml_p)
            root = tree.getroot()
            
            size_elem = root.find('size')
            w = int(size_elem.find('width').text)
            h = int(size_elem.find('height').text)
            resolutions.append((w, h))
            img_area = w * h
            
            for obj in root.findall('object'):
                name = obj.find('name').text.lower()
                class_names.add(name)
                if name == 'powdery mildew':
                    is_pos = True
                    boxes += 1
                    bndbox = obj.find('bndbox')
                    xmin = int(bndbox.find('xmin').text)
                    ymin = int(bndbox.find('ymin').text)
                    xmax = int(bndbox.find('xmax').text)
                    ymax = int(bndbox.find('ymax').text)
                    bw = xmax - xmin
                    bh = ymax - ymin
                    rel_areas.append((bw * bh) / img_area)
                    img_boxes.append((xmin, ymin, xmax, ymax))
        
        if is_pos:
            pos_imgs += 1
            bboxes_per_img.append(boxes)
            images_to_sample.append((img_p, img_boxes))
        else:
            neg_imgs += 1
            bboxes_per_img.append(0)
            
        md5 = compute_md5(img_p)
        my_hashes[md5] = img_p
        if md5 in detect_field_hashes['md5']:
            exact_dups += 1
            
        ph = compute_phash(img_p)
        if ph is not None:
            my_phashes[img_p] = ph
            for ref_ph in detect_field_hashes['phash'].values():
                if abs(ph - ref_ph) <= 3:
                    near_dups += 1
                    break

    res_w = [r[0] for r in resolutions]
    res_h = [r[1] for r in resolutions]
    
    print(f"Total imgs: {total_imgs}, Pos (powdery mildew): {pos_imgs}, Neg: {neg_imgs}")
    if res_w:
        print(f"Min res: {min(res_w)}x{min(res_h)}, Max res: {max(res_w)}x{max(res_h)}, Median: {np.median(res_w)}x{np.median(res_h)}")
    print(f"Classes found: {class_names}")
    
    if rel_areas:
        rel_areas = np.array(rel_areas)
        print(f"Median relative area: {np.median(rel_areas):.4f}")
        print(f"p25: {np.percentile(rel_areas, 25):.4f}, p75: {np.percentile(rel_areas, 75):.4f}")
        print(f"Range: {np.min(rel_areas):.4f} - {np.max(rel_areas):.4f}")
        print(f">40%: {np.mean(rel_areas > 0.40) * 100:.2f}%")
        
    print(f"Bboxes per img (all): Mean {np.mean(bboxes_per_img):.2f}, Median {np.median(bboxes_per_img):.2f}")
    print(f"Exact dups vs field: {exact_dups}, Near dups: {near_dups}")
    
    sampled = random.sample(images_to_sample, min(25, len(images_to_sample)))
    for idx, (img_p, boxes) in enumerate(sampled):
        img = cv2.imread(str(img_p))
        if img is None: continue
        gt_img = img.copy()
        for box in boxes:
            cv2.rectangle(gt_img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 3)
        panel = cv2.hconcat([cv2.resize(img, (800, 800)), cv2.resize(gt_img, (800, 800))])
        cv2.imwrite(str(out_panels_dir / f"sample_{idx}.jpg"), panel)
        
    return my_hashes, my_phashes

def load_detect_field_hashes():
    base_dir = Path("02_datasets/procesados/dataset_detect_field")
    md5s = set()
    phashes = {}
    for split in ['train', 'valid', 'test']:
        img_dir = base_dir / split / "images"
        if img_dir.exists():
            for img_p in img_dir.glob("*.jpg"):
                md5s.add(compute_md5(img_p))
                ph = compute_phash(img_p)
                if ph is not None:
                    phashes[img_p] = ph
    return {'md5': md5s, 'phash': phashes}

def check_cross_duplicates(md_hashes, md_phashes, h_hashes, h_phashes):
    print("\n=== Cross Duplicates ===")
    exact = len(set(md_hashes.keys()).intersection(set(h_hashes.keys())))
    print(f"Exact duplicates MD vs HERMOS: {exact}")
    
    near = 0
    for ph1 in md_phashes.values():
        for ph2 in h_phashes.values():
            if abs(ph1 - ph2) <= 3:
                near += 1
                break
    print(f"Near duplicates MD vs HERMOS: {near}")

if __name__ == "__main__":
    df_hashes = load_detect_field_hashes()
    
    md_h, md_ph = analyze_md_nahid(
        "02_datasets/publicos/candidatos/Powdery Mildew.v1i.yolov11",
        "00_gestion/dataset_candidates_audit/md_nahid",
        df_hashes
    )
    
    h_h, h_ph = analyze_hermos(
        "02_datasets/publicos/candidatos/HERMOS",
        "00_gestion/dataset_candidates_audit/hermos",
        df_hashes
    )
    
    check_cross_duplicates(md_h, md_ph, h_h, h_ph)
