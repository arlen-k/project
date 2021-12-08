/**
 * @param {Function} fn 防抖函数
 * @param {Number} delay 延迟时间
 */
export function debounce(fn, delay) {
  var timer
  return function () {
    var context = this
    var args = arguments
    clearTimeout(timer)
    timer = setTimeout(function () {
      fn.apply(context, args)
    }, delay)
  }
}

/**
 * @param {date} time 需要转换的时间
 * @param {String} fmt 需要转换的格式 如 yyyy-MM-dd、yyyy-MM-dd HH:mm:ss
 */
export function formatTime(time, fmt) {
  if (!time) return ''
  else {
    const date = new Date(time)
    const o = {
      'M+': date.getMonth() + 1,
      'd+': date.getDate(),
      'H+': date.getHours(),
      'm+': date.getMinutes(),
      's+': date.getSeconds(),
      'q+': Math.floor((date.getMonth() + 3) / 3),
      S: date.getMilliseconds(),
    }
    if (/(y+)/.test(fmt))
      fmt = fmt.replace(
        RegExp.$1,
        (date.getFullYear() + '').substr(4 - RegExp.$1.length)
      )
    for (const k in o) {
      if (new RegExp('(' + k + ')').test(fmt)) {
        fmt = fmt.replace(
          RegExp.$1,
          RegExp.$1.length === 1
            ? o[k]
            : ('00' + o[k]).substr(('' + o[k]).length)
        )
      }
    }
    return fmt
  }
}

 
export const isEmpty = function(value) {
  return (Array.isArray(value) && value.length === 0) 
      || (Object.prototype.isPrototypeOf(value) && Object.keys(value).length === 0)
}

//日期转换
Date.prototype.format = function (format) {
  var args = {
      "M+": this.getMonth() + 1,
      "d+": this.getDate(),
      "h+": this.getHours(),
      "m+": this.getMinutes(),
      "s+": this.getSeconds(),
      "q+": Math.floor((this.getMonth() + 3) / 3),  //quarter
      "S": this.getMilliseconds()
  }
  if (/(y+)/.test(format))
      format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length))
  for (var i in args) {
      var n = args[i]
      if (new RegExp("(" + i + ")").test(format))
          format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? n : ("00" + n).substr(("" + n).length))
  }
  return format
}

//locationStorage
export const Storage = {
 //存储单个属性
    set :function(key,value){
        window.localStorage[key]=value
    },
    //读取单个属性
    get:function(key,defaultValue){
        return  window.localStorage[key] || defaultValue
    },
    remove:function(key){
        return window.localStorage.removeItem(key)
    },
    //存储对象，以JSON格式存储
    setObject:function(key,value){
        window.localStorage[key]=JSON.stringify(value)
    },
    //读取对象
    getObject: function (key) {
        return JSON.parse(window.localStorage[key] || '{}')
    }
}