from rest_framework import serializers
from ..models import CowEstrusData

# 발정 탐지 전용 데이터를 JSON 으로 변환하기 위한 시리얼라이저
class CowEstrusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CowEstrusData
        fields = ['id','cow_id', 'temperature', 'activity_level', 'detected_at', 'is_estrus', 'cctv_source']