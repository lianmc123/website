$(function () {
    var ue = UE.getEditor('container', {
        "serverUrl": '/ueditor/upload/',
        autoHeightEnabled: false,
        autoFloatEnabled: true,
        toolbars: [[  //一行一个数组
            'undo',
            'redo',
            'bold',
            'italic',
            'source',
            'blockquote',
            'selectall',
            'insertcode',
            'fontfamily',
            'fontsize',
            'simpleupload',
            'emotion',
        ]]
    });
    ue.ready(function () {
        ue.setHeight(200);
    });
    $("#comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $('#login-tag').attr('data-is-login');
        if (!loginTag){
            window.location = '/signin/'
        }else {
            var content = ue.getContent();
            var post_id = $('#post-content').attr('data-id');
            csrfajax.post({
                'url': '/acomment/',
                'data': {
                    'content': content,
                    'post_id': post_id
                },
                'success': function (data) {
                    if (data['code'] == 200){
                        window.location.reload()
                    }else {
                        swalert.alertInfo(data['msg'])
                    }
                },
                'fail': function (error) {
                    swalert.alertNetworkError()
                }
            });
        }
    });
});
