const path = require('path')
const resolve = dir => {
  return path.join(__dirname, dir)
}
let http = 'http://127.0.0.1:80'
module.exports = {
  publicPath: './',
  chainWebpack: config => {
    config.resolve.alias
      .set('_c', resolve('src/components')) // key,value自行定义，比如.set('@@', resolve('src/components'))
  },
  devServer: {
      open: true,
      proxy: {
          '/member': {
              target:http ,//要代理的本地api地址，也可以换成线上测试地址
              changeOrigin: true,//允许跨域
              pathRewrite:{
                "^/member":"/member"
              }//将/api开头替换为/api
          },
          '/artic': {
            target: http,//要代理的本地api地址，也可以换成线上测试地址
            changeOrigin: true,//允许跨域
            pathRewrite:{
              "^/artic":"/artic"
            }//将/api开头替换为/api
        },
        
      }
  },
  lintOnSave: false// 屏蔽EsLint
}