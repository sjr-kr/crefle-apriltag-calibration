import camera_calibration as calib
import os

def main():
    print("--- Camera Calibration Setup ---")
    
    img_path = "/Users/sungjaerhee/Desktop/crefle-apriltag-calibration/checkerboards"
    output_file = "test-params/calibration_data.npz"
    
    camera_index = int(input("Enter camera index (e.g., 0 for built-in, 1 for external): "))
    rows = int(input("Enter checkerboard internal corner rows (e.g., 6): "))
    cols = int(input("Enter checkerboard internal corner columns (e.g., 9): "))
    checkerboard_size = (cols, rows)
    square_size_m = float(input("Enter checkerboard/marker square side length in meters (e.g., 0.025): "))
    num_images = int(input("Enter number of images to capture (at least 15 recommended): "))
    delay = int(input("Enter delay between captures in seconds (e.g., 2): "))

    capture_success = calib.capture_calibration_images(camera_index, num_images, delay, img_path)

    if capture_success:
        calib_success, mtx, dist = calib.run_calibration(img_path, checkerboard_size, square_size_m)
        if calib_success:
            calib.save_calibration_data(output_file, mtx, dist, camera_index, square_size_m)
    else:
        print("Calibration aborted because image capture failed or was cancelled.")

if __name__ == '__main__':
    main()