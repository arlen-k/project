/*
 * @Description: 
 * @Version: 2.0
 * @Autor: 作者博客：www.arlen.top
 * @Date: 2021-07-06 10:02:20
 * @LastEditors: Seven
 * @LastEditTime: 2021-11-16 16:04:59
 */
import axios from 'axios'
import Vue from  'vue'
// import routeList from '../router'

let _this =new Vue()
var request = axios.create({
  // baseURL: process.env.VUE_APP_BASE_API,
  timeout: 60000
})

request.interceptors.request.use( config => {
    config.headers['token'] =  sessionStorage.token || ''
    return config
  },
  error => {
    Promise.reject(error)
  }
)

request.interceptors.response.use( response => {
    let data = response.data
    if(data.code!=200){
      _this.$message({
        message: data.msg,
        type: 'err'
      }); 
      if(data.code==401){
        sessionStorage.removeItem('token')
        location.href='/#/login' 
        return
      } 
      return Promise.reject('error')
    }   
    
    return response.data
     
  },
  error => {
    _this.$message({
      message:'服务器错误',
      type: 'error'
    });
    Promise.reject(error)
  }
)

export default request;