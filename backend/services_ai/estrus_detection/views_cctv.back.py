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

            # 요청 데이터에서 필요한 값 추출
            temperature = serializer.validated_data.get('temperature')
            activity_level = serializer.validated_data.get('activity_level')
            cctv_source = serializer.validated_data.get('cctv_source', None)  # None 허용으로 변경
            
            # 모델 경로 설정
            model_path = os.path.join(settings.VARIABLE_ROOT, 'shared', 'aimodels', 'estrus_model_v1.pth')
            if not os.path.exists(model_path):
                model_path = os.path.join(settings.BASE_DIR, 'shared', 'aimodels', 'estrus_model_v1.pth')
                if not os.path.exists(model_path):
                    logger.error(f"Model file not found at {model_path}")
                    return Response({"error": f"Model file not found at {model_path}"}, status=500)

            logger.info(f"Received data: {serializer.validated_data}")
            # 기존 estrus_prediction 로직 반영
            cctv_url = request.POST.get("cctv_url")  # 기존 코드에서 cctv_url 처리 반영
            if cctv_url:  # cctv_url이 제공된 경우
                result = run_estrus_inference(cctv_data=cctv_url)
                return Response({"prediction": result.tolist()})  # 기존 JsonResponse 스타일 반영

            # CCTV 프레임 데이터가 없는 경우 오류 반환 (기존 로직 유지)
            if not cctv_source and not cctv_url:
                logger.warning("No CCTV frame data or URL provided")
                return Response({"error": "No CCTV frame data or URL provided"}, status=400)

            # 모델 로드 및 예측
            detector = EstrusDetector(model_path, PyTorchEstrusHandler())
            prediction = detector.detect(cctv_data=cctv_source, temperature=temperature, activity_level=activity_level)

            # 예측 보정
            is_estrus = prediction[0] > 0.5 and (temperature or 0) > 38.5 and (activity_level or 0) > 50

            # DB에 예측 결과 저장
            estrus_data = serializer.save(is_estrus=is_estrus)
            response_serializer = self.get_serializer(estrus_data)
            return Response(response_serializer.data)

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return Response({"error": f"Prediction failed: {str(e)}"}, status=500)

    def get(self, request, *args, **kwargs):
        # 소 ID로 필터링된 데이터 조회
        cow_id = request.query_params.get('cow_id', None)
        if cow_id:
            queryset = self.get_queryset().filter(cow_id=cow_id)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])  # HTTP 메서드 명시
# 기존 함수 유지 (호환성을 위해)
def estrus_prediction(request):
    if request.method == "POST":
        cctv_url = request.POST.get("cctv_url")
        if not cctv_url:
            return JsonResponse({"error": "No CCTV URL provided"}, status=400)
        result = run_estrus_inference(cctv_data=cctv_url)
        return Response({"prediction": result.tolist()})
        #return JsonResponse({"prediction": result.tolist()})
    return Response({"error": "POST 요청만 지원됩니다."}, status=400)
    #return JsonResponse({"error": "POST 요청만 지원됩니다."}, status=400)
