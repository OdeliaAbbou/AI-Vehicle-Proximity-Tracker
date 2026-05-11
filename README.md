# 🚗 AI Vehicle Proximity Tracker

Real-time vehicle detection and tracking on video, estimating the **closest moment** of each vehicle relative to the camera.

Built with **YOLOv8** (Ultralytics) for detection and tracking, and **OpenCV** for visual rendering.

https://github.com/user-attachments/assets/d36166d4-39a0-4612-9e23-f83cb48fc72b

## How It Works

The script analyzes a video frame by frame and performs two parallel tasks:

1. **Visual tracking** — each detected vehicle gets a colored bounding box. It turns red when the vehicle approaches the frame edges (bottom, left, right), with a flash effect upon crossing.

2. **Proximity estimation** — the bounding box area is used as a proxy for distance to the camera: the larger the box, the closer the vehicle. The script records the peak area of each vehicle along with the corresponding timestamp and position.

> The crossing line (75% of frame height) is only used for visuals. Final data is based on the **actual max area**, which gives a more reliable estimate of the closest moment.

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- Ultralytics (`ultralytics`)

## Installation

```bash
pip install opencv-python ultralytics
```

The `yolov8n.pt` model (YOLOv8 Nano) is downloaded automatically on first run.

## Usage

1. Place the video file in the same folder as the script, named `video.mp4`.
2. Run the script:

```bash
python main.py
```

3. The video is displayed with real-time tracking. Press `q` to quit.
4. Results are printed to the terminal once the video ends.

## Configuration

Parameters can be adjusted at the top of the script:

| Parameter | Default | Description |
|---|---|---|
| `BOTTOM_LINE` | 75% of frame height | Position of the invisible bottom line |
| `PROXIMITY_PX` | 50 px | Proximity threshold for the bottom line |
| `PROXIMITY_PX_SIDES` | 5 px | Proximity threshold for left/right edges |
| `FLASH_DURATION` | ~0.6 sec | Duration of the red flash after crossing |

## Output

For each detected vehicle that crossed a line, the script prints:

```
Car ID: 3
Closest Time: 4.12 sec
Frame: 124
Max Area: 58320
Position: (210, 180, 450, 420)
```

- **Closest Time** — timestamp (in seconds) when the vehicle was closest
- **Max Area** — maximum bounding box area (in px²)
- **Position** — bounding box coordinates `(x1, y1, x2, y2)` at peak moment

## Color Coding (Display)

- 🟢 **Green** — vehicle detected, at normal distance
- 🔴 **Red** — vehicle near an edge or in post-crossing flash phase

## Stack

- **YOLOv8 Nano** — object detection + tracking with persistent IDs
- **OpenCV** — video reading, bounding box rendering, real-time display

## License

MIT
