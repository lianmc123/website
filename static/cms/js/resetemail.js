$(function () {
    $("#get-captcha").click(function (event) {
        var email = $("input[name=email]").val();
        if (!email){
            swalert.alertInfoToast("请输入邮箱");
            return ;
        }
        csrfajax.get({
            'url':'/cms/email_captcha/',
            'data':{
                'email':email
            },
            'success':function (data) {
                if (data["code"] == 200){
                    swalert.alertInfo("请到邮箱查看验证码");
                }else {
                    swalert.alertInfo(data['msg']);
                }
            },
            'fail':function (error) {
                swalert.alertError("发生了错误");
            }
        });
    });
    $("#commit-btn").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name=email]");
        var captchaE = $("input[name=captcha]");
        var email = emailE.val();
        var captcha = captchaE.val();
        if (!email){
            swalert.alertInfoToast("请输入邮箱");
            return ;
        }else if (!captcha){
            swalert.alertInfoToast("请输入验证码");
            return ;
        }
        csrfajax.post({
            'url':'/cms/resetemail/',
            'data':{
                'email':email,
                'captcha': captcha
            },
            'success':function (data) {
                if (data["code"] == 200){
                    swalert.alertInfo("修改成功");
                    emailE.val("");
                    captchaE.val("");
                }else {
                    swalert.alertInfo(data['msg']);
                }
            },
            'fail':function (error) {
                swalert.alertNetworkError()
            }
        });
    });
});