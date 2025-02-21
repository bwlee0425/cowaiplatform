import torch
from config.interfaces import AIModelHandler  # 추상 인터페이스를 상속받기 위해 가져옴

class PyTorchEstrusHandler(AIModelHandler):
    """
    PyTorch 기반의 한우 발정 탐지 모델 핸들러.
    AIModelHandler 추상 클래스를 구현하며, PyTorch 모델을 로드하고 예측 수행 기능을 제공함.
    """

    def load_model(self, model_path: str):
        """
        주어진 경로에서 PyTorch 모델을 로드하는 메서드.
        :param model_path: 모델 파일(.pt, .pth)의 경로
        :return: 로드된 PyTorch 모델
        """
        self.model = torch.load(model_path)  # 모델 로드
        return self.model

    def predict(self, data):
        """
        입력 데이터를 기반으로 발정 여부를 예측하는 메서드.
        :param data: 예측을 위한 입력 데이터 (리스트 또는 텐서)
        :return: 모델 예측 결과
        """
        return self.model(torch.tensor(data))  # 모델을 사용하여 예측 수행
    
""" 주요 개념:
PyTorchEstrusHandler는 AIModelHandler의 인터페이스를 구현한 클래스.
load_model(): PyTorch 모델을 지정된 경로에서 로드하여 self.model에 저장.
predict(): 입력 데이터를 텐서로 변환한 후 모델에 전달하여 예측 수행."""

class EstrusDetector:
    """
    한우 발정 탐지 시스템의 핵심 클래스.
    AI 모델 핸들러를 주입받아 유연한 모델 변경이 가능하도록 설계됨.
    """

    def __init__(self, model_path: str, handler: AIModelHandler):
        """
        탐지기 객체를 초기화하는 메서드.
        :param model_path: AI 모델 파일의 경로
        :param handler: AIModelHandler 인터페이스를 구현한 모델 핸들러
        """
        self.handler = handler  # 모델 핸들러 저장
        self.model = self.handler.load_model(model_path)  # 모델 로드

    def detect(self, raw_data):
        """
        입력 데이터를 분석하여 발정 여부를 예측하는 메서드.
        :param raw_data: 예측을 위한 원본 데이터 (리스트 또는 넘파이 배열)
        :return: 예측 결과
        """
        return self.handler.predict(raw_data)  # 모델 핸들러를 통해 예측 실행
    
"""주요개념
EstrusDetector 클래스는 AI 모델을 사용하여 발정을 탐지하는 역할.
__init__():
model_path를 받아 모델을 로드하고,
AIModelHandler 인터페이스를 구현한 핸들러(PyTorchEstrusHandler)를 주입받아 모델을 로드.
detect(): 모델 핸들러를 사용하여 입력 데이터를 기반으로 발정 여부를 예측."""

"""이 코드의 특징 및 장점
인터페이스 기반 설계(OOP 원칙 적용)

AIModelHandler 인터페이스를 만들어서 여러 종류의 AI 모델을 동일한 방식으로 처리 가능.
PyTorchEstrusHandler 외에도 TensorFlowEstrusHandler, ScikitLearnEstrusHandler 등 다양한 구현이 가능함.
유연한 모델 교체 가능

EstrusDetector는 AI 모델의 구체적인 구현(PyTorchEstrusHandler)을 알 필요 없이, AIModelHandler 인터페이스만 사용하여 모델을 다룸.
이를 통해 PyTorch → TensorFlow 등 쉽게 모델을 교체 가능.
테스트 및 확장 용이

AIModelHandler를 Mocking(모의 객체)으로 대체하면, 모델 없이도 탐지기(EstrusDetector)를 테스트할 수 있음.
예를 들어, 테스트용 가짜 모델 핸들러를 만들 수 있음:
python

class MockModelHandler(AIModelHandler):
    def load_model(self, model_path: str):
        return "Mock Model Loaded"

    def predict(self, data):
        return "Mock Prediction"
이를 활용하면 실제 AI 모델 없이도 EstrusDetector의 동작을 검증할 수 있음.

사용 예시
python

# 모델 파일 경로
model_path = "models/estrus_model.pth"

# PyTorch 모델 핸들러 생성
pytorch_handler = PyTorchEstrusHandler()

# 탐지기 객체 생성
detector = EstrusDetector(model_path, pytorch_handler)

# 예측할 데이터
input_data = [0.5, 0.3, 0.8]  # 가상의 발정 관련 입력 데이터

# 발정 탐지 실행
prediction = detector.detect(input_data)
print("Prediction:", prediction)

정리
이 코드는 한우 발정 탐지 시스템을 구축하는 데 필요한 AI 모델 추론 로직을 인터페이스 기반 설계(OOP 원칙 적용) 방식으로 구현한 것입니다.

AIModelHandler는 공통 인터페이스를 제공하여 다양한 AI 모델(PyTorch, TensorFlow, Scikit-Learn)을 손쉽게 교체할 수 있도록 합니다.
PyTorchEstrusHandler는 PyTorch 모델을 로드하고 예측하는 기능을 담당합니다.
EstrusDetector는 모델 핸들러를 받아서 발정 여부를 예측하는 기능을 수행합니다.
💡 이 설계 방식의 장점
✅ 모델 교체가 용이함 → PyTorch 외에도 다른 AI 모델을 쉽게 적용 가능
✅ 코드의 유지보수 및 확장성 향상 → 인터페이스 기반 설계(OOP) 적용
✅ 테스트가 용이함 → Mock 객체 활용 가능

이제 이 구조를 기반으로 다양한 AI 모델을 적용하거나, API에 연동하여 실제 한우 발정 탐지 시스템을 구축할 수 있습니다. 🚀"""


"""실행 흐름
클라이언트가 POST /estrus/ 요청을 보냄
json

{
    "cctv_frame": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
}

EstrusDetectionView.post() 실행
"cctv_frame" 데이터를 추출
EstrusDetector를 이용해 예측 수행

EstrusDetector.detect(raw_data) 실행
PyTorchEstrusHandler.predict()를 호출하여 모델 예측 수행

예측 결과를 JSON 형태로 반환
json

{
    "prediction": [0.9, 0.1]
}

최종정리
urls.py	/estrus/ 엔드포인트를 EstrusDetectionView에 연결
views.py	클라이언트 요청을 받아 모델을 실행하고 예측 결과를 반환
inference.py	PyTorch 모델을 로드하고 데이터를 예측하는 핵심 로직"""