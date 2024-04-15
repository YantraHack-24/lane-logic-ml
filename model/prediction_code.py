import cv2
from ultralytics import YOLO

# Path to the trained model
model_path = r"C:/Users/harsh/Desktop/programming_in_general/Python\best(1).pt"
# Path to the video file
# Ambulance
video_path = r"C:\Users\harsh\Desktop\programming_in_general\Python\ambulance_tests.mp4"
# Normal Test Case
# video_path = r"C:\Users\harsh\Desktop\programming_in_general\Python\3759222-hd_1920_1080_30fps.mp4"
# Jam
# video_path = r"C:\Users\harsh\Desktop\programming_in_general\Python\Test_video_1.mp4"
# Load the YOLO model
model = YOLO(model_path)
cap = cv2.VideoCapture(video_path)
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        frame = cv2.resize(frame, (700, 500))
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Print the type of results object
        print("Type of results:", type(results))

        # Print the contents of the results object
        print("Contents of results:", results)

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
