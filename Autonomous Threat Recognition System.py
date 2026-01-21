# import cv2
# import os
# import pandas as pd
# from datetime import datetime
# from ultralytics import YOLO
#
# # ===================== CONFIG =====================
# MODEL_PATH = "yolov8n.pt"   # Replace with custom-trained model if available
# CONF_THRESHOLD = 0.4
# OUTPUT_ROOT = "outputs"
#
# THREAT_CLASSES = {
#     "person": "Hostile Movement",
#     "car": "Vehicle",
#     "truck": "Vehicle",
#     "bus": "Vehicle",
#     "motorbike": "Vehicle",
#     "knife": "Weapon",
#     "gun": "Weapon"
# }
# # ==================================================
#
# # Create date-wise output folder
# today = datetime.now().strftime("%Y-%m-%d")
# output_dir = os.path.join(OUTPUT_ROOT, today)
# os.makedirs(output_dir, exist_ok=True)
#
# video_out_path = os.path.join(output_dir, "threat_recording.mp4")
# excel_out_path = os.path.join(output_dir, "threat_report.xlsx")
#
# # Load model
# model = YOLO(MODEL_PATH)
#
# # Detection log
# report_data = []
#
# # ================= INPUT SOURCE ===================
# def get_video_source():
#     print("Select Input Source:")
#     print("1 - Live Camera")
#     print("2 - Video File")
#     choice = input("Enter choice: ")
#
#     if choice == "1":
#         return cv2.VideoCapture(0)
#     else:
#         path = input("Enter video file path: ")
#         return cv2.VideoCapture(path)
#
# cap = get_video_source()
#
# # Video writer
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# fps = int(cap.get(cv2.CAP_PROP_FPS) or 25)
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# out = cv2.VideoWriter(video_out_path, fourcc, fps, (width, height))
#
# # ================== MAIN LOOP =====================
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     results = model(frame, conf=CONF_THRESHOLD, verbose=False)
#
#     for r in results:
#         for box in r.boxes:
#             cls_id = int(box.cls[0])
#             label = model.names[cls_id]
#
#             if label in THREAT_CLASSES:
#                 threat_type = THREAT_CLASSES[label]
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 conf = float(box.conf[0])
#
#                 # Draw bounding box
#                 color = (0, 0, 255) if threat_type == "Weapon" else (0, 255, 255)
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#
#                 text = f"{threat_type}: {label} ({conf:.2f})"
#                 cv2.putText(frame, text, (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
#
#                 # Log event
#                 report_data.append({
#                     "Date": today,
#                     "Time": datetime.now().strftime("%H:%M:%S"),
#                     "Threat Type": threat_type,
#                     "Object": label,
#                     "Confidence": round(conf, 2)
#                 })
#
#     out.write(frame)
#     cv2.imshow("Autonomous Threat Recognition", frame)
#
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
#
# # ================= CLEANUP ========================
# cap.release()
# out.release()
# cv2.destroyAllWindows()
#
# # Save Excel report
# df = pd.DataFrame(report_data)
# df.to_excel(excel_out_path, index=False)
#
# print("===================================")
# print("Threat Detection Completed")
# print(f"Video saved to: {video_out_path}")
# print(f"Excel report saved to: {excel_out_path}")
# print("===================================")


import cv2
import os
import pandas as pd
from datetime import datetime
from ultralytics import YOLO

# ===================== CONFIG =====================
MODEL_PATH = "yolov8n.pt"
CONF_THRESHOLD = 0.4
OUTPUT_ROOT = "outputs"

THREAT_CLASSES = {
    "person": "Hostile Movement",
    "car": "Vehicle",
    "truck": "Vehicle",
    "bus": "Vehicle",
    "motorbike": "Vehicle",
    "knife": "Weapon",
    "gun": "Weapon"
}
# =================================================

# Timestamp
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H-%M-%S")

# Create date-wise folder
output_dir = os.path.join(OUTPUT_ROOT, date_str)
os.makedirs(output_dir, exist_ok=True)

video_out_path = os.path.join(
    output_dir, f"threat_recording_{date_str}_{time_str}.mp4"
)
excel_out_path = os.path.join(
    output_dir, f"threat_report_{date_str}_{time_str}.xlsx"
)

# Load YOLO model
model = YOLO(MODEL_PATH)

# Detection log
report_data = []

# ================= INPUT SOURCE ===================
def get_video_source():
    print("Select Input Source:")
    print("1 - Live Laptop Camera")
    print("2 - Video File")
    choice = input("Enter choice (1/2): ")

    if choice == "1":
        return cv2.VideoCapture(0)
    else:
        path = input("Enter video file path: ")
        return cv2.VideoCapture(path)

cap = get_video_source()

# Video writer setup
fps = int(cap.get(cv2.CAP_PROP_FPS) or 25)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(video_out_path, fourcc, fps, (width, height))

# ================== MAIN LOOP =====================
print("Press 'q' to quit safely")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=CONF_THRESHOLD, verbose=False)

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label in THREAT_CLASSES:
                threat_type = THREAT_CLASSES[label]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                color = (0, 0, 255) if threat_type == "Weapon" else (0, 255, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                cv2.putText(
                    frame,
                    f"{threat_type}: {label} ({conf:.2f})",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

                report_data.append({
                    "Date": date_str,
                    "Time": datetime.now().strftime("%H:%M:%S"),
                    "Threat Type": threat_type,
                    "Detected Object": label,
                    "Confidence": round(conf, 2)
                })

    out.write(frame)
    cv2.imshow("Autonomous Threat Recognition", frame)

    # ---- PRESS q TO QUIT ----
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quit command received. Closing safely...")
        break

# ================= CLEANUP ========================
cap.release()
out.release()
cv2.destroyAllWindows()

# Save Excel report
if report_data:
    df = pd.DataFrame(report_data)
    df.to_excel(excel_out_path, index=False)

print("===================================")
print("Threat Recognition Session Closed")
print(f"Video saved : {video_out_path}")
print(f"Report saved: {excel_out_path}")
print("===================================")
