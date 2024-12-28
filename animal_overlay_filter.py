import cv2
import mediapipe as mp
from image_overlay import overlay

mp_face_detection = mp.solutions.face_detection

overlay_status=0


cat_right_ear = cv2.imread('./images/cat_right_ear.png', cv2.IMREAD_UNCHANGED)
cat_left_ear = cv2.imread('./images/cat_left_ear.png', cv2.IMREAD_UNCHANGED)
cat_nose = cv2.imread('./images/cat_nose.png', cv2.IMREAD_UNCHANGED)

fox_right_ear = cv2.imread(None, cv2.IMREAD_UNCHANGED)  # TODO: 여우 오른쪽 귀 이미지 경로를 None에 지정하세요.   './images/fox_right_ear.png'
fox_left_ear = cv2.imread(None, cv2.IMREAD_UNCHANGED)   # TODO: 여우 왼쪽 귀 이미지 경로를 None에 지정하세요.     './images/fox_left_ear.png'
fox_nose = cv2.imread(None, cv2.IMREAD_UNCHANGED)       # TODO: 여우 코 이미지 경로를 None에 지정하세요.          './images/fox_nose.png'



def generate_frames():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7) as face_detection:
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
                    if  overlay_status==1:
                        overlay(image, *right_eye, 50, 50, cat_right_ear)
                        overlay(image, *left_eye, 50, 50, cat_left_ear)
                        overlay(image, *nose_tip, 150, 50, cat_nose)

                    elif  overlay_status==2:

                        # TODO: 오버레이할 이미지를 None에 지정하세요 : fox_right_ear , fox_left_ear , fox_nose
                        overlay(image, *right_eye, 50, 50, None)
                        overlay(image, *left_eye, 50, 50, None)
                        overlay(image, *nose_tip, 150, 50, None)

            _ , buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
