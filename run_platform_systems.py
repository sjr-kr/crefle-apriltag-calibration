import cv2
import numpy as np
import os
import platform_logic as pl

# calibration data 불러오기
CALIB_DATA_PATH = "test-params/calibration_data.npz"

# 없으면 프로그램 종료
if not os.path.exists(CALIB_DATA_PATH):
    print(f"Error: Calibration data not found. Please run main.py first.")
    exit()

with np.load(CALIB_DATA_PATH) as data:
    mtx = data['mtx']
    dist = data['dist']
    CAMERA_INDEX = int(data['camera_index'])

print("--- System Configuration ---")
marker_length = float(input("Enter the marker side length in meters (e.g., 0.04 for 4cm): "))
platform_size = float(input("Enter the platform side length in meters (e.g., 0.2 for 20cm): "))

PLATFORM_MARKER_IDS = [0, 1, 2, 3] 
OBJECT_MARKER_ID = 10 

half_size = platform_size / 2
half_marker = marker_length / 2

        
"""
마커를

id=0   id=1
id=3   id=2

이런 식으로 놔야 x,y,z 좌표가 생성됨
"""

MARKER_POSITIONS_3D = {
    0: np.array([[-half_size-half_marker,  half_size+half_marker, 0], [-half_size+half_marker,  half_size+half_marker, 0], [-half_size+half_marker,  half_size-half_marker, 0], [-half_size-half_marker,  half_size-half_marker, 0]]),
    1: np.array([[ half_size-half_marker,  half_size+half_marker, 0], [ half_size+half_marker,  half_size+half_marker, 0], [ half_size+half_marker,  half_size-half_marker, 0], [ half_size-half_marker,  half_size-half_marker, 0]]),
    2: np.array([[ half_size-half_marker, -half_size+half_marker, 0], [ half_size+half_marker, -half_size+half_marker, 0], [ half_size+half_marker, -half_size-half_marker, 0], [ half_size-half_marker, -half_size-half_marker, 0]]),
    3: np.array([[-half_size-half_marker, -half_size+half_marker, 0], [-half_size+half_marker, -half_size+half_marker, 0], [-half_size+half_marker, -half_size-half_marker, 0], [-half_size-half_marker, -half_size-half_marker, 0]])
}

PLATFORM_CONFIG = {
    "platform_marker_ids": PLATFORM_MARKER_IDS,
    "marker_length": marker_length,
    "object_marker_id": OBJECT_MARKER_ID,
    "marker_positions_3d": MARKER_POSITIONS_3D
}

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
params = cv2.aruco.DetectorParameters()

cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print(f"Error: Camera index {CAMERA_INDEX} cannot be opened.")
    exit()

print("\nStarting platform system... Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=params)

    # 마커 detection 성공
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        success, rel_coords, rvec_obj_in_platform, rvec_plat, tvec_plat = pl.define_platform_and_get_relative_coords(
            corners, ids, mtx, dist, PLATFORM_CONFIG
        )

        # rotation vector가 있음 -> 각도 return
        if rvec_plat is not None:
            cv2.drawFrameAxes(frame, mtx, dist, rvec_plat, tvec_plat, 0.1)

        if success:
            coord_text = f"Obj Coords (Platform Ref): X:{rel_coords[0]:.3f} Y:{rel_coords[1]:.3f} Z:{rel_coords[2]:.3f}"
            cv2.putText(frame, coord_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display rotation vector if available
            if rvec_obj_in_platform is not None:
                rot_text = f"Obj Rot (Platform Ref): RX:{rvec_obj_in_platform[0][0]:.3f} RY:{rvec_obj_in_platform[1][0]:.3f} RZ:{rvec_obj_in_platform[2][0]:.3f}"
                cv2.putText(frame, rot_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("플랫폼 좌표 테스트", frame)

    # Q 입력 시 loop 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()