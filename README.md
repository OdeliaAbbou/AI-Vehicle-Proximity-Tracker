# AI Vehicle Proximity Tracker

A real-time computer vision project using YOLOv8 and OpenCV to detect, track, and analyze vehicle proximity in video streams.

## Features

* Real-time vehicle detection using YOLOv8
* Persistent object tracking with unique IDs
* Closest moment estimation using bounding box area
* Visual proximity alerts with dynamic color changes
* Flash effect when a vehicle crosses virtual boundaries
* Frame and timestamp recording
* Vehicle trajectory analysis

## Technologies Used

* Python
* OpenCV
* YOLOv8 (Ultralytics)
* Computer Vision
* Object Tracking

## How It Works

The system processes a video frame by frame.

For each detected vehicle:

* YOLO detects the object
* A tracking ID is assigned
* The bounding box area is calculated
* The largest area observed is stored as the closest moment to the camera

The project also detects when vehicles approach invisible boundaries near:

* bottom edge
* left edge
* right edge

Vehicles close to these zones are highlighted in red.

## Installation

```bash
pip install ultralytics opencv-python
```

## Run

```bash
python main.py
```

## Example Output

```text
Car ID: 3
Closest Time: 4.21 sec
Frame: 126
Max Area: 52300
```

## Project Structure

```text
project/
│
├── main.py
├── video.mp4
├── yolov8n.pt
└── README.md
```

## Concepts Demonstrated

* Object Detection
* Multi-Object Tracking
* Spatial Analysis
* Video Processing
* Real-Time Visualization
* Bounding Box Analysis
* Frame-by-Frame Processing

## Future Improvements

* Speed estimation
* Lane detection
* Distance approximation in meters
* Heatmap visualization
* Vehicle classification filtering
* GPU acceleration
