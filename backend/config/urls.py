"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import exception_handler
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
import debug_toolbar

# 커스텀 스키마 생성기
class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_endpoints(self, request):
        endpoints = super().get_endpoints(request)
        excluded_paths = ['swagger/', 'redoc/', 'api/schema/', 'swagger2/', 'redoc2/']
        return {path: endpoint for path, endpoint in endpoints.items()
                if not any(excluded in path for excluded in excluded_paths)}

# drf-spectacular의 스키마 엔드포인트
urlpatterns = [
     # OpenAPI 스키마를 생성하는 URL
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger 뷰
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc 뷰
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),
]

# drf-yasg의 스키마 뷰 설정 (다른 이름으로 사용)
swagger_schema_view  = get_schema_view(
    openapi.Info(
        title="CowAi API",
        default_version="v1",
        description="API documentation for CowAi project",
        terms_of_service="https://www.cowaiplatform.com/terms/",
        contact=openapi.Contact(email="support@cowaiplatform.com"),
        license=openapi.License(name="Apache 2.0"),
    ),
    public=True,
    permission_classes=[IsAuthenticated],  # 공개 API라면 AllowAny 사용, 인증이 필요한 경우 IsAuthenticated로 변경
    authentication_classes=[SessionAuthentication, BasicAuthentication],  # 인증 방식 설정
    generator_class=CustomSchemaGenerator,
)

# drf-yasg의 Swagger UI 엔드포인트 (이름을 다르게 해서 중복되지 않게 설정)
urlpatterns += [
    path('swagger2/', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='yasg-swagger-ui'),
    path('redoc2/', swagger_schema_view.with_ui('redoc', cache_timeout=0), name='yasg-redoc-ui'),
]

# 나머지 API 경로 설정
urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'), name='api'),  # api/ 경로를 포함
]

# 개발 환경에서 디버그 툴바와 미디어 파일 제공
if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)