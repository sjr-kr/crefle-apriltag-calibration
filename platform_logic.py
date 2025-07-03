import cv2
import numpy as np

def define_platform_and_get_relative_coords(corners, ids, mtx, dist, platform_config):
    # 플랫폼을 기준으로 객체의 상대 3D 좌표 계산
    platform_marker_ids = platform_config['platform_marker_ids']
    marker_length = platform_config['marker_length']
    object_marker_id = platform_config['object_marker_id']

    detected_markers = {id[0]: corner for id, corner in zip(ids, corners)}

    rvec_platform_to_cam = None
    tvec_platform_to_cam = None
    is_platform_found = False

    # 플랫폼의 4개 코너가 모두 보이는지 확인
    if all(marker_id in detected_markers for marker_id in platform_marker_ids):
        points_3d = []
        points_2d = []
        for marker_id in platform_marker_ids:
            ideal_3d_points = platform_config['marker_positions_3d'][marker_id]
            detected_2d_corners = detected_markers[marker_id][0]
            for p3d, p2d in zip(ideal_3d_points, detected_2d_corners):
                points_3d.append(p3d)
                points_2d.append(p2d)

        points_3d = np.array(points_3d, dtype=np.float32)
        points_2d = np.array(points_2d, dtype=np.float32)
        
        ret, rvec_platform_to_cam, tvec_platform_to_cam = cv2.solvePnP(points_3d, points_2d, mtx, dist)
        
        if ret:
            is_platform_found = True

    # 플랫폼과 객체가 모두 찾아졌을 때만 실행
    if is_platform_found and object_marker_id in detected_markers:
        object_corners = detected_markers[object_marker_id]
        rvec_obj_to_cam, tvec_obj_to_cam, _ = cv2.aruco.estimatePoseSingleMarkers(
            object_corners, marker_length, mtx, dist
        )

        R_platform_to_cam, _ = cv2.Rodrigues(rvec_platform_to_cam)
        R_cam_to_platform = R_platform_to_cam.T
        
        t_obj_in_cam = tvec_obj_to_cam[0][0]
        t_platform_in_cam = tvec_platform_to_cam.flatten()
        
        vec_platform_to_obj_in_cam = t_obj_in_cam - t_platform_in_cam
        t_obj_in_platform = R_cam_to_platform @ vec_platform_to_obj_in_cam
        
        return True, t_obj_in_platform, rvec_platform_to_cam, tvec_platform_to_cam
    
    # 객체를 찾지 못했더라도, 플랫폼은 찾았으면 플랫폼 정보만 반환
    elif is_platform_found:
        return False, None, rvec_platform_to_cam, tvec_platform_to_cam

    # 아무것도 찾지 못했을 때
    return False, None, None, None