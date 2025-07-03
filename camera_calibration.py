import cv2
import numpy as np
import time
import os
import glob

# 카메라 캡쳐 로직
def capture_calibration_images(camera_index, num_images, delay, img_dir):
    print("\n--- Step 1: Image Capture ---")
    
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        print(f"ERROR: Camera index {camera_index} cannot be opened.")
        return False

    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        print(f"Directory '{img_dir}' created.")

    img_counter = 0
    print("\nPress 'c' to capture an image. Press 'q' to quit early.")

    while img_counter < num_images:
        ret, frame = camera.read()
        if not ret:
            print("ERROR: Frame cannot be read.")
            break
        
        cv2.imshow(f"Capture ({img_counter+1}/{num_images}) - Press 'c' to capture", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            img_name = os.path.join(img_dir, f"capture_{img_counter}.jpg")
            cv2.imwrite(img_name, frame)
            print(f"SUCCESS: {img_name} saved!")
            img_counter += 1
            if img_counter < num_images:
                print(f"Waiting for {delay} seconds...")
                time.sleep(delay)
        elif key == ord('q'):
            print("Capture stopped by user.")
            break

    camera.release()
    cv2.destroyAllWindows()
    
    if img_counter > 0:
        print("\nImage capture finished.")
        return True
    else:
        print("\nNo images were captured.")
        return False

# 캘리브레이션 로직
def run_calibration(img_dir, checkerboard_size, square_size_m):
    print("\n--- Step 2: Running Calibration ---")
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)
    objp = objp * square_size_m
    objpoints = []
    imgpoints = []
    images = glob.glob(os.path.join(img_dir, '*.jpg'))
    if not images:
        print(f"ERROR: No images found in '{img_dir}'.")
        return False, None, None
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
    if not objpoints:
        print("ERROR: No valid checkerboards found. Calibration failed.")
        return False, None, None

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    if ret:
        print("\nCalibration successful.")
        return True, mtx, dist
    else:
        print("\nCalibration failed.")
        return False, None, None

# .npz 파일로 캘리브레이션 값 저장
def save_calibration_data(file_path, mtx, dist, camera_index, marker_size):
    np.savez(file_path, mtx=mtx, dist=dist, camera_index=camera_index, marker_size=marker_size)
    print(f"\nSUCCESS: All data saved to '{file_path}'")