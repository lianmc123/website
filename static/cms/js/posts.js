$(function () {
    $("input[name=my-checkbox]").on('switchChange.bootstrapSwitch', function (event, state) {
        var self = $(this);
        var tr = self.parent().parent().parent().parent();
        var post_id = tr.attr("data-id");
        csrfajax.post({
            'url': '/cms/spost/',
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    window.location.reload()
                } else {
                    $(this).parent().parent().attr('checked', false);
                    swalert.alertInfo(data['msg'])
                }
            },
            'fail': function (error) {
                $(this).parent().parent().attr('checked', false);
                swalert.alertErrorToast("网络错误")
            }
        });
    });
});

$(function () {
    $(".edit-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = tr.attr("data-highlight");
        var url = '';
        if (highlight == 1) {
            url = '/cms/uhpost/';
        } else {
            url = '/cms/hpost/';
        }
        csrfajax.post({
            'url': url,
            'data': {
                'post_id': post_id,
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    swalert.alertSuccessToast("操作成功");
                    setTimeout(function () {
                        window.location.reload();
                    }, 500);
                } else {
                    swalert.alertInfo(data['msg']);
                }
            },
            'fail': function (error) {
                swalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $(".delete-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        swalert.alertConfirm({
            'msg': "确定删除?",
            'confirmCallback': function () {
                csrfajax.post({
                    'url': '/cms/dpost/',
                    'data': {
                        'post_id': post_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            swalert.alertInfo(data['msg']);
                        }
                    },
                    'fail': function (error) {
                        swalert.alertErrorToast("网络错误");
                    }
                });
            }
        });
    });
});