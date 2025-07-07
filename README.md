# AprilTag Calibration and Detection Suite

This project provides a suite of tools for generating AprilTags, calibrating a camera, and detecting AprilTags in images.

## Features

*   **Generate AprilTags:** Create multiple AprilTag markers with specified IDs.
*   **Camera Calibration:** Calibrate a camera using a set of captured images.
*   **AprilTag Detection:** Detect AprilTags in images using the calibrated camera parameters.
*   **Platform Logic:** Control platform systems based on AprilTag detection (stubbed).

## Getting Started

### Prerequisites

*   Python 3
*   OpenCV
*   NumPy

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/crefle-apriltag-calibration.git
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Generate AprilTags

To generate AprilTag markers, run the `generate_multiple_markers.py` script:

```bash
python generate_multiple_markers.py
```

This will create a set of AprilTag markers in the `generated_markers` directory.

### 2. Calibrate the Camera

To calibrate the camera, you need a set of images of a checkerboard pattern. Place these images in the `test-images` directory. Then, run the `camera_calibration.py` script:

```bash
python camera_calibration.py
```

This will create a `calibration_data.npz` file in the `test-params` directory, which contains the camera matrix and distortion coefficients.

### 3. Run the AprilTag Detector

To detect AprilTags in an image, run the `run_apriltag_detector.py` script:

```bash
python run_apriltag_detector.py --image <path_to_image>
```

Replace `<path_to_image>` with the path to the image you want to process. The script will use the calibration data from `test-params/calibration_data.npz` to detect the AprilTags.

### 4. Run the Platform Systems

To run the platform systems, which include the AprilTag detector and platform logic, run the `run_platform_systems.py` script:

```bash
python run_platform_systems.py
```

This script will process the images in the `test-images` directory and print the detected AprilTags.

## File Descriptions

*   `main.py`: The main entry point for the application.
*   `generate_multiple_markers.py`: Generates AprilTag markers.
*   `camera_calibration.py`: Calibrates the camera.
*   `run_apriltag_detector.py`: Detects AprilTags in an image.
*   `run_platform_systems.py`: Runs the platform systems.
*   `platform_logic.py`: Contains the platform logic.
*   `requirements.txt`: The Python dependencies.
*   `snapcraft.yaml`: The Snapcraft configuration file.
*   `nodesource_setup.sh`: A script to set up Node.js.
*   `.env`: The environment variables.
*   `README.md`: This file.
*   `generated_markers/`: The directory for the generated AprilTag markers.
*   `test-images/`: The directory for the test images.
*   `test-params/`: The directory for the calibration data.
