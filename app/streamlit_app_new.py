import streamlit as st
import requests
import pandas as pd
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
import warnings

# Global variable to track the uploaded status of each road
uploaded_roads = {"Road 1": False, "Road 2": False, "Road 3": False, "Road 4": False}
warnings.filterwarnings("ignore")


def run():
    st.set_page_config(
        page_title="Traffic Management System",
        page_icon="🚦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.sidebar.image("https://iili.io/JvkMvf9.png")
    st.write("# Lane Logic: Crafting Seamless Urban Traffic Solutions")

    st.markdown(
        """
        We propose the implementation of a lane priority algorithm to assist traffic junction congestions in urban areas. The deep learning algorithm and API calls operate on parallel threads, while the priority algorithm runs multiple times within each cycle. The cycle time is defined as the total time taken for each lane to receive the green light at least once. Once every lane has received a green light in the current cycle, the cycle is reset, and the priority mask is updated. The priority mask consists of four floating-point values ranging from 0 to 1.
    """
    )

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # In each column, display a video player
    video_file_1 = st.sidebar.file_uploader("Upload Video 1", type=["mp4"])
    video_file_2 = st.sidebar.file_uploader("Upload Video 2", type=["mp4"])
    video_file_3 = st.sidebar.file_uploader("Upload Video 3", type=["mp4"])
    video_file_4 = st.sidebar.file_uploader("Upload Video 4", type=["mp4"])

    if video_file_1 is not None:
        col1.video(video_file_1)
        uploaded_roads["Road 1"] = True
    if video_file_2 is not None:
        col2.video(video_file_2)
        uploaded_roads["Road 2"] = True
    if video_file_3 is not None:
        col3.video(video_file_3)
        uploaded_roads["Road 3"] = True
    if video_file_4 is not None:
        col4.video(video_file_4)
        uploaded_roads["Road 4"] = True

    if st.button("Analyze Videos"):
        with st.spinner("Analyzing Videos..."):
            st.components.v1.html(
                """<script>
                let videos = parent.document.querySelectorAll("video");
                videos.forEach(v => {
                    v.play();
                })
                </script>""",
                width=0,
                height=0,
            )
            responses = {}
            if video_file_1:
                responses["road1"] = send_to_endpoint(video_file_1)
            if video_file_2:
                responses["road2"] = send_to_endpoint(video_file_2)
            if video_file_3:
                responses["road3"] = send_to_endpoint(video_file_3)
            if video_file_4:
                responses["road4"] = send_to_endpoint(video_file_4)

            # Store in session state
            st.session_state["responses"] = responses
            st.session_state["response_ready"] = True

    if "response_ready" in st.session_state and st.session_state["response_ready"]:
        # Display the DataFrames from responses
        col1, col2, col3, col4 = st.columns(4)
        for road_key, response in st.session_state["responses"].items():
            roads = {
                "road1": "Road 1",
                "road2": "Road 2",
                "road3": "Road 3",
                "road4": "Road 4",
            }
            predictions = response["predictions"]
            timestamps = []
            road = []
            vehicle_columns = []

            for item in predictions:
                timestamps.append(item["timestamp"])
                road.append(item["road"])
                vehicles = item["vehicles"]
                for vehicle, count in vehicles.items():
                    if vehicle not in vehicle_columns:
                        vehicle_columns.append(vehicle)

            df = pd.DataFrame(columns=["Timestamp", "Road"] + vehicle_columns)

            for item in predictions:
                vehicles = item["vehicles"]
                row = [item["timestamp"], item["road"]]
                for col in vehicle_columns:
                    row.append(vehicles.get(col, 0))
                df.loc[len(df)] = row

            # return df
            st.write(f"## Response Video for {roads[road_key]}:")
            st.write(df)

        if st.button("Generate Optimal Traffic Path", key="generate_button"):
            generate_traffic_table()


def send_to_endpoint(video_file):
    endpoint_url = "http://127.0.0.1:8000/process_video"
    files = {"video_file": ("video.mp4", video_file, "video/mp4")}
    response = requests.post(endpoint_url, files=files)
    return response.json()


def generate_traffic_table():
    timestamps = []
    roads = [
        road for road, uploaded in uploaded_roads.items() if uploaded
    ]  # Filter uploaded roads
    if not roads:
        print("No roads uploaded.")  # Display message if no roads are uploaded
        return None

    green_time = send_to_endpoint(timestamps)
    selected_roads = send_to_endpoint(timestamps)

    df = pd.DataFrame(
        {
            "Timestamp": timestamps,
            "Road To Be Kept Green": selected_roads,
            "Green Time": green_time,
        }
    )

    st.write(df)
    st.set_option("deprecation.showPyplotGlobalUse", False)
    # Generate pie chart
    road_counts = df["Road To Be Kept Green"].value_counts()
    plt.figure(figsize=(8, 6))  # Adjust the size of the figure
    plt.style.use("dark_background")  # Set the theme to dark
    road_counts.plot(kind="bar")
    plt.title("Traffic Distribution")
    plt.xlabel("Road")
    plt.ylabel("Frequency or number of vehicles detected on each road")
    # Display pie chart
    st.pyplot()
    st.write(
        """
             In a traffic management context, the count represents the *frequency or number of vehicles* detected on each road during a specific period of time. This information can be valuable for understanding the distribution of traffic across different roads and intersections within a city or urban area.
             For instance, **if Road 1 has a higher count compared to other roads, it suggests that more vehicles are using Road 1 during the analyzed period. This could indicate that Road 1 is a major thoroughfare or that there may be congestion or other traffic-related issues that need attention**.
             Analyzing and visualizing the count of vehicles on each road can help traffic engineers, urban planners, and policymakers make informed decisions about traffic flow management, infrastructure improvements, traffic signal timings, and other measures aimed at optimizing traffic flow and reducing congestion.
        """
    )


if __name__ == "__main__":
    run()
