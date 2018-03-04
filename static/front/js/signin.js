$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var telephone = $("input[name=telephone]").val();
        var password = $("input[name=password]").val();
        var remember = $("input[name=remember]").is(":checked")?1:0;
        csrfajax.post({
            'url': '/signin/',
            'data': {
                'telephone':telephone,
                'password': password,
                'remember': remember
            },
            'success':function (data) {
                if (data['code'] == 200){
                    var return_to = $("#return-to-span").text();
                        if (return_to){
                            window.location = return_to;
                        }else {
                            window.location = '/';
                    }
                }else {
                    swalert.alertInfo(data['msg'])
                }
            },
            'fail': function (error) {
                swalert.alertError('网络错误')
            }
        });
    });
});