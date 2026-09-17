import yaml
import csv
from pathlib import Path
import json
import os

runs_dirs = [
    "runs/train/baseline_v1",
    "runs/train/baseline_80epochs",
    "runs/train/monoclass_pm_v1",
    "runs/train/test_sanity_check",
    "runs/detect/yolo11s_detect_field_v1",
    "runs/detect/yolo11s_detect_field_v2",
    "runs/detect/yolo11m_detect_field_v1"
]

results = []

for run_path in runs_dirs:
    p = Path(run_path)
    if not p.exists(): continue
    
    args_file = p / "args.yaml"
    csv_file = p / "results.csv"
    
    info = {"run_name": p.name, "path": str(p)}
    info["timestamp"] = os.path.getmtime(p) if p.exists() else None
    
    if args_file.exists():
        with open(args_file, "r") as f:
            args = yaml.safe_load(f)
            info["model"] = args.get("model", "unknown")
            info["data"] = args.get("data", "unknown")
            info["epochs"] = args.get("epochs", "unknown")
            info["batch"] = args.get("batch", "unknown")
            info["imgsz"] = args.get("imgsz", "unknown")
            info["optimizer"] = args.get("optimizer", "unknown")
            info["lr0"] = args.get("lr0", "unknown")
            info["seed"] = args.get("seed", "unknown")
            info["device"] = args.get("device", "unknown")
            info["augmentations"] = {
                "hsv_h": args.get("hsv_h"),
                "hsv_s": args.get("hsv_s"),
                "hsv_v": args.get("hsv_v"),
                "degrees": args.get("degrees"),
                "translate": args.get("translate"),
                "scale": args.get("scale"),
                "shear": args.get("shear"),
                "perspective": args.get("perspective"),
                "flipud": args.get("flipud"),
                "fliplr": args.get("fliplr"),
                "mosaic": args.get("mosaic"),
                "mixup": args.get("mixup")
            }
            
    if csv_file.exists():
        try:
            with open(csv_file, "r") as f:
                reader = csv.DictReader(f)
                headers = [h.strip() for h in reader.fieldnames]
                rows = list(reader)
                
            if rows:
                last_row = {k.strip(): v.strip() for k, v in rows[-1].items()}
                
                info["epochs_completed"] = int(last_row.get("epoch", 0))
                
                precision_col = [c for c in headers if "precision" in c.lower()]
                recall_col = [c for c in headers if "recall" in c.lower()]
                map50_col = [c for c in headers if "map50" in c.lower() and "95" not in c.lower()]
                map5095_col = [c for c in headers if "map50-95" in c.lower()]
                
                if precision_col: info["precision"] = last_row.get(precision_col[0])
                if recall_col: info["recall"] = last_row.get(recall_col[0])
                if map50_col: info["map50"] = last_row.get(map50_col[0])
                if map5095_col: info["map50_95"] = last_row.get(map5095_col[0])
        except Exception as e:
            info["csv_error"] = str(e)
            
    info["has_best"] = (p / "weights" / "best.pt").exists()
    info["has_last"] = (p / "weights" / "last.pt").exists()
            
    results.append(info)

results.sort(key=lambda x: x.get("timestamp", 0))

print(json.dumps(results, indent=2))
