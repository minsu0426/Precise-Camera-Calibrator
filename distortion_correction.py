import numpy as np
import cv2

# 데이터 로드
with np.load('calib_data.npz') as data:
    mtx = data['mtx']
    dist = data['dist']

cap = cv2.VideoCapture('45796.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    h, w = frame.shape[:2]
    # 최적의 카메라 매트릭스 계산
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # 왜곡 보정 수행
    dst = cv2.undistort(frame, mtx, dist, None, new_camera_mtx)
    
    # 결과 비교를 위해 나란히 붙이기
    combined = np.hstack((frame, dst))
    cv2.imshow('Original vs Rectified', combined)

    if cv2.waitKey(1) & 0xFF == 27: break # ESC로 종료

cap.release()
cv2.destroyAllWindows()