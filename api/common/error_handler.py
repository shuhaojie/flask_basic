from typing import Dict
from flask import jsonify
from api.log import logger


class CodeStatus:
    SUC = 2_00_00_00  # success
    ERR = 4_00_00_00  # client error
    EXC = 5_00_00_00  # internal exception


class CodeBusiness:
    DEFAULT = 0
    # BUSINESS_NAME = 1_00_00


class CodeOperation:
    DEFAULT = 0
    CREATE = 1_00
    READ = 2_00
    UPDATE = 3_00
    DELETE = 4_00
    RECREATE = 5_00
    SYNC = 6_00  # sync create task
    MISS = 7_00
    INVALID = 8_00
    REVOKE = 9_00
    EXPIRE = 10_00
    UPLOAD = 11_00


class CodeAny:
    DEFAULT = 0
    TASK = 1
    LIST = 2  # list page
    MQ = 3  # message queue
    SERVICE = 4  # downstream service
    JWT = 5  # json web token
    FILE = 6
    SCHEMA = 7  # marshmallow schema
    AUTH = 8  # user's auth
    URL = 10  # request url


class Base:
    Code = CodeStatus.EXC + CodeBusiness.DEFAULT + CodeOperation.DEFAULT + CodeAny.DEFAULT
    Status = 500
    Message = '服务器内部错误或网络错误'

    def __init__(self):
        self.code = self.Code
        self.message = self.Message
        self.status = self.Status

    def asdict(self):
        return dict(code=self.Code, status=self.Status, message=getattr(self, 'message', self.Message))


class ServerException(Base):
    pass


class APIException(Exception, Base):
    def __init__(self, message: str = '', errors: Dict = None):
        self.message = message or self.Message
        self.errors = errors or {}

    def __str__(self):
        return self.message

    def to_response(self):
        _response = self.asdict()
        _response['errors'] = self.errors
        return _response, self.Status


class DataCommitException(APIException, ServerException):
    Status = 400
    Message = "数据库写入失败"


class MathException(APIException, ServerException):
    Status = 400
    Message = "数据库写入失败"


class MessageException(APIException, ServerException):
    """
    错误异常信息
    """

    data = None
    Code = 4_00_00_11

    def asdict(self):
        res = dict(code=self.Code, status=500, message=getattr(self, "message", self.Message))
        if self.data:
            res.update(data=self.data)
        return res


def register_error_handler(app):
    @app.errorhandler(DataCommitException)
    def data_commit_error(err: DataCommitException):
        logger.exception(str(err))
        return jsonify(err.asdict())

    @app.errorhandler(MessageException)
    def message_exception(err: MessageException):
        logger.warning(err.message)
        return jsonify(err.asdict())
