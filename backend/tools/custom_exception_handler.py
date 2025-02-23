from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging
import traceback

# 로거 설정: 프로젝트의 로깅 설정에 맞춰 로거를 설정합니다.
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    사용자 정의 예외 처리기. 발생한 예외에 대한 정보를 로깅하고,
    클라이언트에게 구체적인 에러 메시지를 반환합니다.
    """
    # 기본 예외 처리기 사용하여 예외 처리
    response = exception_handler(exc, context)
    
    # 예외 처리 후 response가 None이 아니라면, 예외 처리 결과가 있다는 의미
    if response is not None:
        # 예외 정보를 로깅
        logger.error(f"Exception occurred: {str(exc)}", exc_info=True)

        # 스택 트레이스도 함께 로깅하여 디버깅에 도움을 줍니다.
        logger.error("Stack Trace: %s", traceback.format_exc())

        # 서버 오류(500) 처리: 클라이언트에게 간단한 메시지를 제공하되, 개발자는 스택 트레이스를 통해 문제를 파악할 수 있도록 합니다.
        if response.status_code == 500:
            response.data = {
                "error": "500 Internal Server Error",
                "message": "An unexpected error occurred. Please try again later.",
                "details": str(exc),  # 예외의 간단한 설명
                "stack_trace": traceback.format_exc()  # 서버에서 발생한 예외의 스택 트레이스를 반환
            }
        
        # 클라이언트 오류(404) 처리: 해당 리소스를 찾을 수 없는 경우
        elif response.status_code == 404:
            response.data = {
                "error": "404 Not Found",
                "message": "The requested resource could not be found. Please check the URL or resource ID."
            }
        
        # 잘못된 요청(400) 처리: 클라이언트 요청에 문제가 있을 때
        elif response.status_code == 400:
            response.data = {
                "error": "400 Bad Request",
                "message": "There was an issue with the request. Please check the data sent."
            }
        
        # 인증 오류(401) 처리: 인증이 필요한 요청에 인증 정보가 없을 때
        elif response.status_code == 401:
            response.data = {
                "error": "401 Unauthorized",
                "message": "You are not authorized to access this resource. Please check your authentication credentials."
            }

    # 기본 응답 또는 커스터마이즈된 응답을 반환합니다.
    return response