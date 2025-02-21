from django.urls import path
from services.estrus_detection.views import EstrusDetectionView

urlpatterns = [
    path('estrus/', EstrusDetectionView.as_view()),  # '/estrus/' 경로로 요청이 들어오면 EstrusDetectionView 실행
]

"""path('estrus/', EstrusDetectionView.as_view()):
/estrus/ 엔드포인트를 설정하고, 요청이 들어오면 EstrusDetectionView 클래스를 실행합니다.
as_view():
APIView 기반 클래스는 Django의 CBV(Class-Based View) 방식이므로 .as_view()를 호출해야 합니다."""