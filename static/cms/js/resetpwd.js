$(function () {
    $(".btn-primary").click(function (event) {
        // 阻止按钮提交表单
        event.preventDefault();
        var oldpwd = $("input[name=oldpwd]");
        var newpwd = $("input[name=newpwd]");
        var newpwd2 = $("input[name=newpwd2]");
        var oldpwd_value = oldpwd.val();
        var newpwd_value = newpwd.val();
        var newpwd_value2 = newpwd2.val();
        csrfajax.post({
            'url':'/cms/resetpwd/',
            'data':{
                'oldpwd': oldpwd_value,
                'newpwd': newpwd_value,
                'newpwd2': newpwd_value2
            },
            'success': function(data) {
                if (data['code'] == 200){
                    swalert.alertSuccessToast("修改成功");
                    oldpwd.val("");
                    newpwd.val("");
                    newpwd2.val("");
                }else{
                    swalert.alertError(data['msg']);
                }
                console.log(data)
            },
            'fail':function (error) {
                swalert.alertNetworkError();
            }
        });
    });
});