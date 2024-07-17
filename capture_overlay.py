import cv2
import mediapipe as mp


mp_face_detection = mp.solutions.face_detection #mediapipe에서 제공하는 얼굴인식 머신러닝 모델

overlay_status=0

# 오버레이 이미지를 불러오기
image_right_eye = cv2.imread('./images/right_eye.png', cv2.IMREAD_UNCHANGED)
image_left_eye = cv2.imread('./images/left_eye.png', cv2.IMREAD_UNCHANGED)
image_nose = cv2.imread('./images/nose.png', cv2.IMREAD_UNCHANGED)

image_fox_right_eye = cv2.imread('./images/fox_right_eye.png', cv2.IMREAD_UNCHANGED)
image_fox_left_eye = cv2.imread('./images/fox_left_eye.png', cv2.IMREAD_UNCHANGED)
image_fox_nose = cv2.imread('./images/fox_nose.png', cv2.IMREAD_UNCHANGED)

def overlay(image, x, y, w, h, overlay_image): # 오버레이(위에 덧씌우는)하는 함수
                                               #image: 오버레이할 대상이 되는 원본 이미지
                                               # x, y: 오버레이할 위치의 왼쪽 위 모서리의 x, y 좌표
                                               # w, h: 오버레이할 이미지의 너비,높이
                                               #overlay_image: 위에 덧씌울 이미지 이 이미지는 투명도 정보가 포함된 PNG 형식임
    try:
        alpha = overlay_image[:, :, 3] / 255.0  #투명도 채널을 읽어서 0에서 1 사이의 값으로 정규화
        mask_image = cv2.merge([alpha, alpha, alpha]) #투명도를 RGB 채널 형태로 변환하여 
        image_roi = image[y-h:y+h, x-w:x+w]  #원본 이미지에서 오버레이할 영역을 잘라내어 image_roi에 저장
        if image_roi.shape[0] > 0 and image_roi.shape[1] > 0: 
            overlay_image_resized = cv2.resize(overlay_image, (image_roi.shape[1], image_roi.shape[0])) #overlay_image를 image_roi의 크기로 조정하여 크기를 맞춤
            if image_roi.shape[:2] == overlay_image_resized.shape[:2]: #잘라낸 영역과 조정된 오버레이 이미지의 크기가 같은지 확인
                for c in range(0, 3):
                    image_roi[:, :, c] = (overlay_image_resized[:, :, c] * mask_image[:, :, c] +
                                          image_roi[:, :, c] * (1.0 - mask_image[:, :, c])) # 오버레이 이미지의 투명한 부분만 원본 이미지에 적용, 나머지 부분은 원본 이미지가 그대로 유지되도록 조정
                image[y-h:y+h, x-w:x+w] = image_roi # 합성된 이미지를 원본 이미지의 해당 위치에 다시 할당
    except Exception as e:
        pass



def generate_frames():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7) as face_detection: #얼굴 감지를 수행하는 객체 face_detection을 생성
        while True:
            success, image = cap.read() #한 프레임씩 읽어옴
            if not success: #success가 false면 
                break #종료
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) #이미지 좌우반전, bgr-> rbg로 변환 후 image에 저장
            image.flags.writeable = False
            results = face_detection.process(image) #얼굴 감지 객체 사용해서 결과를 result에 저장
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #rbg -> bgr로 변환

            if results.detections: #results에 얼굴이 인식되었을때만 실행
                for detection in results.detections:
                    keypoints = detection.location_data.relative_keypoints
                    left_eye = keypoints[0]
                    right_eye = keypoints[1]
                    nose_tip = keypoints[2]
                    h, w, _ = image.shape
                    right_eye = (int(right_eye.x * w) + 20, int(right_eye.y * h) - 100) #각 특징점을 픽셀단위로 변환
                    left_eye = (int(left_eye.x * w) - 20, int(left_eye.y * h) - 100)
                    nose_tip = (int(nose_tip.x * w), int(nose_tip.y * h))
                    if  overlay_status==1:
                        overlay(image, *right_eye, 50, 50, image_right_eye)
                        overlay(image, *left_eye, 50, 50, image_left_eye)
                        overlay(image, *nose_tip, 150, 50, image_nose)

                    elif  overlay_status==2:
                        overlay(image, *right_eye, 50, 50, image_fox_right_eye)
                        overlay(image, *left_eye, 50, 50, image_fox_left_eye)
                        overlay(image, *nose_tip, 150, 50, image_fox_nose)

            _ , buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
