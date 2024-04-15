from ultralytics import YOLO

model = YOLO(
    r"C:\Users\Sagar\Python files_Jupiter\Git Repo Local\SIH traffic project\runs\detect\train2\weights\last.pt"
)

results = model.train(
    data="config.yaml",
    epochs=300,
    batch=10,
    optimizer="Adam",
    lr0=0.0005,
    workers=2,
    amp=False,
)

results = model.train(resume=True)

import os
import matplotlib.pyplot as plt

for i, f in enumerate(
    os.listdir(
        r"C:\Users\Sagar\Python files_Jupiter\Git Repo Local\SIH traffic project\data\images\val"
    )
):
    results = model(
        os.path.join(
            r"C:\Users\Sagar\Python files_Jupiter\Git Repo Local\SIH traffic project\data\images\val",
            f,
        )
    )
    for img in results:
        plt.imsave(
            f"C:/Users/Sagar/Python files_Jupiter/Git Repo Local/SIH traffic project/result/{i}.jpg",
            img.plot(),
        )

results = model(
    [
        r"C:\Users\Sagar\Python files_Jupiter\Git Repo Local\SIH traffic project\test1.jpg",
        r"C:\Users\Sagar\Python files_Jupiter\Git Repo Local\SIH traffic project\test2.jpg",
        r"C:\Users\Sagar\Python files_Jupiter\Git Repo Local\SIH traffic project\test3.jpg",
    ]
)

for result in results:
    print(result.boxes.cls)

for i, res in enumerate(results):
    plt.imsave(f"./res{i}.jpg", res.plot())

import cv2
from ultralytics import YOLO

# Open the video file
video_path = r"C:\Users\Sagar\Python files_Jupiter\Git Repo Local\SIH traffic project\Test_video_1.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        frame = cv2.resize(frame, (700, 500))
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
