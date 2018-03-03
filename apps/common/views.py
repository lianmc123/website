from flask import Blueprint, request
from exts import aliyunsms
from utils import restful
from utils.captcha import Captcha
import random
from .forms import SMSCaptchaForm

bp = Blueprint('common', __name__, url_prefix='/c')


# @bp.route('/sms_captcha/', method=["POST"])
# def sms_captcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(msg="未收到手机号码")
#     # captcha = Captcha.gene_text(number=4)
#     captcha = random.randint(100000, 999999)
#     # if alidayu.send_sms(telephone, code=captcha):
#     #     return restful.success()
#     # else:
#     #     return restful.params_error(msg="发送失败")
#     # result = aliyunsms.sms.send_single(telephone, aliyunsms.ALISMS_SIGN, aliyunsms.ALISMS_TPL_REGISTER,
#     #                                    {"code": captcha})
#     result = aliyunsms.send_single(telephone, {"code": captcha})
#     if result:
#         return restful.success()
#     else:
#         return restful.params_error(msg="发送失败")

@bp.route('/sms_captcha/', methods=["POST"])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = random.randint(100000, 999999)
        result = aliyunsms.send_single(telephone, {"code": captcha})
        if result:
            return restful.success()
        else:
            return restful.params_error(msg="发送失败")
    else:
        return restful.params_error(msg="参数错误")
