from ultralytics import YOLO
import glob
import os

def main():
    model = YOLO(r"runs/detect/yolo11m_detect_field_v1/weights/best.pt")
    
    out_dir = r"C:\Users\nsorr\.gemini\antigravity-ide\brain\b4c0c249-28c5-495e-88d9-c6bec75070a4\scratch\preds"
    
    # Get labels
    val_labels = glob.glob("02_datasets/procesados/dataset_detect_field/valid/labels/*.txt")
    
    # Only keep labels with actual content
    valid_stems = []
    for lbl in val_labels:
        with open(lbl, "r") as f:
            lines = f.readlines()
            if len(lines) > 0:
                valid_stems.append(os.path.splitext(os.path.basename(lbl))[0])
                
    italy_stems = [s for s in valid_stems if "italy_" in s.lower()]
    robo_stems = [s for s in valid_stems if "italy_" not in s.lower()]
    
    sample_stems = italy_stems[:3] + robo_stems[:3]
    
    for stem in sample_stems:
        img_path = f"02_datasets/procesados/dataset_detect_field/valid/images/{stem}.jpg"
        if not os.path.exists(img_path):
            img_path = f"02_datasets/procesados/dataset_detect_field/valid/images/{stem}.jpeg"
            if not os.path.exists(img_path):
                img_path = f"02_datasets/procesados/dataset_detect_field/valid/images/{stem}.png"
                
        if os.path.exists(img_path):
            results = model(img_path, conf=0.15)
            res = results[0]
            save_path = os.path.join(out_dir, f"pos_pred_{os.path.basename(img_path)}")
            res.save(filename=save_path)
            print(f"Saved {save_path}")

if __name__ == "__main__":
    main()
