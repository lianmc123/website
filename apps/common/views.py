from flask import Blueprint, request, make_response
from utils.captcha import Captcha
from io import BytesIO
from exts import aliyunsms
from utils import restful
import random
from .forms import SMSCaptchaForm
from utils import web_cache
from tasks import send_sms_captcha

bp = Blueprint('common', __name__, url_prefix='/c')


@bp.route('/sms_captcha/', methods=["POST"])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = random.randint(100000, 999999)
        # result = aliyunsms.send_single(telephone, {"code": captcha})
        # if result:
        #     web_cache.RedisCache().set(telephone, captcha)
        # else:
        #     return restful.params_error(msg="发送失败")
        send_sms_captcha(telephone, captcha)
        web_cache.RedisCache().set(telephone, captcha)
        return restful.success()
    else:
        return restful.params_error(msg="参数错误")


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    web_cache.RedisCache().set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp
