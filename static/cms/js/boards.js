$(function () {
   $("#add-board-btn").click(function (event) {
       event.preventDefault();
       swalert.alertOneInput({
           'title':'输入板块名',
           'placeholder': '板块名',
           'confirmCallback': function (inputValue) {
               csrfajax.post({
                   'url': '/cms/aboard/',
                   'data': {
                       'name': inputValue
                   },
                   'success': function (data) {
                       if (data['code'] == 200){
                           window.location.reload();
                       }else {
                           swalert.alertInfo(data['msg']);
                       }
                   },
                   'fail': function (error) {
                       swalert.alertNetworkError();
                   }
               })
           }
       });
   });
});

$(function () {
    $("input[name=my-checkbox]").on('switchChange.bootstrapSwitch', function(event, state) {
        var self = $(this);
        var tr = self.parent().parent().parent().parent();
        var board_id = tr.attr("data-id");
        csrfajax.post({
            'url': '/cms/sboard/',
            'data': {
                'board_id': board_id
            },
            'success': function (data) {
                if (data['code'] == 200){
                    window.location.reload()
                }else {
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
        var board_id = tr.attr("data-id");
        var name = tr.attr("data-name");

        swalert.alertOneInput({
            'title': '请输入新名称',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                csrfajax.post({
                   'url': '/cms/uboard/',
                   'data': {
                       'board_id': board_id,
                       'name': inputValue
                   },
                   'success': function (data) {
                       if (data['code'] == 200){
                           window.location.reload();
                       }else {
                           swalert.alertInfo(data['msg']);
                       }
                   },
                   'fail': function (error) {
                       swalert.alertNetworkError();
                   }
               });
            }
        });
    });
});

$(function () {
    $(".delete-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr("data-id");
        swalert.alertConfirm({
            'msg': "确定删除?",
            'confirmCallback': function () {
                csrfajax.post({
                    'url': '/cms/dboard/',
                    'data': {
                        'board_id': board_id
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