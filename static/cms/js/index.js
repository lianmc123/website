$(function(){
    $(".navbar-brand").on('click',function(){
        var url = $(this).attr('href');
        $("#J_iframe").attr('src',url);
        return false;
    });
    $(".J_menuItem").on('click',function(){
        var url = $(this).attr('href');
        $("#J_iframe").attr('src',url);
        return false;
    });
    $("#user_profile").click(function (event) {
        event.preventDefault();
        var url = $(this).attr('href')
        $("#J_iframe").attr('src',url);
        return false;
    });
});