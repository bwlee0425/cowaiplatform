from django.shortcuts import render
from django.http import JsonResponse
from social_django.utils import load_strategy, load_backend

def google_auth(request):
    # 클라이언트에서 받은 토큰
    token = request.data.get("token")

    # backend와 strategy 로드
    strategy = load_strategy(request)
    backend = load_backend(strategy, "google", None)

    # 구글 토큰을 backend로 인증
    user = backend.do_auth(token)

    if user:
        # 인증 성공 시 사용자 정보 반환
        return JsonResponse({"message": "Authenticated", "user": user.username})
    else:
        return JsonResponse({"message": "Authentication failed"}, status=400)