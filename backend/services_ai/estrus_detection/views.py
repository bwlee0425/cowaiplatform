from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
import os
import logging
from services_ai.models import CowEstrusData
from .serializers import CowEstrusSerializer
from .inference import EstrusDetector, PyTorchEstrusHandler, run_estrus_inference

logger = logging.getLogger(__name__)

class EstrusDetectionView(generics.GenericAPIView):
    serializer_class = CowEstrusSerializer
    
    def get_queryset(self):
        return CowEstrusData.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            # Serializer로 요청 데이터 검증
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 모델 경로 설정 (가중치만 저장된 파일 사용)
            model_path = os.path.join(settings.VARIABLE_ROOT, 'shared', 'aimodels', 'estrus_model_v1.pth')
            if not os.path.exists(model_path):
                model_path = os.path.join(settings.BASE_DIR, 'shared', 'aimodels', 'estrus_model_v1.pth')
                if not os.path.exists(model_path):
                    logger.error(f"Model file not found at {model_path}")
                    return Response({"error": f"Model file not found at {model_path}"}, status=500)

            logger.info(f"Received data: {serializer.validated_data}")

            # 모델 로드 및 예측 (CCTV 대신 더미 데이터로 테스트)
            detector = EstrusDetector(model_path, PyTorchEstrusHandler())
            prediction = detector.detect()  # 더미 데이터는 inference.py에서 처리

            # 예측 결과 반환
            return Response({"prediction": prediction.tolist()})

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return Response({"error": f"Prediction failed: {str(e)}"}, status=500)

    def get(self, request, *args, **kwargs):
        # 소 ID로 필터링된 데이터 조회 (기존 유지)
        cow_id = request.query_params.get('cow_id', None)
        if cow_id:
            queryset = self.get_queryset().filter(cow_id=cow_id)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def estrus_prediction(request):
    if request.method == "POST":
        # 더미 데이터로 간소화 (CCTV 로직 제거)
        model_path = os.path.join(settings.VARIABLE_ROOT, 'shared', 'aimodels', 'estrus_model_v1.pth')
        if not os.path.exists(model_path):
            model_path = os.path.join(settings.BASE_DIR, 'shared', 'aimodels', 'estrus_model_v1.pth')
        result = run_estrus_inference()
        return Response({"prediction": result.tolist()})
    return Response({"error": "POST 요청만 지원됩니다."}, status=400)