import torch
from torch.serialization import add_safe_globals
from torch.nn.modules.linear import Linear
from django.conf import settings
import os
from pathlib import Path
from config.interfaces import AIModelHandler  # 추상 인터페이스
from ..tools.stream_handler import process_stream  # stream_handler 경로 가정
from ..aimodels.estrus_model_v1 import EstrusModelV1  # 기존 EstrusModelV1 가져오기
import redis
from .aimodels.dummy_model import DummyModel

# 프로젝트 루트 기준으로 /shared/aimodels/ 경로 설정
model_path = os.path.join(settings.VARIABLE_ROOT, 'shared', 'aimodels', 'estrus_model_v1.pth')
if not os.path.exists(model_path):
    model_path = os.path.join(settings.BASE_DIR, 'shared', 'aimodels', 'estrus_model_v1.pth')

# EstrusModelV1을 안전 목록에 추가
add_safe_globals([DummyModel, Linear])

class PyTorchEstrusHandler(AIModelHandler):
    """
    PyTorch 기반의 한우 발정 탐지 모델 핸들러.
    AIModelHandler 추상 클래스를 구현하며, EstrusModelV1을 로드하고 예측 수행.
    """

    def __init__(self):
        self.model = None

    def load_model(self, model_path: str):
        """
        주어진 경로에서 PyTorch 모델(EstrusModelV1)을 로드.
        :param model_path: 모델 파일(.pth)의 경로
        :return: 로드된 PyTorch 모델
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")
        
        # DummyModel 생성 후 가중치 로드
        self.model = DummyModel()
        state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)  # CPU로 로드 가능하도록 설정
        self.model.load_state_dict(state_dict)  # 모델 가중치 로드
        self.model.eval()  # 평가 모드로 설정
        return self.model

    def predict(self, data=None, temperature=None, activity_level=None, cctv_data=None):
        """
        입력 데이터를 기반으로 발정 여부를 예측.
        :param data: 입력 데이터 (리스트 또는 텐서)
        :param temperature: 온도 데이터 (선택적)
        :param activity_level: 활동 수준 데이터 (선택적)
        :param cctv_data: CCTV 스트림 URL 또는 데이터 (선택적)
        :return: 모델 예측 결과
        """
        if not self.model:
            raise RuntimeError("모델이 로드되지 않았습니다. 먼저 load_model을 호출하세요.")

        # CCTV 데이터가 있으면 전처리
        # if cctv_data:
        #     if isinstance(cctv_data, str):  # URL로 가정
        #         data = self._preprocess_cctv_from_stream(cctv_data)
        #     else:
        #         data = self._preprocess_cctv(cctv_data)

        if data is None:
            #raise ValueError("예측을 위해 data 또는 cctv_data가 필요합니다.")
            data = torch.tensor([[1.0, 2.0, 3.0]], dtype=torch.float32)  # 임시 더미 데이터

        if not isinstance(data, torch.Tensor):
            data = torch.tensor(data, dtype=torch.float32)

        with torch.no_grad():
            return self.model(data)  # EstrusModelV1의 forward 호출

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
        import cv2
        frame = cv2.resize(frame, (224, 224))  # 모델 입력 크기
        frame = frame / 255.0  # 정규화
        return torch.tensor(frame, dtype=torch.float32).permute(2, 0, 1)  # [C, H, W]


class EstrusDetector:
    """
    한우 발정 탐지 시스템의 핵심 클래스.
    """

    def __init__(self, model_path: str, handler: AIModelHandler):
        self.handler = handler
        self.model = self.handler.load_model(model_path)

    def detect(self, data=None, temperature=None, activity_level=None, cctv_data=None):
        """
        입력 데이터를 분석하여 발정 여부 예측.
        """
        return self.handler.predict(data, temperature, activity_level, cctv_data)


def run_estrus_inference(data=None, cctv_data=None, temperature=None, activity_level=None):
    """
    기존 run_estrus_inference 함수를 새 구조에 맞게 구현.
    :param data: 입력 데이터
    :param cctv_data: CCTV 데이터
    :param temperature: 온도 데이터
    :param activity_level: 활동 수준 데이터
    :return: 예측 결과
    """
    handler = PyTorchEstrusHandler()
    detector = EstrusDetector(model_path, handler)
    # result = detector.detect(data=data, cctv_data=cctv_data, temperature=temperature, activity_level=activity_level)
    # return result
    return detector.detect(data=data, cctv_data=cctv_data, temperature=temperature, activity_level=activity_level)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def predict(self, temperature=None, activity_level=None, cctv_data=None):
    cache_key = f"estrus:{temperature}:{activity_level}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return cached_result.decode('utf-8')
    result = self.model.predict(temperature, activity_level, cctv_data)
    redis_client.setex(cache_key, 3600, result)  # 1시간 캐싱
    return result

# 사용 예시
if __name__ == "__main__":
    # 예시 입력 데이터
    input_data = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]  # EstrusModelV1 입력 크기 맞춤
    result = run_estrus_inference(data=input_data)
    print(f"예측 결과: {result}")