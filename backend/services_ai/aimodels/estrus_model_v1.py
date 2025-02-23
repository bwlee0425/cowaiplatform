import torch
import torch.nn as nn
import cv2
import os
from ..tools.stream_handler import process_stream  # 상대 경로로 유틸리티 가져오기

class EstrusModelV1(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Linear(10, 1)  # 예시 구조, 실제 모델로 교체 가능

    def forward(self, x):
        return self.model(x)

    def predict(self, data=None, temperature=None, activity_level=None, cctv_data=None):
        """
        입력 데이터를 기반으로 발정 여부를 예측하는 메서드.
        """
        if cctv_data:
            if isinstance(cctv_data, str):  # URL로 가정
                data = self._preprocess_cctv_from_stream(cctv_data)
            else:
                data = self._preprocess_cctv(cctv_data)

        if data is None:
            raise ValueError("예측을 위해 data 또는 cctv_data가 필요합니다.")

        if not isinstance(data, torch.Tensor):
            data = torch.tensor(data, dtype=torch.float32)

        with torch.no_grad():
            return self.forward(data)

    def _preprocess_cctv_from_stream(self, stream_url):
        processed_data = []
        for frame in process_stream(stream_url):
            frame_data = self._process_frame(frame)
            processed_data.append(frame_data)
        return torch.stack(processed_data)

    def _preprocess_cctv(self, cctv_data):
        processed_data = [self._process_frame(frame) for frame in cctv_data]
        return torch.stack(processed_data)

    def _process_frame(self, frame):
        frame = cv2.resize(frame, (224, 224))  # 모델 입력 크기
        frame = frame / 255.0  # 정규화
        return torch.tensor(frame, dtype=torch.float32).permute(2, 0, 1)  # [C, H, W]

# 모델 인스턴스 생성 및 저장
if __name__ == "__main__":
    model = EstrusModelV1()

    # 프로젝트 루트 기준으로 /shared/aimodels/ 경로 설정
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    model_path = os.path.join(base_dir, 'shared', 'aimodels', 'estrus_model_v1.pth')

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    torch.save(model.state_dict(), model_path)  # 모델 weights만 저장 (권장 방식)
    print(f"모델이 {model_path}에 저장되었습니다.")