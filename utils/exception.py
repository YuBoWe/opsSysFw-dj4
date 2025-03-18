from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class MyException(APIException):
    status_code = 1000
    message = '未知错误，请联系管理员，电话13598263357'

    @classmethod
    def get_message(cls):
        return {'code': cls.status_code, 'message': cls.message}


class InvalidPassword(MyException):
    status_code = 101
    message = '密码错误，请重新输入'


class DoseNotExistException(MyException):
    status_code = 1001
    message = 'Employee matching query does not exist.'


class AttributeError(MyException):
    status_code = 103
    message = '对应的处理handler不存在'


class InvalidToken(MyException):
    status_code = 1003
    message = '登录超时，请重新登录'


class AuthenticationFailed(MyException):
    status_code = 1004
    message = '用户名或者密码错误或者该用户未激活，请重新登录'


class NotAuthenticated(MyException):
    status_code = 1005
    message = "用户未登录，请用户登录"


exp_map = {
    ### 异常类型: custom异常类
    'DoesNotExist': DoseNotExistException,
    'AttributeError': AttributeError,
    'InvalidToken': InvalidToken,
    'AuthenticationFailed': AuthenticationFailed,
    'NotAuthenticated': NotAuthenticated,
}


# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)
#
#     print(response)
#     print(exc, type(exc))
#     print(exc.__class__.__name__)
#
#     # Now add the HTTP status code to the response.
#     # if response is not None:
#     #     response.data['status_code'] = response.status_code
#     message = exp_map.get(exc.__class__.__name__, MyException).get_message()
#
#     return Response(message, status=200)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    print('~~~~~~~~~~~~')
    print(exc, exc.__class__.__name__, context)
    print('~~~~~~~~~~~~')
    if isinstance(exc, MyException):
        message = exc.get_message()
    else:
        message = exp_map.get(exc.__class__.__name__, MyException).get_message()

    return Response(message)
