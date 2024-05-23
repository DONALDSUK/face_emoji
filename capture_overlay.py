# capture_overlay.py
import cv2
import mediapipe as mp

# MediaPipe 얼굴 검출 및 그림 그리기 유틸리티 초기화
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# 오버레이 이미지를 불러오기
image_right_eye = cv2.imread('./images/right_eye.png', cv2.IMREAD_UNCHANGED)
image_left_eye = cv2.imread('./images/left_eye.png', cv2.IMREAD_UNCHANGED)
image_nose = cv2.imread('./images/nose.png', cv2.IMREAD_UNCHANGED)

# 오버레이 이미지를 주어진 위치에 덧씌우는 함수
def overlay(image, x, y, w, h, overlay_image):
    alpha = overlay_image[:, :, 3] / 255.0
    mask_image = cv2.merge([alpha, alpha, alpha])

    # 이미지의 크기를 적절히 조정
    image_roi = image[y-h:y+h, x-w:x+w]
    if image_roi.shape[0] > 0 and image_roi.shape[1] > 0:  # 이미지가 유효한 크기를 가지고 있는지 확인
        overlay_image_resized = cv2.resize(overlay_image, (image_roi.shape[1], image_roi.shape[0]))

        for c in range(0, 3):
            image_roi[:, :, c] = (overlay_image_resized[:, :, c] * mask_image[:, :, c] +
                                   image_roi[:, :, c] * (1.0 - mask_image[:, :, c]))
        image[y-h:y+h, x-w:x+w] = image_roi

# 웹캠에서 프레임을 캡처하고 처리하는 제너레이터 함수
def generate_frames():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
        while True:
            success, image = cap.read()
            if not success:
                break

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = face_detection.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.detections:
                for detection in results.detections:
                    keypoints = detection.location_data.relative_keypoints
                    left_eye = keypoints[0]
                    right_eye = keypoints[1]
                    nose_tip = keypoints[2]
                    h, w, _ = image.shape
                    right_eye = (int(right_eye.x * w) + 20, int(right_eye.y * h) - 100)
                    left_eye = (int(left_eye.x * w) - 20, int(left_eye.y * h) - 100)
                    nose_tip = (int(nose_tip.x * w), int(nose_tip.y * h))

                    # 오른쪽 눈, 왼쪽 눈, 코 위치에 오버레이 이미지 적용
                    overlay(image, *right_eye, 50, 50, image_right_eye)
                    overlay(image, *left_eye, 50, 50, image_left_eye)
                    overlay(image, *nose_tip, 150, 50, image_nose)

            # 프레임을 JPEG 형식으로 인코딩하여 스트리밍
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            # 프레임을 multipart/x-mixed-replace 형식으로 반환
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
