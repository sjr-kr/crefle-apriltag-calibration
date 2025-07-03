import cv2
import numpy as np
import os

# --- 설정값 ---
# 한 번에 생성할 마커 ID 목록
IDS_TO_GENERATE = [10]

# 이미지 크기 (픽셀 단위)
PIXEL_SIZE = 400

# 저장할 디렉토리
OUTPUT_DIR = "generated_markers"
# --------------

# 사용할 AprilTag 사전 정의 (Tag36h11)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)

# 저장할 디렉토리가 없으면 생성
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Directory '{OUTPUT_DIR}' created.")

# 지정된 ID 목록을 순회하며 마커 생성
for marker_id in IDS_TO_GENERATE:
    print(f"Generating marker with ID: {marker_id}...")
    
    # 마커 이미지 생성
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, PIXEL_SIZE, borderBits=1)

    # 저장
    file_name = f"apriltag_36h11_id_{marker_id}.png"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    cv2.imwrite(file_path, marker_image)

    print(f"-> SUCCESS: Marker saved to '{file_path}'")

print("\nAll markers generated successfully.")

# 마지막 마커 preview
cv2.imshow(f"Last Generated Marker (ID: {IDS_TO_GENERATE[-1]})", marker_image)
cv2.waitKey(3000)
cv2.destroyAllWindows()