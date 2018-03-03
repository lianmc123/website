$(function () {
    $("#graph-captcha").click(function (event) {
        imgE = $("#graph-captcha-img");
        var url = imgE.attr("src").split("?")[0] + "?" + Math.random();
        // imgE.attr("src", "");
        imgE.attr("src", url);
    });
    $("#sms-captcha-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        telephone = $("input[name=telephone]").val();
        if(!(/^1[345789]\d{9}$/.test(telephone))){
            swalert.alertInfoToast('请填入正确的手机号码!');
            return;
        }

        csrfajax.get({
            'url': '/c/sms_captcha?telephone=' + telephone,
            'success': function (data) {
                if(data['code'] == 200){
                    swalert.alertSuccessToast("短信验证码发送成功");
                    self.attr('disabled', 'disabled');
                    var timeCount = 60;
                    var timer = setInterval(function () {
                        timeCount--;
                        self.text(timeCount);
                        if(timeCount <= 0){
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text("获取验证码");
                        }
                    }, 1000);
                }else {
                    swalert.alertInfoToast(data['msg'])
                }
            },
            'fail': function (error) {
                console.log(error)
            }
        });
    });
});