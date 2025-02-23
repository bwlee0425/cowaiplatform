import sys
import os

# 트리를 타고 올라서 만나는 곳을 현재경로로 설정해줘야함.
# 환경변수 설정해줬는데 왜 안되는지 모르겠음
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import settings

print(settings.BASE_DIR)

from django.conf import settings

print(settings.VARIABLE_ROOT)

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"  # 프로젝트의 settings.py 경로
from django.conf import settings
import django
django.setup()  # Django 환경 초기화

model_path = os.path.join(settings.VARIABLE_ROOT)
print(model_path)


# 장고실행환경, python manage.py shell 안에서만 가능
from django.conf import settings
import os

model_path = os.path.join(settings.VARIABLE_ROOT, 'SHARED\\MODELS', 'estrus_model_v1.pth')

print(model_path)

print(settings.VARIABLE_ROOT)