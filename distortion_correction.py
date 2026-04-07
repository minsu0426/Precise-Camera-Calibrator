import numpy as np
import cv2

with np.load('calib_data.npz') as data:
    mtx = data['mtx']
    dist = data['dist']

cap = cv2.VideoCapture('calib_video.mp4')
image_saved = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    h, w = frame.shape[:2]
    
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(frame, mtx, dist, None, new_camera_mtx)
    
    combined = np.hstack((frame, dst))
    cv2.imshow('Original vs Rectified', combined)

    # 스크린샷 자동 저장
    if not image_saved:
        cv2.imwrite('rectified_demo.jpg', combined)
        print("데모 이미지(rectified_demo.jpg) 저장 완료")
        image_saved = True

    # ESC 키 입력 시 종료
    if cv2.waitKey(1) & 0xFF == 27: 
        break 

cap.release()
cv2.destroyAllWindows()