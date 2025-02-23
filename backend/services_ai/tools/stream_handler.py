import cv2

def process_stream(cctv_url):
    cap = cv2.VideoCapture(cctv_url)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # 프레임 처리 (AI 모델로 전달)
        yield frame
    cap.release()

# 옵션 1: 라이브 스트리밍
# 입력: RTSP/HTTP 스트림 URL (예: rtsp://farm-cctv:554/stream).
# 처리: tools/stream_handler.py에서 OpenCV나 GStreamer로 스트림을 받아 프레임 단위로 분석.