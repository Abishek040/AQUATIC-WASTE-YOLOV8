import cv2
import argparse
from pathlib import Path
from ultralytics import YOLO


def main():

    parser = argparse.ArgumentParser(
        description="YOLOv8 floating-object detection on video"
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Path to input video"
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold"
    )

    parser.add_argument(
        "--output",
        default="detection_output.mp4",
        help="Output video filename"
    )

    args = parser.parse_args()

    # Locate model
    model_path = (
        Path(__file__).resolve().parent.parent
        / "models"
        / "best.pt"
    )

    model = YOLO(str(model_path))

    # Open video
    cap = cv2.VideoCapture(args.source)

    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open video: {args.source}"
        )

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    # Create output writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        args.output,
        fourcc,
        fps,
        (width, height)
    )

    print("Starting video detection...")
    print(f"Input : {args.source}")
    print(f"Output: {args.output}")
    print(f"Confidence: {args.conf}")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # YOLO inference
        results = model.predict(
            source=frame,
            conf=args.conf,
            verbose=False
        )

        # Draw bounding boxes
        annotated_frame = results[0].plot()

        # Save frame
        writer.write(annotated_frame)

        # Display
        cv2.imshow(
            "Aquatic Waste - Floater Detection",
            annotated_frame
        )

        # Press Q to stop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    print("Detection completed.")


if __name__ == "__main__":
    main()