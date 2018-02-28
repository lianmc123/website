from flask import jsonify


class HttpCode(object):
    ok = 200
    unauth_error = 401
    params_error = 400
    server_error = 500


def restful_result(code=200, msg="", data={}):
    return jsonify({"code": code, "msg": msg, "data": data})


def success(msg="", data={}):
    return restful_result(data=data, code=HttpCode.ok, msg=msg)


def unauth_error(msg=""):
    return restful_result(code=HttpCode.unauth_error, msg=msg)


def params_error(msg=""):
    return restful_result(code=HttpCode.params_error, msg=msg)


def server_error(msg=""):
    return restful_result(code=HttpCode.server_error, msg=msg or "服务器内部错误")
