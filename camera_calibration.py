import numpy as np
import cv2

# 체스보드 내부 코너 개수 (가로, 세로)
BOARD_PATTERN = (10, 7) 
# 체스보드 한 칸의 실제 크기 (mm 등 단위 통일)
SIZE_OF_SQUARE = 18.0

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((BOARD_PATTERN[0] * BOARD_PATTERN[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:BOARD_PATTERN[0], 0:BOARD_PATTERN[1]].T.reshape(-1, 2) * SIZE_OF_SQUARE

objpoints = []
imgpoints = []

cap = cv2.VideoCapture('calib_video.mp4')
frame_count = 0
# 연산량 감소를 위해 15프레임당 1번씩 코너 검출
frame_interval = 15 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    if frame_count % frame_interval == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret_corners, corners = cv2.findChessboardCorners(gray, BOARD_PATTERN, None)

        if ret_corners:
            objpoints.append(objp)
            
            # Sub-pixel 수준으로 코너 좌표 정밀 보정
            corners_subpix = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners_subpix)
            
            cv2.drawChessboardCorners(frame, BOARD_PATTERN, corners_subpix, ret_corners)
            cv2.imshow('Calibration', frame)
            cv2.waitKey(100) 
            
    frame_count += 1

cap.release()
cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print(f"RMS Error: {ret}")
print(f"Camera Matrix (K):\n{mtx}")
print(f"Distortion Coefficients:\n{dist}")

# 산출된 캘리브레이션 파라미터 저장
np.savez('calib_data.npz', mtx=mtx, dist=dist)