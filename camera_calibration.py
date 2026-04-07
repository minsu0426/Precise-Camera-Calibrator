import numpy as np
import cv2
import glob

BOARD_PATTERN = (8, 6) 
SIZE_OF_SQUARE = 25.0

# 3D 점 준비
objp = np.zeros((BOARD_PATTERN[0] * BOARD_PATTERN[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:BOARD_PATTERN[0], 0:BOARD_PATTERN[1]].T.reshape(-1, 2) * SIZE_OF_SQUARE

objpoints = [] # 3D 실제 점
imgpoints = [] # 2D 이미지 점

# 촬영한 영상 로드
cap = cv2.VideoCapture('45796.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, BOARD_PATTERN, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        # 코너 그리기 및 시각화
        cv2.drawChessboardCorners(frame, BOARD_PATTERN, corners, ret)
        cv2.imshow('Calibration', frame)
        cv2.waitKey(100) # 분석 속도 조절

cap.release()
cv2.destroyAllWindows()

# 캘리브레이션 수행
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print(f"RMS Error: {ret}")
print(f"Camera Matrix (K):\n{mtx}")
print(f"Distortion Coefficients:\n{dist}")

# 결과 저장
np.savez('calib_data.npz', mtx=mtx, dist=dist)