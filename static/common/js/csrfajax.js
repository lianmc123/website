// 对jQuery的ajax封装
// 在header部分:<meta name="csrf-token" content="{{ csrf_token() }}">
'use strict';
var csrfajax = {
    'get' :function (args) {
        args['method'] = 'get';
        this.ajax(args)
    },
    'post' :function (args) {
        args['method'] = 'post';
        this.ajax(args)
    },
    'ajax':function (args) {
        //设置csrftoken
        this._ajaxSetup();
        $.ajax(args);
    },
    '_ajaxSetup': function () {
        $.ajaxSetup({
            beforeSend: function(xhr, settings){
                if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomail){
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        });
    }
};