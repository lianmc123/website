import uuid
import datetime
import hmac
import base64
import requests
from urllib.parse import quote
import logging


# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
# ACCESS_KEY_ID = config.ALIDAYU_APP_KEY
#
# ACCESS_KEY_SECRET = config.ALIDAYU_APP_SECRET


class AliYunSMS(object):
    APP_KEY_FIELD = 'ALIDAYU_APP_KEY'
    APP_SECRET_FIELD = 'ALIDAYU_APP_SECRET'
    SMS_SIGN_NAME_FIELD = 'ALIDAYU_SIGN_NAME'
    SMS_TEMPLATE_CODE_FIELD = 'ALIDAYU_TEMPLATE_CODE'

    def __init__(self, app=None):
        self.format = "JSON"
        self.version = "2017-05-25"
        # self.key = ACCESS_KEY_ID
        # self.secret = ACCESS_KEY_SECRET
        self.signature = ""
        self.signature_method = "HMAC-SHA1"
        self.signature_version = "1.0"
        self.signature_nonce = str(uuid.uuid4())
        self.timestamp = datetime.datetime.utcnow().isoformat("T")
        self.region_id = "cn-hangzhou"

        self.gateway = "http://dysmsapi.aliyuncs.com/"
        self.action = ""
        self.params = {}
        self.phone = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        config = app.config
        try:
            self.key = config[self.APP_KEY_FIELD]
            self.secret = config[self.APP_SECRET_FIELD]
            self.sign = config[self.SMS_SIGN_NAME_FIELD]
            self.template = config[self.SMS_TEMPLATE_CODE_FIELD]
        except Exception as e:
            logging.error(e.args)
            raise ValueError('请填写正确的阿里大鱼配置！')

    def send_single(self, phone, params):
        self.action = "SendSms"
        self.phone = phone
        self.params = params
        query_string = self.build_query_string()

        resp = requests.get(self.gateway + "?" + query_string)
        resp = resp.json()
        try:
            if resp['Code'] == 'OK':
                return resp
            else:
                print('=' * 10)
                print("阿里大于错误信息：", resp)
                print('=' * 10)
                return False
        except:
            print('=' * 10)
            print("阿里大于错误信息：", resp)
            print('=' * 10)
            return False

    def build_query_string(self):
        query = []
        query.append(("Format", self.format))
        query.append(("Version", self.version))
        query.append(("AccessKeyId", self.key))
        query.append(("SignatureMethod", self.signature_method))
        query.append(("SignatureVersion", self.signature_version))
        query.append(("SignatureNonce", self.signature_nonce))
        query.append(("Timestamp", self.timestamp))
        query.append(("RegionId", self.region_id))
        query.append(("Action", self.action))
        query.append(("SignName", self.sign))
        query.append(("TemplateCode", self.template))
        query.append(("PhoneNumbers", self.phone))
        params = "{"
        for param in self.params:
            params += "\"" + param + "\"" + ":" + "\"" + str(self.params[param]) + "\"" + ","
        params = params[:-1] + "}"
        query.append(("TemplateParam", params))
        query = sorted(query, key=lambda key: key[0])
        query_string = ""
        for item in query:
            query_string += quote(item[0], safe="~") + "=" + quote(item[1], safe="~") + "&"
        query_string = query_string[:-1]
        tosign = "GET&%2F&" + quote(query_string, safe="~")
        secret = self.secret + "&"
        hmb = hmac.new(secret.encode("utf-8"), tosign.encode("utf-8"), "sha1").digest()
        self.signature = quote(base64.standard_b64encode(hmb).decode("ascii"), safe="~")
        query_string += "&" + "Signature=" + self.signature
        return query_string


# 可选XML
ALIYUN_API_FORMAT = "JSON"
