import cv2
import numpy as np
import hashlib
from pathlib import Path
from PIL import Image
import imagehash
from collections import defaultdict
import builtins
import time

def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

def compute_hashes(img_path):
    md5 = hashlib.md5()
    with open(img_path, "rb") as f:
        md5.update(f.read())
    
    try:
        img = Image.open(img_path)
        ph = imagehash.phash(img)
        dh = imagehash.dhash(img)
        return md5.hexdigest(), ph, dh
    except Exception as e:
        return md5.hexdigest(), None, None

def audit():
    base_dir = Path("02_datasets/publicos/candidatos/Portugal/resized/Powdery Mildew")
    images = list(base_dir.glob("*.jpg")) + list(base_dir.glob("*.JPG")) + list(base_dir.glob("*.png"))
    
    print(f"Total images: {len(images)}")
    
    # Analyze filenames
    # Example format: might be IMG_20210515_... or something
    prefixes = defaultdict(int)
    for img_p in images:
        name = img_p.name
        # Try to find a pattern. Let's split by underscore or hyphen
        parts = name.replace('-', '_').split('_')
        if len(parts) > 1:
            prefix = parts[0]
            if len(prefix) < 4: 
                prefix = "_".join(parts[:2])
            prefixes[prefix] += 1
        else:
            prefixes["NO_DELIMITER"] += 1
            
    print("\n--- Filename Prefixes ---")
    for k, v in sorted(prefixes.items(), key=lambda item: item[1], reverse=True)[:10]:
        print(f"  {k}: {v}")
        
    print("\nSample filenames:")
    for img_p in images[:5]:
        print(f"  {img_p.name}")
        
    print("\n--- Hashing ---")
    start = time.time()
    
    md5_dict = defaultdict(list)
    phash_dict = {}
    dhash_dict = {}
    
    for idx, img_p in enumerate(images):
        if idx % 200 == 0: print(f" Hashing {idx}/{len(images)}...")
        m, p, d = compute_hashes(img_p)
        md5_dict[m].append(img_p)
        if p is not None:
            phash_dict[img_p] = p
            dhash_dict[img_p] = d
            
    print(f"Hashing done in {time.time()-start:.1f}s")
    
    exact_dups = sum(len(lst)-1 for lst in md5_dict.values() if len(lst) > 1)
    print(f"\nExact duplicates (MD5): {exact_dups} duplicate images")
    
    # Near duplicates
    near_dups = set()
    phash_pairs = set()
    
    # Since 2252 isn't too large, O(N^2) comparison takes 2252 * 2252 / 2 = 2.5 million operations. Very fast.
    img_list = list(phash_dict.keys())
    
    print("Finding near duplicates...")
    for i in range(len(img_list)):
        p1 = phash_dict[img_list[i]]
        for j in range(i+1, len(img_list)):
            p2 = phash_dict[img_list[j]]
            if abs(p1 - p2) <= 5: # Threshold of 5 for near duplicate
                near_dups.add(img_list[i])
                near_dups.add(img_list[j])
                phash_pairs.add((img_list[i], img_list[j], abs(p1 - p2)))
                
    print(f"\nNear duplicates (pHash <= 5): {len(near_dups)} images involved in {len(phash_pairs)} pairs")
    
    # Count how many independent images remain
    # Easiest way: build connected components
    parent = {img: img for img in img_list}
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i])
        return parent[i]
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            
    for i, j, dist in phash_pairs:
        union(i, j)
        
    unique_roots = set(find(img) for img in img_list)
    print(f"\nEstimated independent images (after collapsing near-duplicates): {len(unique_roots)}")

if __name__ == "__main__":
    audit()
