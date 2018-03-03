from flask import Blueprint, request
from exts import aliyunsms
from utils import restful
from utils.captcha import Captcha
import random

bp = Blueprint('common', __name__, url_prefix='/c')


@bp.route('/sms_captcha/')
def sms_captcha():
    telephone = request.args.get('telephone')
    if not telephone:
        return restful.params_error(msg="未收到手机号码")
    # captcha = Captcha.gene_text(number=4)
    captcha = random.randint(100000, 999999)
    # if alidayu.send_sms(telephone, code=captcha):
    #     return restful.success()
    # else:
    #     return restful.params_error(msg="发送失败")
    # result = aliyunsms.sms.send_single(telephone, aliyunsms.ALISMS_SIGN, aliyunsms.ALISMS_TPL_REGISTER,
    #                                    {"code": captcha})
    result = aliyunsms.send_single(telephone, {"code": captcha})
    if result:
        return restful.success()
    else:
        return restful.params_error(msg="发送失败")
# {'HostId': 'dysmsapi.aliyuncs.com',
# 'Recommend': 'https://error-center.aliyun.com/status/search?Keyword=SignatureDoesNotMatch&source=PopGw',
# 'RequestId': 'FBDB2AC6-DCD0-4945-A1CC-2FA70F197B37',
# 'Message': 'Specified signature is not matched with our calculation. server string to sign is:GET&%2F&AccessKeyId%3DLTAIfbaYxJm4sWQZ%26Action%3DSendSms%26Format%3DJSON%26PhoneNumbers%3D13680964851%26RegionId%3Dcn-hangzhou%26SignName%3D%25E6%2598%2593%25E7%25A7%2580%25E7%25B1%25B3%26SignatureMethod%3DHMAC-SHA1%26SignatureNonce%3D7ccde86c-3a44-4aa3-bbe4-57041ccdb691%26SignatureVersion%3D1.0%26TemplateCode%3DSMS_126635198%26TemplateParam%3D%257B%2522code%2522%253A%25224519%2522%257D%26Timestamp%3D2018-03-03T07%253A18%253A56.401842%26Version%3D2017-05-25',
# 'Code': 'SignatureDoesNotMatch'}
# {'Message': 'OK',
# 'BizId': '290921020061150923^0',
# 'RequestId': 'F8A2299F-0CF3-4563-820D-22469B047AC1',
# 'Code': 'OK'}
