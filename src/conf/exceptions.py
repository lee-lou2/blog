import enum
from types import DynamicClassAttribute

from rest_framework import exceptions
from rest_framework.views import exception_handler


class ErrorCode(enum.Enum):
    """오류 코드"""

    DEFAULT_ERROR = ("0000000", 500, "기본 에러")

    def to_exception(self, show_detail: bool = True):
        """Exception 으로 전환"""
        error_code, status_code, detail = self.value
        return ErrorCodeException(
            error_code=error_code,
            status_code=status_code,
            detail=detail if show_detail else "",
        )

    @classmethod
    def choices(cls):
        return [(key.value[0], key.name) for key in cls]

    @DynamicClassAttribute
    def error_code(self):
        """오류 코드"""
        return self.value[0]

    @DynamicClassAttribute
    def status_code(self):
        """HTTP 상태 코드"""
        return self.value[1]

    @DynamicClassAttribute
    def message(self):
        """오류 상세"""
        return self.value[2]


class ErrorCodeException(exceptions.APIException):
    """기본 API 오류"""

    def __init__(self, error_code, *args, **kwargs):
        self.error_code = error_code
        self.status_code = kwargs.pop("status_code", 500)
        super().__init__(*args, **kwargs)


def default_exception_handler(exc, context):
    """
    [ 기본 오류 핸들러 ]
    {
        "message": 오류_내용,
        "error_code": 커스텀_오류_코드,
    }
    """
    response = exception_handler(exc, context)
    # 비어있다면 그대로 반환
    if response is None:
        return response

    response.data = {"message": response.data}

    # 오류 코드 추가
    if isinstance(exc, ErrorCodeException):
        error_code = exc.error_code
    else:
        error_code = ErrorCode.DEFAULT_ERROR.error_code

    response.data["error_code"] = error_code
    return response
