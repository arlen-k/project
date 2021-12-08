import request from "./request"
import qs from 'qs'

export const httpImg = location.origin+"/artic/photo/"  // 查看
export const upUrl = '/artic/photo/upload' // 上传

export function login(params) {
  return request({
    url: "/artic/loginUser",
    method: "post",
    data:params
  })
}

export function getMsgList(params) {
  return request({
    url: "/member/getMsgList",
    method: "post",
    data:qs.stringify( params)
  })
}

export function addmessage(params) {
  return request({
    url: "/member/message",
    method: "post",
    data:qs.stringify( params)
  })
}

export function deleteMsg(params) {
  return request({
    url: "/member/deleteMsg",
    method: "post",
    data:qs.stringify( params)
  })
}

export function editMsg(params) {
  return request({
    url: "/member/editMsg",
    method: "post",
    data:qs.stringify( params)
  })
}

export function addArtic(params) {
  return request({
    url: "/artic/addartic",
    method: "post",
    data:qs.stringify( params)
  })
}

export function getArtList(params) {
  return request({
    url: "/artic/getArtList",
    method: "post",
    data:qs.stringify( params)
  })
}

export function deleteArt(params) {
  return request({
    url: "/artic/deleteArt",
    method: "post",
    data:qs.stringify( params)
  })
}

export function artInfo(params) {
  return request({
    url: "/artic/artInfo",
    method: "post",
    data:qs.stringify( params)
  })
}

export function editArt(params) {
  return request({
    url: "/artic/editArt",
    method: "post",
    data:qs.stringify( params)
  })
}

// 视频

export function getVideoList(params) {
  return request({
    url: "/artic/getVideoList",
    method: "post",
    data:qs.stringify( params)
  })
}

export function editVideo(params) {
  return request({
    url: "/artic/editVideo",
    method: "post",
    data:qs.stringify( params)
  })
}

export function deleteVideo(params) {
  return request({
    url: "/artic/deleteVideo",
    method: "post",
    data:qs.stringify( params)
  })
}

export function addvideo(params) {
  return request({
    url: "/artic/addvideo",
    method: "post",
    data:qs.stringify( params)
  })
}
