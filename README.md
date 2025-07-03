
# Crefle AprilTag Calibration and Tracking

This project provides a complete system for camera calibration, AprilTag generation, and real-time object tracking using a multi-marker platform setup. It allows you to define a stable reference frame and track the 3D coordinates of an object relative to it.

## Key Features

- **Camera Calibration**: Captures checkerboard images and computes the camera matrix and distortion coefficients.
- **AprilTag Generation**: Creates and saves AprilTag markers with specified IDs.
- **Real-Time Detection**: Detects AprilTags in a live camera feed and estimates their poses.
- **Platform-Relative Tracking**: Defines a platform using four AprilTag markers and calculates the 3D coordinates of an object marker relative to the platform.

---

## File Descriptions

| File | Description |
| :--- | :--- |
| `main.py` | The main entry point for running the camera calibration process. |
| `camera_calibration.py` | Contains functions for capturing calibration images and computing camera parameters. |
| `generate_multiple_markers.py` | Generates and saves AprilTag markers for the platform and objects. |
| `run_apriltag_detector.py` | Detects all visible AprilTags and overlays their ID and distance from the camera. |
| `run_platform_systems.py` | Establishes a coordinate system using a four-marker platform and tracks an object marker relative to it. |
| `platform_logic.py` | Implements the core logic for defining the platform and calculating relative coordinates. |

---

## Workflow

### Step 1: Generate AprilTag Markers

1.  Open `generate_multiple_markers.py`.
2.  Modify the `IDS_TO_GENERATE` list to include the marker IDs you need for the platform (e.g., `[0, 1, 2, 3]`) and the object (e.g., `[10]`).
3.  Run the script to save the markers as PNG files in the `generated_markers` directory.

### Step 2: Calibrate the Camera

1.  Run `main.py`.
2.  Follow the on-screen prompts to configure the calibration settings:
    - **Camera Index**: `0` for built-in, `1` for external.
    - **Checkerboard Corners**: The number of internal corners (e.g., 6x9).
    - **Square Size**: The side length of a checkerboard square in meters.
3.  Capture at least 15-20 images of the checkerboard from different angles.
4.  The script will save the calibration data to `test-params/calibration_data.npz`.

### Step 3: Run the Platform System

1.  Arrange the four platform markers (IDs 0, 1, 2, 3) in a square, as shown in the diagram in `run_platform_systems.py`.
2.  Run `run_platform_systems.py`.
3.  Enter the marker and platform side lengths when prompted.
4.  The system will detect the platform and track the object marker (ID 10), displaying its coordinates relative to the platform's center.

---

## Configuration

- **`platform_logic.py`**: The core logic for coordinate transformation is defined here. You can modify the `define_platform_and_get_relative_coords` function to adjust how the platform is defined or how relative coordinates are calculated.
- **`run_platform_systems.py`**: This file contains the main configuration for the platform system, including marker IDs, marker layout, and 3D positions. You can change `PLATFORM_MARKER_IDS` and `OBJECT_MARKER_ID` to match your setup.
