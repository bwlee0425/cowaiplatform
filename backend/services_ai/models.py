from django.db import models

#암소 발정 데이터 관련 DB 스키마 정의
class CowEstrusData(models.Model):
    cow_id = models.CharField(max_length=50)  # 암소 ID
    temperature = models.FloatField(null=True, blank=True)  # 체온 (선택적)
    activity_level = models.FloatField(null=True, blank=True)  # 활동량 (선택적)
    detected_at = models.DateTimeField(auto_now_add=True)  # 기록 시간
    is_estrus = models.BooleanField(null=True)  # 발정 여부 (AI 예측 결과)
    cctv_source = models.CharField(max_length=255, null=True, blank=True)  # CCTV 데이터 출처 (URL 또는 파일 경로)

    class Meta:
        db_table = 'cow_estrus_data'  # 테이블 이름 지정 (선택 사항)

    def __str__(self):
        return f"Cow {self.cow_id} - {self.detected_at}"