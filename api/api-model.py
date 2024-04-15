import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Dict
import os
import tempfile
import logging
from ultralytics import YOLO
import uvicorn

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
# Load your YOLO model
model_path = r"C:/Users/harsh/Desktop/programming_in_general/Python/yolov8s.pt"
model = YOLO(model_path)

# Define the mapping of vehicle names to categories
vehicle_categories = {
    "ambulance": "ambulance",
    "bicycle": "bicycles",
    "bus": "buses",
    "fire hydrant": None,
    "bicycle": "bicycles",
    "truck": "trucks",
    "unicycle": "bicycles",
    "van": "vans",
    "car": "cars",
    "taxi": "cars",
    "green auto": "cars",
    "red auto": "cars",
    "train": "trains",
    "tractor": "tractors",
}


def count_vehicles(results) -> Dict[str, int]:
    """
    Count the number of different types of vehicles detected in YOLO results.
    """
    vehicles = {category: 0 for category in vehicle_categories.values() if category}
    print("Results inside count_vehicles:")
    print(results)
    for result in results:
        print("Result inside result:")
        print(result)
        for label in result.names.values():
            print("Label inside result.names.values():")
            print(label)
            category = vehicle_categories.get(label)
            print("Category inside result.names.values():")
            print(category)
            if category:
                vehicles[category] += 1
    return vehicles


@app.post("/process_video/")
async def process_video(video_file: UploadFile = File(...)):
    # Create a temporary file to write the video byte stream
    with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
        temp_video_file.write(await video_file.read())
        temp_video_file_path = temp_video_file.name
    try:
        logging.debug("Temporary video file created: %s", temp_video_file_path)
        # Initialize empty list to store timestamped predictions
        timestamped_predictions = []
        # Load video file using OpenCV
        cap = cv2.VideoCapture(temp_video_file_path)
        # Check if video capture was successful
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Error opening video file")
        logging.debug("Video capture successful")

        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Loop through the video frames
        for frame_index in range(int(frame_count)):
            # Read frame from video
            success, frame = cap.read()
            if not success:
                break  # Break loop if no frame is retrieved
            logging.debug("Frame read successfully")
            # Resize frame if needed
            frame = cv2.resize(frame, (700, 500))
            # Run YOLO inference on the frame
            results = model(frame)
            print(results)  # Add this line to verify YOLO results
            logging.debug("YOLO inference completed")
            # Count vehicles in YOLO results
            vehicle_counts = count_vehicles(results)
            print(vehicle_counts)  # Add this line to debug vehicle counts
            # Calculate timestamp based on frame index and frame rate
            timestamp = frame_index / frame_rate
            # Append timestamped predictions to the list
            timestamped_predictions.append(
                {
                    "timestamp": timestamp,
                    "road": 0,  # Assuming road is always 0 for now
                    "vehicles": vehicle_counts,
                }
            )

        # Release the video capture object
        cap.release()
        logging.debug("Video capture object released")
        # Return timestamped predictions
        return {"predictions": timestamped_predictions}
    finally:
        # Delete the temporary video file
        if temp_video_file_path:
            os.unlink(temp_video_file_path)
            logging.debug("Temporary video file deleted")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
