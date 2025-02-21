from rest_framework.views import APIView
from rest_framework.response import Response
from .inference import EstrusDetector, PyTorchEstrusHandler

class EstrusDetectionView(APIView):
    def post(self, request):
        raw_data = request.data.get("cctv_frame", [])  # 요청에서 'cctv_frame' 데이터를 가져옴 (기본값: 빈 리스트)
        detector = EstrusDetector("models/estrus_model.pth", PyTorchEstrusHandler())  # 모델 로드
        result = detector.detect(raw_data)  # 모델을 사용해 예측 수행
        return Response({"prediction": result.tolist()})  # 예측 결과를 JSON 형태로 반환

"""EstrusDetectionView(APIView)

Django REST framework의 APIView를 상속받아 RESTful API 엔드포인트를 만듭니다.
post 메서드를 구현하여 POST 요청을 처리합니다.
post(self, request)

클라이언트가 POST /estrus/ 요청을 보낼 때 실행됩니다.
request.data.get("cctv_frame", []):
요청 데이터에서 "cctv_frame" 키의 값을 가져옵니다.
없을 경우 기본값으로 빈 리스트([])를 사용합니다.
detector = EstrusDetector("models/estrus_model.pth", PyTorchEstrusHandler()):
EstrusDetector 객체를 생성하고 models/estrus_model.pth 파일에서 모델을 로드합니다.
result = detector.detect(raw_data):
모델을 사용하여 raw_data(CCTV 프레임) 데이터를 분석합니다.
return Response({"prediction": result.tolist()}):
모델의 예측 결과를 JSON 응답으로 반환합니다."""