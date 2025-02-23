from django.urls import path
from services_ai.estrus_detection.views import EstrusDetectionView, estrus_prediction

urlpatterns = [
    path('estrus/', EstrusDetectionView.as_view(), name='estrus_detection'),  # 클래스 기반 뷰
    path("estrus/predict/", estrus_prediction, name="estrus_prediction"),     # 함수 기반 뷰
]

"""path('estrus/', EstrusDetectionView.as_view()):
/estrus/ 엔드포인트를 설정하고, 요청이 들어오면 EstrusDetectionView 클래스를 실행합니다.
as_view():
APIView 기반 클래스는 Django의 CBV(Class-Based View) 방식이므로 .as_view()를 호출해야 합니다."""