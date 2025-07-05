import cv2
import numpy as np
import os

CALIB_DATA_PATH = "test-params/calibration_data.npz"

if not os.path.exists(CALIB_DATA_PATH):
    print(f"Error: Calibration data file not found at '{CALIB_DATA_PATH}'")
    print("Please run 'main.py' to calibrate the camera first.")
    exit()

with np.load(CALIB_DATA_PATH) as data:
    mtx = data['mtx']
    dist = data['dist']
    CAMERA_INDEX = int(data['camera_index'])
    MARKER_LENGTH_M = float(data['marker_size'])

print("Calibration data and settings loaded successfully:")
print(f"  - Camera Index: {CAMERA_INDEX}")
print(f"  - Marker Length: {MARKER_LENGTH_M} m")

# 일단 Tag36h11로 테스트, 추후에 변경 가능
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
params = cv2.aruco.DetectorParameters()

# 1: 아이폰 카메라, 2: 외장 카메라
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print(f"Error: Camera index {CAMERA_INDEX} cannot be opened.")
    exit()

print("Starting detector... Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Frame cannot be read.")
        break

    # 흑백 -> 컬러
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=params)

    if ids is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, MARKER_LENGTH_M, mtx, dist)

        for i in range(len(ids)):
            cv2.drawFrameAxes(frame, mtx, dist, rvecs[i], tvecs[i], MARKER_LENGTH_M / 2)
            
            cv2.aruco.drawDetectedMarkers(frame, corners)
            tvec = tvecs[i][0]
            coord_text = f"ID: {ids[i][0]} Z: {tvec[2]:.3f} m"
            corner_point = corners[i][0][0]
            text_pos = (int(corner_point[0]), int(corner_point[1] - 15))
            cv2.putText(frame, coord_text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 카메라 Real-Time 디스플레이
    cv2.imshow('AprilTag Detector', frame)

    # q 누르면 중단
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Detector stopped.")