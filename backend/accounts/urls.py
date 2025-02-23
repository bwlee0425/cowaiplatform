from django.urls import path
from . import views

urlpatterns = [
    path('google/', views.google_auth, name='google_auth'),  # /auth/google/로 연결
]