import cv2
import mediapipe as mp

def main_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, image = cap.read()
        if not success:
            break
        # 이미지를 수평으로 뒤집고(BGR 색상 공간에서 RGB 색상 공간으로 변환)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # 성능을 향상시키기 위해 이미지의 수정 가능 여부를 False로 설정
        image.flags.writeable = False

        # 이미지를 다시 수정할 수 있도록 설정
        image.flags.writeable = True

        # 이미지를 다시 RGB 색상 공간에서 BGR 색상 공간으로 변환 (OpenCV에서 사용)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # 이미지를 JPEG 형식으로 인코딩하고, 성공 여부를 ret에, 인코딩된 이미지 데이터를 buffer에 저장
        ret, buffer = cv2.imencode('.jpg', image)

        # buffer를 바이트 형태로 변환하여 frame에 저장
        frame = buffer.tobytes()

        # 프레임을 multipart/x-mixed-replace 형식으로 반환
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

