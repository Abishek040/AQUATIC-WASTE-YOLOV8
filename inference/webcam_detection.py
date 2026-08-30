import cv2
from pathlib import Path
from ultralytics import YOLO


# Load trained model
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "best.pt"

model = YOLO(str(MODEL_PATH))

# Open default webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")


print("Starting webcam detection...")
print("Press Q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame from webcam.")
        break

    # Run YOLO inference
    results = model.predict(
        source=frame,
        conf=0.25,
        verbose=False
    )

    # Draw detections
    annotated_frame = results[0].plot()

    # Display result
    cv2.imshow("Aquatic Waste - Floater Detection", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()