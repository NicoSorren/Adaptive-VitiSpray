import cv2
import sys
from pathlib import Path

def main():
    from vitispray.paths import YOLO_DIR
    ext_dir = YOLO_DIR / "external_validation"
    out_dir = ext_dir / "reports" / "panels"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    images = list(ext_dir.glob("*.jpg"))
    for img_p in images:
        orig = cv2.imread(str(img_p))
        c25 = cv2.imread(str(ext_dir / "predictions_v2_conf025" / img_p.name))
        c50 = cv2.imread(str(ext_dir / "predictions_v2_conf050" / img_p.name))
        c70 = cv2.imread(str(ext_dir / "predictions_v2_conf070" / img_p.name))
        
        # resize all to 640 height maintaining aspect ratio
        h, w = orig.shape[:2]
        new_h = 640
        new_w = int(w * (new_h / h))
        
        def resize_img(img):
            return cv2.resize(img, (new_w, new_h))
            
        panel = cv2.hconcat([resize_img(orig), resize_img(c25), resize_img(c50), resize_img(c70)])
        
        # Add labels
        cv2.putText(panel, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(panel, "Conf 0.25", (new_w + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(panel, "Conf 0.50", (2 * new_w + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(panel, "Conf 0.70", (3 * new_w + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        cv2.imwrite(str(out_dir / f"panel_{img_p.name}"), panel)
        
if __name__ == "__main__":
    main()
