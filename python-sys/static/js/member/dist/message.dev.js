"use strict";

;
var member_reg_ops = {
  init: function init() {
    this.eventBind();
  },
  eventBind: function eventBind() {
    $(".reg_wrap .do-reg").click(function () {
      var btn_target = $(this);

      if (btn_target.hasClass("disabled")) {
        common_ops.alert("正在处理！！请不要重复点击~~");
        return;
      }

      var msg = $(".reg_wrap textarea[name=nickname]").val();
      var name = $(".userName").html();

      if (msg == undefined || msg.length < 1) {
        common_ops.alert("请输入不为空内容~~");
        return;
      } // btn_target.addClass("disabled"); //重复点击文件


      $.ajax({
        url: common_ops.buildUrl("/member/message"),
        type: "POST",
        data: {
          content: msg,
          name: name
        },
        dataType: 'json',
        success: function success(res) {
          btn_target.removeClass("disabled");
          var callback = null;

          if (res.code == 200) {
            callback = function callback() {
              location.reload();
            };
          }

          common_ops.alert(res.msg, callback);
        }
      });
    });
  }
};
$(document).ready(function () {
  member_reg_ops.init();
});