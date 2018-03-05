$(function () {
    $("input[name=my-checkbox]").on('switchChange.bootstrapSwitch', function(event, state) {
        // console.log(this); // DOM element
        // console.log(event); // jQuery event
        // console.log(state); // true | false
        var self = $(this);
        console.log(self)
        var tr = self.parent().parent().parent().parent();
        console.log(tr)
        var banner_id = tr.attr("data-id");
        csrfajax.post({
            'url': '/cms/sbanner/',
            'data': {
                'banner_id': banner_id
            },
            'success': function (data) {
                if (data['code'] == 200){
                    window.location.reload()
                }else {
                    swalert.alertInfo(data['msg'])
                }
            },
            'fail': function (error) {
                swalert.alertErrorToast("网络错误")
            }
        });
    });
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var dialog = $("#myModal");
        var name = dialog.find("input[name=name]").val();
        var image_url = dialog.find("input[name=image-url]").val();
        var link_url = dialog.find("input[name=link-url]").val();
        var priority = dialog.find("input[name=priority]").val();
        if (!name || !image_url || !link_url || !priority) {
            swalert.alertInfo("输入信息不完整!");
            return;
        }
        var submitType = $(this).attr('data-type');
        var bannerId = $(this).attr('data-id')
        var url = ''
        if (submitType == 'update'){
            url = '/cms/ubanner/'
        }else {
            url = '/cms/abanner/'
        }
        csrfajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerId
            },
            'success': function (data) {

                if (data['code'] == 200) {
                    window.location.reload();
                    dialog.find("input[name=name]").val("");
                    dialog.find("input[name='image-url']").val("");
                    dialog.find("input[name='link-url']").val("");
                    dialog.find("input[name=priority]").val("");
                } else {
                    swalert.alertInfoToast(data['msg'])
                }
            },
            'fail': function (error) {
                swalert.alertErrorToast("网络错误")
            }
        });

    });
    $(".edit-btn").click(function (event) {
        var dialog = $("#myModal");
        dialog.modal("show");
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image-url");
        var link_url = tr.attr("data-link-url");
        var priority = tr.attr("data-priority");
        dialog.find("input[name=name]").val(name);
        dialog.find("input[name='image-url']").val(image_url);
        dialog.find("input[name='link-url']").val(link_url);
        dialog.find("input[name=priority]").val(priority);
        dialog.find("#save-banner-btn").attr("data-type", 'update');
        dialog.find("#save-banner-btn").attr("data-id", tr.attr("data-id"));
    });
    $("#cancel-btn").click(function (event) {
        var dialog = $("#myModal");
        dialog.find("input[name=name]").val("");
        dialog.find("input[name='image-url']").val("");
        dialog.find("input[name='link-url']").val("");
        dialog.find("input[name=priority]").val("");
    });
    $(".delete-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr("data-id");
        swalert.alertConfirm({
            'msg': "确定删除?",
            'confirmCallback': function () {
                csrfajax.post({
                    'url': '/cms/dbanner/',
                    'data': {
                        'banner_id': banner_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200){
                            window.location.reload()
                        }else {
                            swalert.alertInfo(data['msg'])
                        }
                    },
                    'fail': function (error) {
                        swalert.alertErrorToast("网络错误")
                    }
                });
            }
        });

    });
});