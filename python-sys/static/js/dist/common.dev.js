"use strict";

;
var common_ops = {
  buildUrl: function buildUrl(path, params) {
    //params = { "test":"abc","sort":"asc" };
    // ?test=abc&sort=asc
    var url = "" + path;
    var _param_url = "";

    if (params) {
      _param_url = Object.keys(params).map(function (k) {
        return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=");
      }).join("&");
      _param_url = "?" + _param_url;
    }

    return url + _param_url;
  },
  alert: function alert(msg, cb) {
    layer.alert(msg, {
      yes: function yes(index) {
        if (typeof cb == "function") {
          cb();
        }

        layer.close(index);
      }
    });
  }
};

window.onload = function () {
  $(".navbar-nav li").removeClass("active");
  var list = ['/', '/member/message'];
  var url = window.location.pathname;
  list.forEach(function (item, i) {
    if (url == item) {
      var add = $(".navbar-nav .li")[i];
      add.classList.add("active");
    }
  });
};