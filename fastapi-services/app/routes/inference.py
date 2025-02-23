# 필요한 모듈 임포트
from fastapi import FastAPI, HTTPException  # FastAPI와 예외 처리 클래스
import torch  # PyTorch 라이브러리
import torch.nn as nn  # PyTorch 신경망 모듈
import os  # 파일 경로 처리를 위한 모듈

# FastAPI 애플리케이션 인스턴스 생성
# 이 객체는 API 엔드포인트를 정의하고 HTTP 요청을 처리
app = FastAPI()

# 프로젝트 루트 디렉토리 기준으로 모델 파일 경로 설정
# __file__: 현재 파일(inference.py)의 경로
# os.path.dirname 3번: routes -> app -> fastapi-services -> project 루트로 이동
# 최종 경로: project/shared/aimodels/estrus_model_v1.pth
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(base_dir, 'shared', 'aimodels', 'estrus_model_v1.pth')

# 간단한 예시 모델 클래스 정의
# 실제 모델 구조는 학습 시 사용된 클래스와 동일해야 함
# 여기서는 3개의 입력을 받아 1개의 출력을 생성하는 선형 모델 가정
class EstrusModel(nn.Module):
    def __init__(self):
        super(EstrusModel, self).__init__()
        self.linear = nn.Linear(3, 1)  # 입력 3, 출력 1의 선형 변환
    
    def forward(self, x):
        return self.linear(x)  # 입력 x에 대해 선형 변환 수행

# 모델 초기화 및 로드
try:
    # 모델 인스턴스 생성
    model = EstrusModel()
    # 저장된 가중치를 로드하여 모델에 적용
    # map_location='cpu'는 GPU 없이 CPU에서 로드하도록 설정
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    # 평가 모드로 전환
    # 학습(training)이 아닌 추론(inference)만 수행 (Dropout, BatchNorm 비활성화)
    model.eval()
except FileNotFoundError:
    raise RuntimeError(f"모델 파일을 찾을 수 없습니다: {model_path}")
except Exception as e:
    raise RuntimeError(f"모델 로드 중 오류 발생: {e}")

# "/infer" 경로에 GET 요청을 처리하는 엔드포인트 정의
# 쿼리 파라미터로 입력 데이터를 받음 (예: /infer?data=1.0,2.0,3.0)
@app.get("/infer")
def infer(data: str):
    """
    클라이언트 요청을 받아 모델 추론을 수행하고 결과를 반환하는 함수
    :param data: 쉼표로 구분된 입력 데이터 문자열 (예: "1.0,2.0,3.0")
    :return: 모델 예측 결과를 포함한 JSON 응답
    """
    try:
        # 입력 데이터를 쉼표로 분리하고 float 리스트로 변환
        input_list = [float(x) for x in data.split(",")]
        # 입력 데이터가 3개인지 확인 (모델이 기대하는 입력 크기)
        if len(input_list) != 3:
            raise ValueError("입력 데이터는 정확히 3개의 숫자여야 합니다.")
        
        # 리스트를 PyTorch 텐서로 변환
        # torch.tensor는 float32 타입으로 변환하며, 모델 입력으로 사용 가능
        input_data = torch.tensor(input_list, dtype=torch.float32)
        
        # 모델 추론 수행
        # torch.no_grad(): 추론 시 그래디언트 계산 비활성화 (메모리 절약 및 속도 향상)
        with torch.no_grad():
            output = model(input_data)
        
        # 결과를 JSON 형태로 반환
        # output.item()은 텐서에서 단일 스칼라 값을 추출
        return {"output": output.item()}
    
    except ValueError as ve:
        # 입력 데이터 형식이 잘못된 경우 HTTP 400 에러 반환
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # 기타 예외 발생 시 HTTP 500 에러 반환
        raise HTTPException(status_code=500, detail=f"추론 중 오류 발생: {e}")