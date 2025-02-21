import torch  # PyTorch 라이브러리 임포트
import torch.nn as nn  # 신경망 관련 모듈 임포트

# 1️⃣ 간단한 신경망 모델 정의 (더미 모델)
class DummyModel(nn.Module):  
    def __init__(self):
        super().__init__()  # 부모 클래스(nn.Module) 초기화
        self.fc = nn.Linear(3, 1)  # 입력 크기: 3, 출력 크기: 1인 완전연결층 (FC 레이어)

    def forward(self, x):  
        return self.fc(x)  # 입력 데이터를 FC 레이어에 통과시켜 출력 반환

# 2️⃣ 모델 객체 생성
model = DummyModel()

# 3️⃣ 모델 저장 (.pth 파일로 저장)
torch.save(model, "backend/services/estrus_detection/models/estrus_model.pth")

"""코드 설명
1️⃣ DummyModel 클래스 정의
torch.nn.Module을 상속하여 신경망 모델을 만듭니다.
__init__ 함수에서 **완전연결층 (nn.Linear)**을 정의합니다.
forward 함수에서 입력 데이터를 완전연결층을 거쳐 출력합니다.
2️⃣ 모델 인스턴스 생성 및 저장
DummyModel() 객체를 생성합니다.
torch.save()를 사용하여 모델을 "backend/services/estrus_detection/models/estrus_model.pth" 경로에 저장합니다."""

"""추가 설명
✔ nn.Linear(3,1)의 의미

python
self.fc = nn.Linear(3, 1)

입력 노드(특징) 개수: 3
출력 노드 개수: 1
즉, 이 모델은 입력값 3개를 받아 하나의 값을 출력하는 선형 모델입니다.
예를 들어, x = [1.2, 0.5, -0.3] 같은 입력 벡터를 받으면 이를 하나의 값으로 변환하는 역할을 합니다.

✔ torch.save(model, "경로")의 의미
python
torch.save(model, "backend/services/estrus_detection/models/estrus_model.pth")

모델 객체를 파일(.pth)로 저장하는 함수입니다.
나중에 이 모델을 다시 로드하여 사용할 수 있습니다.

🔥 이 코드가 실제로 쓰이는 곳?
학습된 모델 저장 더 큰 모델을 학습한 후, .pth 파일로 저장하여 배포할 수 있음.
추론(Inference) 용도 저장된 모델을 로드한 후 새로운 데이터를 입력하여 예측 가능.
모델 버전 관리 모델의 체크포인트를 저장하여, 특정 버전으로 쉽게 되돌릴 수 있음.

💡 하지만 이 코드에서는 학습이 포함되지 않고, 단순히 모델을 정의하고 저장하는 역할만 합니다.
실제 사용할 때는 데이터를 학습시키고, 가중치를 저장해야 의미가 있습니다.

🚀 결론
이 코드는 PyTorch에서 기본적인 신경망 모델을 정의하고 저장하는 코드입니다.
다만, 학습 과정이 없으므로 나중에 모델을 다시 불러와 학습시키거나 평가하는 코드가 필요합니다! 😊"""