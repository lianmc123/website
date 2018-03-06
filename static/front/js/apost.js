$(function () {
    var ue = UE.getEditor('container',{
        "serverUrl": '/ueditor/upload/',
        autoHeightEnabled: false,
        autoFloatEnabled: true
    });
    ue.ready(function () {
        ue.setHeight(500);
    });
    $("#menu-index").removeClass("menu__item--current");
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleE = $("input[name=title]");
        var title = titleE.val();
        var boardE = $("select[name=board_id]");
        var board_id = boardE.val();
        var content = ue.getContent();

        csrfajax.post({
            'url': '/add_post/',
            'data': {
                'title': title,
                'board_id': board_id,
                'content': content
            },
            'success': function (data) {
                if (data['code'] == 200){
                    swalert.alertConfirm({
                        'msg': '发表成功',
                        'confirmText': '再发一篇',
                        'cancelText': '回到首页',
                        'confirmCallback': function () {
                            titleE.val("");
                            ue.setContent("");
                        },
                        'cancelCallback': function () {
                            window.location = '/';
                        }
                    });
                }else {
                    swalert.alertInfoToast(data['msg']);
                }
            },
            'fail': function (error) {
                swalert.alertNetworkError();
            }
        });
    });
});