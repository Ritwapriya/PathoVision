from ultralytics import YOLO
import os
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from google import genai
from dotenv import load_dotenv
from config.friendly_names import friendly_names
from config.gemini_prompt_builder import build_gemini_prompt
from config.basic_threat_report import create_threat_report
from datetime import datetime
# ---------------------------
# 0) Load environment variables
# ---------------------------
load_dotenv()

# ---------------------------
# 1) Run YOLO detection
# ---------------------------
model_path = r"Model\Patho.pt"
image_path = r"test_images\test4.jpg"

model = YOLO(model_path)
results = model.predict(source=image_path, imgsz=640, conf=0.25, save=False)

# Show annotated image
annotated_img = results[0].plot()
plt.imshow(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("YOLOv8 Detection")
plt.show()

# ---------------------------
# 2) Extract labels + counts
# ---------------------------
detected_labels_raw = [model.names[int(box.cls)] for box in results[0].boxes]
label_counts = Counter(detected_labels_raw)

friendly_summary = []
for lab, cnt in label_counts.items():
    friendly_label = friendly_names.get(lab, lab.replace('_', ' ').title())
    friendly_summary.append({
        "label": lab,
        "friendly": friendly_label,
        "count": int(cnt),
        "category": "Environmental Hazard"  # example extra param
    })

# ---------------------------
# 3) Build prompt
# ---------------------------
prompt = build_gemini_prompt(friendly_summary, mode="paragraph")

# ---------------------------
# 4) Call Gemini API
# ---------------------------
if "GEMINI_API_KEY" not in os.environ:
    raise RuntimeError("Please set GEMINI_API_KEY in your environment or .env file.")

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
gemini_text = response.text

# After calling Gemini API
print("\n--- Gemini Environmental Risk Explanation ---\n")
print(gemini_text)

choice = input("\nDo you want to download a detailed report? (y/n): ").lower()
if choice == "y":
    # Generate timestamp in format YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"Detailed_Threat_Report_{timestamp}.pdf"
    
    create_threat_report(report_file, model_name="PATHOVISION", gemini_text=gemini_text)
    print(f"Report has been generated: {report_file}")