import cv2

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
                for c in range(0, 3): # 블렌딩
                    image_roi[:, :, c] = (overlay_image_resized[:, :, c] * mask_image[:, :, c] +
                                          image_roi[:, :, c] * (1.0 - mask_image[:, :, c])) # 오버레이 이미지의 투명한 부분만 원본 이미지에 적용, 나머지 부분은 원본 이미지가 그대로 유지되도록 조정
                image[y-h:y+h, x-w:x+w] = image_roi # 합성된 이미지를 원본 이미지의 해당 위치에 다시 할당
    except Exception as e:
        pass